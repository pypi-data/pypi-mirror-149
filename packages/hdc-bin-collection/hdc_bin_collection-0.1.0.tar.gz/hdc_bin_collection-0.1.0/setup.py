# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hdc_bin_collection']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.0,<5.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'hdc-bin-collection',
    'version': '0.1.0',
    'description': 'A module that finds the next bin collection dates for a specific address in Market Harborough, UK. Uses the UPRN to find the address.',
    'long_description': '## Harborough District Council - Bin Collection Dates\n\nA (very) small Python library which takes a UPRN within Market Harborough as a parameter, and returns a dictionary with bin types as keys, and next bin collection dates as values.\n',
    'author': 'Aaron Carson',
    'author_email': 'aaron@aaroncarson.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/caraar12345/hdc-bin-collection',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
