#!/usr/bin/env python3
import fnmatch
import logging
from typing import NamedTuple
import re
# pip dependencies
import yaml
from schema import Optional as Nullable, Schema, SchemaError, Or

VALID_STATUS_LIST = ["ok", "warn", "bad"]


SCHEMA_RULE = {
    "status": Or(*VALID_STATUS_LIST),
    Or("glob", "regex", "domain", only_one=True): Or(str, list[str]),
}

SCHEMA_CONFIG = Schema({
    "ip_rules": [SCHEMA_RULE],
    "hostname_rules": [SCHEMA_RULE]
})

def domain_to_regex(domain: str) -> str:
    if "\\" in domain:
        raise Exception(f"A domain may not contain a backslash. Rejected '{domain}'")
    # escape dot's since they represent the wildcard character in an regex
    regex = domain.replace(".", "\\.")
    # Add a prefix that allows subdomains. For example the domain 'example.com' will should also match 'www.example.com'
    regex = "(.+\\.)?" + regex
    return regex

class Rule:
    def __init__(self, rule: dict):
        regex = rule.get("regex")
        glob = rule.get("glob")
        domain = rule.get("domain")
        if regex and glob:
            raise Exception("Both 'regex' and 'glob' specified")
        if regex and domain:
            raise Exception("Both 'regex' and 'domain' specified")
        if not regex and not glob and not domain:
            raise Exception("You need to define 'regex', 'glob' or 'domain'")
        
        # make sure that regex is a list
        if type(regex) != list:
            regex = [regex] if regex else []
        
        # convert domain to regex
        if domain:
            if type(domain) != list:
                domain = [domain] if domain else []
            regex = [domain_to_regex(x) for x in domain]

        # convert glob to regex
        if glob:
            if type(glob) != list:
                glob = [glob] if glob else []
            regex = [fnmatch.translate(x) for x in glob]

        self.regex_list = [re.compile(x) for x in regex]

        status = rule.get("status")
        if status not in VALID_STATUS_LIST:
            raise Exception(f"Not a valid status: '{status}'")
        self.status = status

        logging.debug(f"Rule: '{regex}' -> {status}")

    def is_match(self, value) -> bool:
        for regex in self.regex_list:
            if regex.fullmatch(value):
                return True
        return False


class RuleList:
    def __init__(self, rules: list[dict]):
        self.rules = [Rule(x) for x in rules]

    def get_status(self, value):
        for rule in self.rules:
            if rule.is_match(value):
                return rule.status
        raise Exception(f"No rule matches '{value}'. Please add a fallback as a last rule (status: <status>, glob: *)")


class RuleConfigFile(NamedTuple):
    ip_rules: RuleList
    hostname_rules: RuleList


def load_rule_file(path: str) -> RuleConfigFile:
    logging.debug(f"Loading rules from '{path}'")
    with open(path, "rb") as f:
        data = yaml.safe_load(f)

    SCHEMA_CONFIG.validate(data)

    logging.debug(f"Parsing IP rule list")
    ip_rules = RuleList(data["ip_rules"])
    logging.debug(f"Parsing hostname rule list")
    hostname_rules = RuleList(data["hostname_rules"])
    return RuleConfigFile(ip_rules=ip_rules, hostname_rules=hostname_rules)



def run_test():
    import os
    script_dir = os.path.dirname(os.path.realpath(__file__))

    ip_list = ["1.1.1.1", "127.0.0.1", "127.127.127.127", "192.169.0.0", "172.18.0.0"]
    example_rules_path = os.path.join(script_dir, "example-config.yaml")
    config = load_rule_file(example_rules_path)

    for ip in ip_list:
        print("IP:", ip)
        print("Status:", config.ip_rules.get_status(ip))
        print()


if __name__ == "__main__":
    run_test()
