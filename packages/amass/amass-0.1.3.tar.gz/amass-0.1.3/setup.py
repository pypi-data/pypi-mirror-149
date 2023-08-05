# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['amass']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp', 'click', 'packaging', 'tomlkit']

entry_points = \
{'console_scripts': ['amass = amass.cli:cli']}

setup_kwargs = {
    'name': 'amass',
    'version': '0.1.3',
    'description': 'Vendor libraries from cdnjs',
    'long_description': '# amass\nVendor libraries from cdnjs\n',
    'author': 'James Meakin',
    'author_email': 'amass@jmsmkn.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jmsmkn/amass',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
