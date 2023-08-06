#!/usr/bin/env python3
import argparse
import csv
import fnmatch
import glob
import logging
import os
import re
import traceback
from typing import Any, Optional
#  local files
from . import RuleConfigFile, load_rule_file
# pip dependencies
from termcolor import colored


STATUS_COLORS = {
    "ok": ("green", ["bold"]),
    "warn": ("yellow", ["bold"]),
    "bad": ("red", ["bold"]),
}


def read_tld_list() -> list[str]:
    script_dir = os.path.dirname(os.path.realpath(__file__))
    tld_file = os.path.join(script_dir, "iana_tld_list.txt")

    with open(tld_file, "r") as f:
        tld_list = f.read().split("\n")

    # Unify entries: Remove laeding and trailing whitespaces and make them lowercase
    tld_list = [x.strip().lower() for x in tld_list]
    # Remove comments and empty lines
    tld_list = [x for x in tld_list if x and not x.startswith("#")]
    return tld_list


def get_better_tld_list() -> list[str]:
    tld_list = read_tld_list()
    
    if "py" in tld_list:
        # would cause false positives for python scripts. Sorry Paraguay :)
        tld_list.remove("py")
        # Add back some "common" generic second-level domain names
        tld_list += ["com.py", "coop.py", "edu.py", "mil.py", "gov.py", "org.py", "net.py", "una.py"]

    if "md" in tld_list:
        # would couse false positives for markdown files. And I never seen a Moldovan domain
        tld_list.remove("md")
        # Add back some "common" generic second-level domain names
        tld_list += ["com.md", "srl.md", "sa.md", "net.md", "org.md", "acad.md"]

    if "zip" in tld_list:
        tld_list.remove("zip") # who thought this one was a good idea?

    # let's add some common internal network names
    tld_list += ["lan", "local", "intern", "internal", "intranet", "intra"]
    
    # .ip is for "speedport.ip", .box for fritz.box, .htb for hack the box machines
    tld_list += ["ip", "box", "htb"]
    
    # and some reserved TLDs
    tld_list += ["test", "example", "invalid", "localhost"]

    # remove duplicates and order them alphabetically
    return sorted(set(tld_list))


def build_ip_regex() -> str:
    boundary = "[^A-Za-z0-9.]"
    start_boundary = f"(?:(?<={boundary})|^)"
    end_boundary = f"(?:(?={boundary})|$)"
    byte = "(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
    return f"{start_boundary}{byte}(?:\\.{byte}){{3}}{end_boundary}"


def build_hostname_regex() -> str:
    # Make sure, that we match the whole domain and fail if it is malformed (like having a . at the end)
    boundary = "[^-_~\$A-Za-z0-9.]"
    start_boundary = f"(?:(?<={boundary})|^)"
    end_boundary = f"(?:(?={boundary})|$)"
    # A part of a domain. Acn contain letters, numbers and dashes. But dashes can not be the first or last character
    part = "(?!-)[A-Za-z0-9-]{1,63}(?<!-)"
    # domain regex. May not work for some net tlds such as .accountants
    
    tld_list = get_better_tld_list()

    tld = "(?:" + "|".join(tld_list) + ")"
    domain_with_tld = start_boundary + f"(?:{part}\\.)+{tld}"
    # internal domains don't need a .something at the end
    internal_url_with_scheme = f"(?<=[a-zA-Z0-9]:\/\/)(?:{part}\\.)*{part}"

    # Match either an internal or a normal public domain
    combined = f"(?:{domain_with_tld}|{internal_url_with_scheme}){end_boundary}"
    return combined


STATUS_BADNESS_ORDER = ["ok", "warn", "bad"]
CHECK_FILE_EXTENSIONS = [".md", ".txt", ".tex"]
IP_REGEX = re.compile(build_ip_regex())
HOSTNAME_REGEX = re.compile(build_hostname_regex())
HOSTNAME_OR_IP_REGEX = re.compile(f"(?:{IP_REGEX.pattern}|{HOSTNAME_REGEX.pattern})")
CSV_HEADER = ["file", "line_nr", "column_nr", "value", "status"]


def get_worst_status(status_list: list[str]):
    status_badness = [STATUS_BADNESS_ORDER.index(x) for x in status_list]
    worst_index = max(status_badness)
    return STATUS_BADNESS_ORDER[worst_index]


def should_check_file(path: str) -> bool:
    for extension in CHECK_FILE_EXTENSIONS:
        if path.endswith(extension):
            return True
    return False


def color_by_status(text: str, status: str, ignore_attrs: bool = False) -> str:
    color_name, attrs = STATUS_COLORS[status]
    if ignore_attrs:
        attrs = []
    return colored(text, color_name, attrs=attrs)

