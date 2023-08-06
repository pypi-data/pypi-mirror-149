# Flake8 prometheus metric name plugin


[![pypi](https://badge.fury.io/py/flake8-prometheus-metrics-name.svg)](https://pypi.org/project/flake8-prometheus-metrics-name/)
[![Python: 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://pypi.org/project/flake8-breakpoint)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://en.wikipedia.org/wiki/MIT_License)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Flake8 plugin to check metrics name prefix for official client https://github.com/prometheus/client_python.

## Installation
```bash
pip install flake8-prometheus-metrics-name
```

## Usage
Imagine we have python module `some_module.py`:
```python
from prometheus_client import Counter

Counter(name='kek_values', documentation='some doc')
Counter(name='some_name1', documentation='some doc')
Counter(name='some_name2', documentation='some doc')  # noqa: PRM902
Counter(name='some_name3', documentation='some doc')
Counter(name='lol_values', documentation='some doc')
```

Add valid metrics name prefixes to `setup.cfg`:
```buildoutcfg
[flake8]
prometheus-metrics-name-prefixes =
    kek_
    lol_
```

Run flake8 `flake8 some_modue.py` cause following warnings:
```bash
some_module.py:4:1: PRM902: Metric name should start with one of following prefixes: "kek_", "lol_", got "some_name1" instead
some_module.py:6:1: PRM902: Metric name should start with one of following prefixes: "kek_", "lol_", got "some_name3" instead
```

Plugin also may be disabled by adding following option to `setup.cfg`:
```buildoutcfg
[flake8]
prometheus-metrics-disabled = 1
```
then AST nodes will not be analized for metrics name on flake8 run.

## License
MIT
