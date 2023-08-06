# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pre_commit_cairo']

package_data = \
{'': ['*']}

install_requires = \
['cairo-lang==0.8.1', 'rich>=12.2.0,<13.0.0']

entry_points = \
{'console_scripts': ['check-format = pre_commit_cairo.check_format:main',
                     'check-lint = pre_commit_cairo.check_lint:main']}

setup_kwargs = {
    'name': 'pre-commit-cairo',
    'version': '0.0.15',
    'description': '',
    'long_description': None,
    'author': 'franalgaba',
    'author_email': 'f.algaba@outlook.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