class FileChecker:
    def __init__(self, config: RuleConfigFile, show_status_list: list[str], create_csv: bool):
        self.config = config
        self.show_status_list = show_status_list
        self.create_csv = create_csv
        # Each entry is a row. Each row is a list: [file, line_nr, column_nr, value, status]
        # The line_nr and column_nr each start at 1
        self.csv_data = []
        self.counts = {
            "ok": 0,
            "warn": 0,
            "bad": 0,
        }


    def check_file(self, path: str) -> None:
        with open(path, "r") as f:
            lines = f.read().split("\n")
    
        for index, line in enumerate(lines):
            matches_status_list = [(match, self.get_status(match.group(0))) for match in HOSTNAME_OR_IP_REGEX.finditer(line)]
            # remove any entries that have a status that should not be shown
            matches_status_list = [(ip, status) for ip, status in matches_status_list if status in self.show_status_list]
            if matches_status_list:
                colored_line = line

                # Do it in reverse, since the addidion of color codes would otherwise mess up the following indices
                for match, status in reversed(matches_status_list):
                    self.counts[status] += 1

                    ip = match.group(0) # 0 = entire match
                    start, end = match.span()
                    colored_ip = color_by_status(ip, status)
                    colored_line = colored_line[:start] + colored_ip + colored_line[end:]

                    if self.create_csv:
                        self.csv_data.append([path, index + 1, start + 1, ip, status])

                worst_status = get_worst_status(status for _, status in matches_status_list)
                tag = color_by_status(worst_status.upper(), worst_status, ignore_attrs=True)
                colored_path = colored(path, "magenta")
                print(f"[{tag}] {colored_path}:{index+1}\n{colored_line}\n")

    def get_status(self, match_text: str) -> str:
        if IP_REGEX.fullmatch(match_text):
            return self.config.ip_rules.get_status(match_text)
        else:
            return self.config.hostname_rules.get_status(match_text)

    def print_summary(self) -> None:
        lines = []
        for status in self.show_status_list:
            count = self.counts[status]
            if count != 0:
                colored_count = color_by_status(count, status)
                lines.append(f"{colored_count} {status}")

        if lines:
            tag = colored("INFO", "blue")
            print(f"[{tag}] Summary:", ", ".join(lines))


def parse_cli_arguments() -> Any:
    ap = argparse.ArgumentParser()
    ap.add_argument("root_dir", help="directory that will be recursively searched for files containing potential leaks")
    ap.add_argument("-c", "--config", help="the config file with the rules, that will be used for the IP and hostname classification")
    ap.add_argument("--csv", help="write the results as a cvs to the given file")
    ap.add_argument("-d", "--debug", action="store_true", help="enable additional debugging outpust (like the used regexes)")
    group_status = ap.add_argument_group("Filter by status")
    group_show_hide = group_status.add_mutually_exclusive_group()
    group_show_hide.add_argument("-s", "--show", help="only shows entries with the given statuses. Multiple values can be passed using comas (example: 'warn,bad')")
    group_show_hide.add_argument("-S", "--hide", help="shows all entries that do NOT match the given statuses. Multiple values can be passed using comas (example: 'ok,warn')")

    return ap.parse_args()


def determine_statuses_to_show(show: Optional[str], hide: Optional[str]):
    def split_entries(string: str) -> list[str]:
        entries = [x.strip() for x in string.split(",")]
        # remove duplicates
        entries = list(set(entries))
        for x in entries:
            if x not in STATUS_BADNESS_ORDER:
                raise Exception(f"Unknown status '{x}' in '{string}'")
        return entries

    # Check against None to correctly handle empty strings as arguments
    if show is None and hide is None:
        # Show all statuses by default
        return STATUS_BADNESS_ORDER
    elif show is None:
        # Handle the hide parameter
        hide_list = split_entries(hide)
        return [status for status in STATUS_BADNESS_ORDER if status not in hide_list]
    elif hide is None:
        # Handle show parameter
        show_list = split_entries(show)
        return show_list
    else:
        raise Exception("Both 'show' and 'hide' are defined, but they are mutually exclusive")


def main():
    args = parse_cli_arguments()

    if args.debug:
        logging.basicConfig(format="[%(levelname)s] %(message)s",level=logging.DEBUG)

    logging.debug("IP search regex: %s", IP_REGEX.pattern)
    logging.debug("Hostname search regex: %s", HOSTNAME_REGEX.pattern)

    if args.config:
        config_path = args.config
    else:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(script_dir, "example-config.yaml")
    config = load_rule_file(config_path)

    show_status_list = determine_statuses_to_show(args.show, args.hide)

    file_checker = FileChecker(config, show_status_list, bool(args.csv))

    root_dir = args.root_dir
    if not os.path.isdir(root_dir):
        raise Exception(f"'{root_dir}' is not an existing directory")
    for dir_path, dir_names, file_names in os.walk(root_dir):
        for name in file_names:
            path = os.path.join(dir_path, name)
            if should_check_file(path):
                try:
                    file_checker.check_file(path)
                except Exception:
                    print(f"[ERROR] Error while checking '{path}'")
                    traceback.print_exc()
    
    file_checker.print_summary()

    if args.csv:
        with open(args.csv, 'w') as csvfile: 
            writer = csv.writer(csvfile) 

            writer.writerow(CSV_HEADER)                
            for row in file_checker.csv_data:
                writer.writerow(row)
        print(f"Written results as CSV to '{args.csv}'") 


if __name__ == "__main__":
    main()
