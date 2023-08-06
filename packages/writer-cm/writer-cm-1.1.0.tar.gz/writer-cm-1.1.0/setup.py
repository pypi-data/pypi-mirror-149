# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['writer_cm']

package_data = \
{'': ['*']}

install_requires = \
['atomicwrites>=1.4.0,<2.0.0']

setup_kwargs = {
    'name': 'writer-cm',
    'version': '1.1.0',
    'description': 'Atomically write files using a context manager',
    'long_description': None,
    'author': 'Derek Wan',
    'author_email': 'd.wan@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dycw/writer-cm',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
