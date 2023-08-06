# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiobafi6', 'aiobafi6.cmd', 'aiobafi6.proto']

package_data = \
{'': ['*']}

install_requires = \
['protobuf>=3.20,<3.21', 'zeroconf>=0.38,<0.39']

entry_points = \
{'console_scripts': ['aiobafi6 = aiobafi6.cmd.main:main']}

setup_kwargs = {
    'name': 'aiobafi6',
    'version': '0.1.0',
    'description': 'Big Ass Fans i6/Haiku protocol asynchronous Python library',
    'long_description': '# Big Ass Fans i6\n\naiobafi6 is a python library to discovery, query and control\n[Big Ass Fans](https://bigassfans.com) products that use the i6 protocol, which\nincludes i6 fans and Haiku fans with the 3.0 firmware.\n\nIt supports almost all the features of the previous protocol ("SenseMe"), with\nthe exception of presence sensing, rooms, and sleep mode.\n\n## Compiling the aiobafi6 protocol buffer\n\nThe BAF i6 protocol uses\n[protocol buffers](https://developers.google.com/protocol-buffers) for message\nwire serialization. This library maintains a\n[single proto file](proto/aiobafi6.proto) with all known messages and contants.\n\nThe generated Python client for this proto file is checked in the repo to avoid\ndepending on the protocol buffer compiler for installation. Whenever the source\nproto file is changed, the Python client files must be re-generated.\n\n`poe protoc`\n',
    'author': 'Jean-Francois Roy',
    'author_email': 'jf@devklog.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jfroy/aiobafi6',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
