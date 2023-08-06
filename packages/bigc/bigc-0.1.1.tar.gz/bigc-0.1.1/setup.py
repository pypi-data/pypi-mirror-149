# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bigc', 'bigc.data', 'bigc.resources']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27,<3.0']

setup_kwargs = {
    'name': 'bigc',
    'version': '0.1.1',
    'description': 'Unofficial client for the BigCommerce API',
    'long_description': "# bigc\n\nAn unofficial Python client for the BigCommerce API.\n\n_This project is currently in an alpha state._\n\n## Installation\n\n```shell\npip install bigc \n```\n\n## Usage\n\nTo authenticate, you'll need the BigCommerce store's hash and an access token.\n\n```python\nfrom bigc import BigCommerceAPI\n\n\nstore_hash = '000000000'\naccess_token = '0000000000000000000000000000000'\nbigcommerce = BigCommerceAPI(store_hash, access_token)\n\norder: dict = bigcommerce.orders.get(101)\norders: list[dict] = list(bigcommerce.orders.all(customer_id=1))\n```\n\nThe following resources are currently supported:\n\n- `carts`\n- `customers`\n- `orders`\n- `products`\n- `product_variants`\n- `webhooks`\n\n### Utilities\n\nSome extra utility functions that don't interact with the BigCommerce API are available in `bigc.utils`.\n\n- `bigc.utils.parse_rfc2822_date`: Convert an RFC-2822 date (used by some BigCommerce APIs) to a `datetime`\n\n### Constants\n\nFor convenience, some constants are made available in `bigc.data`.\n\n- `bigc.data.BigCommerceOrderStatus`: An `Enum` of order statuses and their IDs\n",
    'author': 'Ryan Thomson',
    'author_email': 'ryan@medshift.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MedShift/bigc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
