# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypipet',
 'pypipet.cli',
 'pypipet.cli.cli',
 'pypipet.core',
 'pypipet.core.fileIO',
 'pypipet.core.logging',
 'pypipet.core.model',
 'pypipet.core.operations',
 'pypipet.core.pipeline',
 'pypipet.core.shop_conn',
 'pypipet.core.sql',
 'pypipet.core.transform',
 'pypipet.plugins',
 'pypipet.plugins.canadapost',
 'pypipet.plugins.gg_merchant.shopping',
 'pypipet.plugins.gg_merchant.shopping.content',
 'pypipet.plugins.paypal',
 'pypipet.plugins.woocommerce']

package_data = \
{'': ['*'],
 'pypipet': ['pypipet.egg-info/*'],
 'pypipet.core': ['default_setting/*']}

install_requires = \
['Flask>=2.0.2,<3.0.0',
 'Jinja2>=3.0.3,<4.0.0',
 'ShopifyAPI>=10.0.0,<11.0.0',
 'click>=8.0,<9.0',
 'pandas>=1.2.0,<2.0.0',
 'pyactiveresource>=2.2.2,<3.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'requests>=2.23.0,<3.0.0',
 'sqlalchemy>=1.4.27,<2.0.0']

entry_points = \
{'console_scripts': ['pypipet = pypipet.cli:cli']}

setup_kwargs = {
    'name': 'pypipet',
    'version': '1.1.0',
    'description': 'pypipet',
    'long_description': '\n\n[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)\n[![Generic badge](https://img.shields.io/badge/Status-stable-blue.svg)](https://shields.io/)\n[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)\n[![Generic badge](https://img.shields.io/badge/Pypi-1.0.0-blue.svg)](https://shields.io/)\n[![Generic badge](https://img.shields.io/badge/Python-3.8-blue.svg)](https://shields.io/)\n\n\n# Introduction\n\n**`PyPipet`** is an open source project, aiming to integrate data flows of Ecommerce. It provides platform-independent data flows to support Ecommerce functionality. It simplifies data pipelines of data management in ecommerce, for example, adding catalog, updating product, managing inventory and orders, etc. It is specially customized for small business who are selling on wordpress (for example, with woocommerce), shopify, ebay, etc. (more frontshop connected will be added). It extremely handy if the business is selling on multiple platforms (e.g., for dropshipping). It makes it extreamly easy to move your frontshop from one platform to anothor.\n\n* For source code,  visit  [github repository](https://github.com/pypipet/pypipet).\n* For documentation, vist [docs](https://pypipet.com)\n\n## Latest `pip` [version: 1.1.0](https://pypi.org/project/pypipet/)\n\n### [Change Logs](https://pypi.org/project/changelogs)\n\n[reporting bugs here](https://github.com/pypipet/pypipet/issues)\n\n## [Dependencies](https://pypipet.com/dependencies)\n\n# Installation\n\nuse `pip`\n\n    pip install -r requirements.txt\n\n    pip install --upgrade pypipet  \n\n\nfor using Google Content API to connect Google Merchant, please install\n[`google_auth_httplib2`](https://pypi.org/project/google-auth-httplib2/)\nand [`googleapiclient`](https://github.com/googleapis/google-api-python-client)\n\n## Tested with\n\n- Shopify\n- Woocommerce with Wordpress.com\n- Postgresql\n- AWS RDS\n\n\n## Key features\n\n- cli supported\n- catalog import/export\n- product management for publishing\n- order management\n- fulfillment management\n- inventory management with multiple suppliers\n\n# [Quick start guide](https://pypipet.com/quick_start/create_project/)\n\n\n# [Use cases](https://pypipet.com/usecases/usecases)\n\n\n\n\n\n\n',
    'author': 'pypipet and contributors',
    'author_email': 'pypipet@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
