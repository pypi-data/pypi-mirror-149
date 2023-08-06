# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['lakedrive',
 'lakedrive.common',
 'lakedrive.core',
 'lakedrive.httplibs',
 'lakedrive.localfs',
 'lakedrive.s3']

package_data = \
{'': ['*'], 'lakedrive.s3': ['testfiles/*']}

modules = \
['py']
install_requires = \
['coverage>=6.2,<7.0']

setup_kwargs = {
    'name': 'lakedrive',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'anthony',
    'author_email': 'anthony.potappel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
