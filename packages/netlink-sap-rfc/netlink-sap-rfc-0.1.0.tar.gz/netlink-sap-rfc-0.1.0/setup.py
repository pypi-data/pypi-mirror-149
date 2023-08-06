# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rfc']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.8.0,<5.0.0', 'netlink-logging>=0.1.0,<0.2.0', 'pyrfc>=2.5.0,<3.0.0']

setup_kwargs = {
    'name': 'netlink-sap-rfc',
    'version': '0.1.0',
    'description': 'Access SAP via RFC',
    'long_description': '# netlink-sap-rfc\n\nTools for SAP RFC\n\n',
    'author': 'Bernhard Radermacher',
    'author_email': 'bernhard.radermacher@netlink-consulting.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/netlink-consulting/netlink-sap-rfc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
