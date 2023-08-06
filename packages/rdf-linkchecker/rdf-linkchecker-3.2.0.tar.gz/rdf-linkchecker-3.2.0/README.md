# rdf_linkchecker

<div align="center">

[![Build status](https://github.com/WWU-AMM/rdf_linkchecker/workflows/build/badge.svg?branch=main&event=push)](https://github.com/WWU-AMM/rdf_linkchecker/actions?query=workflow%3Abuild)
[![Python Version](https://img.shields.io/pypi/pyversions/rdf_linkchecker.svg)](https://pypi.org/project/rdf_linkchecker/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/WWU-AMM/rdf_linkchecker/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/WWU-AMM/rdf_linkchecker/blob/main/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/WWU-AMM/rdf_linkchecker/releases)
[![License](https://img.shields.io/github/license/WWU-AMM/rdf_linkchecker)](https://github.com/WWU-AMM/rdf_linkchecker/blob/main/LICENSE)
![Coverage Report](assets/images/coverage.svg)

Check URLs in Triple-Store files.

</div>

## Installation

```bash
python3 -m pip install rdf-linkchecker
```

## Usage

Run with a list of files to check

```bash
rdf-linkchecker myonefile.ttl myotherfile.ttl
```

## Configuration

The `--config-filename` option can be used to pass an `INI`-style file.
```
[connection]
retries = 1
#seconds
timeout = 3
# first sleep in seconds between retries
# exponential backoff afterwards
sleep =1

[skip]
# any URL matching an entry in this comma separated list is not checked
domains = https://some.tld/path,http://someother.tld

# level: "all" | "only-failed" | "none"
# target: "console" | filename
"reporting": {"level": "all", "target": "console"}
```



## Credits [![🚀 Your next Python package needs a bleeding-edge project structure.](https://img.shields.io/badge/python--package--template-%F0%9F%9A%80-brightgreen)](https://github.com/TezRomacH/python-package-template)

This project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template)
