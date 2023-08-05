# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['specargs', 'specargs.framework']

package_data = \
{'': ['*']}

install_requires = \
['apispec-webframeworks>=0.5.2,<0.6.0',
 'apispec[marshmallow,yaml]>=5.1.1,<6.0.0',
 'attrs>=21.4.0,<22.0.0',
 'cattrs>=1.10.0,<2.0.0',
 'webargs>=8.1.0,<9.0.0']

setup_kwargs = {
    'name': 'specargs',
    'version': '0.1.0',
    'description': 'A library for request parsing and response serialization that generates OpenAPI Specification files',
    'long_description': '# specargs\n\n**specargs** is a Python library for request parsing and response serialization that generates OpenAPI\nSpecification files. **specargs** is built upon [marshmallow](https://marshmallow.readthedocs.io),\n[apispec](https://apispec.readthedocs.io), and [webargs](https://webargs.readthedocs.io). Full documentation can be\nfound at <https://specargs.rtfd.io>.\n\nThis project is under active development and should be considered unstable until the release of version 1.0.0.\n',
    'author': 'Manuel Zamora',
    'author_email': 'mzamora808@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/maz808/specargs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
