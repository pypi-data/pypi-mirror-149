# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hypothesis_faker']

package_data = \
{'': ['*']}

install_requires = \
['faker>=13.7.0,<14.0.0',
 'hypothesis>=6.14.0,<7.0.0',
 'writer-cm>=1.1.1,<2.0.0',
 'xdg>=5.1.1,<6.0.0']

setup_kwargs = {
    'name': 'hypothesis-faker',
    'version': '0.1.2',
    'description': 'faker providers wrapped as hypothesis strategies',
    'long_description': None,
    'author': 'Derek Wan',
    'author_email': 'd.wan@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dycw/hypothesis-faker',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
