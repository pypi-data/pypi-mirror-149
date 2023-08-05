# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arcane', 'arcane.googleads']

package_data = \
{'': ['*']}

install_requires = \
['arcane-core>=1.7.0,<2.0.0',
 'arcane-datastore>=1.0.2,<2.0.0',
 'arcane-requests>=0.3.0,<0.4.0',
 'arcane-secret>=0.2.0,<0.3.0',
 'backoff==1.10.0',
 'google-ads>=15.1.1,<16.0.0',
 'pyyaml==5.4.1']

setup_kwargs = {
    'name': 'arcane-googleads',
    'version': '3.8.0',
    'description': "Un package pour interagir avec l'API Google Ads",
    'long_description': '# Arcane google-ads\n\nUtility package to interact with Google Ads\n',
    'author': 'Arcane',
    'author_email': 'product@arcane.run',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
