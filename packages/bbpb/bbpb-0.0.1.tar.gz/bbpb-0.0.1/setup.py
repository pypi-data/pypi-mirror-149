# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blackboxprotobuf']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bbpb',
    'version': '0.0.1',
    'description': 'Library for working with protobuf messages without a protobuf type definition.',
    'long_description': None,
    'author': 'Ryan Winkelmaier',
    'author_email': 'ryan.winkelmaier@nccgroup.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nccgroup/blackboxprotobuf',
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
