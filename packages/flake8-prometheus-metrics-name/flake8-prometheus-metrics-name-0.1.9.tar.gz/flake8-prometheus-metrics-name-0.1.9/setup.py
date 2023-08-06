# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_prometheus_metrics_name']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=4.0.0,<5.0.0', 'prometheus_client>=0.7.1,<0.8.0']

entry_points = \
{'flake8.extension': ['PRM = flake8_prometheus_metrics_name.api:Api']}

setup_kwargs = {
    'name': 'flake8-prometheus-metrics-name',
    'version': '0.1.9',
    'description': 'Flake8 plugin for prometheus metric name validation',
    'long_description': '# Flake8 prometheus metric name plugin\n\n\n[![pypi](https://badge.fury.io/py/flake8-prometheus-metrics-name.svg)](https://pypi.org/project/flake8-prometheus-metrics-name/)\n[![Python: 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://pypi.org/project/flake8-breakpoint)\n[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://en.wikipedia.org/wiki/MIT_License)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\nFlake8 plugin to check metrics name prefix for official client https://github.com/prometheus/client_python.\n\n## Installation\n```bash\npip install flake8-prometheus-metrics-name\n```\n\n## Usage\nImagine we have python module `some_module.py`:\n```python\nfrom prometheus_client import Counter\n\nCounter(name=\'kek_values\', documentation=\'some doc\')\nCounter(name=\'some_name1\', documentation=\'some doc\')\nCounter(name=\'some_name2\', documentation=\'some doc\')  # noqa: PRM902\nCounter(name=\'some_name3\', documentation=\'some doc\')\nCounter(name=\'lol_values\', documentation=\'some doc\')\n```\n\nAdd valid metrics name prefixes to `setup.cfg`:\n```buildoutcfg\n[flake8]\nprometheus-metrics-name-prefixes =\n    kek_\n    lol_\n```\n\nRun flake8 `flake8 some_modue.py` cause following warnings:\n```bash\nsome_module.py:4:1: PRM902: Metric name should start with one of following prefixes: "kek_", "lol_", got "some_name1" instead\nsome_module.py:6:1: PRM902: Metric name should start with one of following prefixes: "kek_", "lol_", got "some_name3" instead\n```\n\nPlugin also may be disabled by adding following option to `setup.cfg`:\n```buildoutcfg\n[flake8]\nprometheus-metrics-disabled = 1\n```\nthen AST nodes will not be analized for metrics name on flake8 run.\n\n## License\nMIT\n',
    'author': 'perminovs',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/perminovs/flake8_prometheus_metrics_name',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
