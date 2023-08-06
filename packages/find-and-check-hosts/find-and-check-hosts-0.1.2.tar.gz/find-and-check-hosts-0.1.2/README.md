# find-and-check-hosts

[![PyPI version](https://img.shields.io/pypi/v/find-and-check-hosts)](https://pypi.org/project/find-and-check-hosts/)
![License](https://img.shields.io/pypi/l/find-and-check-hosts)
![Python versions](https://img.shields.io/pypi/pyversions/find-and-check-hosts)


Searches files for IPs and hostnames and checks them against a rule list to prevent accidentially leaking sensitive information.

## Installation

This repo can now be installed with pip:
```
pip install find-and-check-hosts
```

Or you can install it manually by following these steps:

1. Clone this repository
2. Install the dependencies listed in `./requirements.txt` with pip
3. (Optional) Do a `pip install .` to add the `find-and-check-hosts` command to your PATH

## Usage

If you did the pip installation, you should be able to just call the installed script:
```
find-and-check-hosts <arguments>
```

If you just cloned it, you need to call it by path:
```
./src/main.py <arguments>
```

## Notable changes

### Version 0.1.2

- Added a `domain` filter, that will match a domain and any subdomains. For example `domain: example.com` will match `example.com`, `my.subdomain.example.com`, but not `my-example.com` or `example-com`.
- Allowed the `regex`, `glob` and `domain` fields to also accept a list of values. For example:
    ```
    hostname_rules:
    - status: ok
    - domain:
      - example.com
      - example.org
    ```

