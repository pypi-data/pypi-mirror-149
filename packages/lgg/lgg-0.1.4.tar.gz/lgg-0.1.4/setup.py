# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lgg']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'lgg',
    'version': '0.1.4',
    'description': 'A simple yet fancy logger for Python scripts',
    'long_description': "# python-logger\nA simple yet fancy logger for Python scripts\n\n\n## Install\n- Using pip:\n```shell\npip install lgg\n```\n\n- Using Poetry:\n```shell\npoetry add lgg\n```\n\n## Usage\n```python\nlogger = get_logger()\n\nlogger.info('This is an info message')\n\nlogger.debug('Debugging message')\n\nlogger.error('error message')\n\nlogger.warning('DeprecationWarning: this feature won\\'t'\n               ' be available in the next release v0.10.0')\n```\n![Result](.resources/overview.png)\n",
    'author': 'Ayoub Assis',
    'author_email': 'assis.ayoub@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/blurry-mood/python-logger',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
