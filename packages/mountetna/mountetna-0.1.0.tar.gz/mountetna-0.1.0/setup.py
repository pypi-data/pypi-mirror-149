# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mountetna']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.1,<2.0.0']

setup_kwargs = {
    'name': 'mountetna',
    'version': '0.1.0',
    'description': 'Client package for Mount Etna data library',
    'long_description': '# Mount Etna\n\nBase Python client for the Mount Etna Data Library system.\n',
    'author': 'Zachary Collins',
    'author_email': 'zachary.collins@ucsf.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mountetna/monoetna',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
