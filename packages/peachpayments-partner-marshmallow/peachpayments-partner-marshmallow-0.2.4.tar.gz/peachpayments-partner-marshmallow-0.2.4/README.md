# PeachPayments Partner Marshmallow Library

## Overview

**PeachPayments Partner Marshmallow Library** is a platform-agnostic Python package to help Payment Service Providers in integrating with PeachPayments. This library provides functionality to validate request and response data using Marshmallow Python library.


**Source Code**: https://gitlab.com/peachpayments/peach-partner-marshmallow/

---
### Key terms
|   Term	                    |   Definition	|
|---------------------------- |--------------	|
|   Partner API		            |   A service provided by Peach Payments to enable Payment Service Providers to become available on the Peach Platform |
|   Payment Service Provider	|   A payment service provider who integrates with the Partner API	|
|   Outbound API call	        |   API calls sent from Partner API to the Payment Service Provider  |
|   Inbound API call		      |   API calls sent from Payment Service Provider to Partner API    |


## Usage
Package requires Python 3.9+

### Installation
```sh
# pip
$ pip3 install peachpayments-partner-marshmallow
```
```sh
# poetry
$ poetry add peachpayments-partner-marshmallow
```

### Field validation

Payment Service Provider receives a debit request from PeachPayments.

```python
# ... imports
from peachpayments_partner_marshmallow.validator import validate_debit_request, validate_debit_response


def debit(db: Session, data: dict):
    request_validation = validate_debit_request(data)
    if not request_validation["valid"]:
        raise HttpJSONError(request_validation["response"])

    # Store a transaction in a database
    # Prepare the response to PeachPayments in the `response_fields` dictionary

    response_validation = validate_debit_response(response_fields)
    if not response_validation["valid"]:
        raise Exception("Badly formatted response fields")

    return HttpResponse(response_fields)
```
