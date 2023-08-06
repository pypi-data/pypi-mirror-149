# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dycw_template']

package_data = \
{'': ['*']}

install_requires = \
['gitpython>=3.1.27,<4.0.0']

setup_kwargs = {
    'name': 'dycw-template',
    'version': '0.1.6',
    'description': 'DYCW template package',
    'long_description': None,
    'author': 'Derek Wan',
    'author_email': 'd.wan@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
