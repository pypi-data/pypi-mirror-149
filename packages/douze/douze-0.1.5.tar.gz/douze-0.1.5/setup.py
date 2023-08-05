# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['douze']

package_data = \
{'': ['*']}

install_requires = \
['typefit>=0.4.0,<0.5.0']

setup_kwargs = {
    'name': 'douze',
    'version': '0.1.5',
    'description': 'A DigitalOcean API client to help with 12-factors apps',
    'long_description': 'DOuze\n=====\n\nA DigitalOcean client library aimed to be a backend for Ansible modules.\n\nYou can find:\n\n- `douze.api.DoApi` &mdash; The main API which mimics the REST API\n- `douze.api.DoIdemApi` &mdash; The idempotent API which can power Ansible\n  modules\n',
    'author': 'Rémy Sanchez',
    'author_email': 'remy.sanchez@hyperthese.net',
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
