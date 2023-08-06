# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prodigy']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'lxml>=4.6.3,<5.0.0',
 'requests-cache>=0.6.4,<0.7.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'prodigy-api',
    'version': '3.0.0',
    'description': 'Python Package to Hack Prodigy The Math Game',
    'long_description': '# Prodigy API\n\nThis is a Python Package to Hack Prodigy The Math Game.\n\nDocs: https://prodigy.readthedocs.io\n',
    'author': 'ProdigyAPI',
    'author_email': 'hostedpostedsite@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ProdigyAPI/ProdigyAPIWrapperInPython',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
