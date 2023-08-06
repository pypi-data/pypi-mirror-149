# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['peachpayments_partner_marshmallow']

package_data = \
{'': ['*']}

install_requires = \
['iso4217>=1.6.20180829,<2.0.0',
 'marshmallow==3.13.0',
 'peachpayments-partner>=0.1.7,<0.2.0']

setup_kwargs = {
    'name': 'peachpayments-partner-marshmallow',
    'version': '0.2.4',
    'description': 'PeachPayments Partner Marshmallow library contains Marshmallow schemas to help integrate PeachPayments with their partners.',
    'long_description': '# PeachPayments Partner Marshmallow Library\n\n## Overview\n\n**PeachPayments Partner Marshmallow Library** is a platform-agnostic Python package to help Payment Service Providers in integrating with PeachPayments. This library provides functionality to validate request and response data using Marshmallow Python library.\n\n\n**Source Code**: https://gitlab.com/peachpayments/peach-partner-marshmallow/\n\n---\n### Key terms\n|   Term\t                    |   Definition\t|\n|---------------------------- |--------------\t|\n|   Partner API\t\t            |   A service provided by Peach Payments to enable Payment Service Providers to become available on the Peach Platform |\n|   Payment Service Provider\t|   A payment service provider who integrates with the Partner API\t|\n|   Outbound API call\t        |   API calls sent from Partner API to the Payment Service Provider  |\n|   Inbound API call\t\t      |   API calls sent from Payment Service Provider to Partner API    |\n\n\n## Usage\nPackage requires Python 3.9+\n\n### Installation\n```sh\n# pip\n$ pip3 install peachpayments-partner-marshmallow\n```\n```sh\n# poetry\n$ poetry add peachpayments-partner-marshmallow\n```\n\n### Field validation\n\nPayment Service Provider receives a debit request from PeachPayments.\n\n```python\n# ... imports\nfrom peachpayments_partner_marshmallow.validator import validate_debit_request, validate_debit_response\n\n\ndef debit(db: Session, data: dict):\n    request_validation = validate_debit_request(data)\n    if not request_validation["valid"]:\n        raise HttpJSONError(request_validation["response"])\n\n    # Store a transaction in a database\n    # Prepare the response to PeachPayments in the `response_fields` dictionary\n\n    response_validation = validate_debit_response(response_fields)\n    if not response_validation["valid"]:\n        raise Exception("Badly formatted response fields")\n\n    return HttpResponse(response_fields)\n```\n',
    'author': 'PeachPayments',
    'author_email': 'support@peachpayments.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/peachpayments/peachpayments-partner-marshmallow/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
