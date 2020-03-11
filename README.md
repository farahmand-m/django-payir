# Django Pay.ir

[![Build Status](https://travis-ci.org/farahmand-m/django-payir.svg?branch=master)](https://travis-ci.org/farahmand-m/django-payir)
[![PyPI version](https://badge.fury.io/py/django-payir.svg)](https://badge.fury.io/py/django-payir)

Django Pay.ir is a pluggable application that integrates Pay.ir services into your website. The application introduces 
two new models to your system that encapsulate Pay.ir API calls as object methods. Django Pay.ir has been tested on and 
supports:

- Python 3.7+
- Django 2.2.11 (Latest LTS Release)

# Getting Started

1.  Install the package:

    ```shell script
    pip install django-payir
    ```

2.  Add `payir` to your `INSTALLED_APPS` setting:

    ```python
    INSTALLED_APPS = [
        ...
        'payir',
    ]
    ```

3.  Run `python manage.py makemigrations` and `python manage.py migrate` to create the necessary models.
4.  Start a development server and visit http://127.0.0.1:8000/admin/payir/gateway to set up your gateways.

# Usage

## Database Models

The application consists of two models, encapsulating [Pay.ir](https://pay.ir)'s API.

### Transactions

Transaction models store the following attributes:

- `account`: A ForeignKey to the user account of the payer.
- `created`: Date and time of the creation of the object. 
- `modified`: Date and time of the latest modification of the object.
- `amount`: The amount of the transaction in IRR. 
- `description`: A short description for the transaction (can be 255 characters at most). 
- `gateway`: The gateway used to carry out the transaction.
- `token`: The token assigned to the transaction by [Pay.ir](https://pay.ir).
- `verified`: Whether the transaction has been verified with [Pay.ir](https://pay.ir) or not.
- `verified_at`: Date and time of the verification of the transaction with [Pay.ir](https://pay.ir). 

### Gateways

Gateway objects contain three attributes, `label`, `api_key`, and `default_callback` which are an arbitrary label for 
the gateway, the API Key assigned to you in [Pay.ir](https://pay.ir), and the pathname for a view that verifies the 
transactions with [Pay.ir](https://pay.ir). The callback view can be overridden with each transaction: 

Gateways come with the following methods:

-   Submission Method

    ```python
    submit(request, transaction, mobile=None, valid_card_number=None, callback=None)
    ```
    
    The method submits the necessary information to [Pay.ir](https://pay.ir) in order to acquire a token for the 
    transaction. If successful, the transaction object will be updated with the token and method will return a 
    HttpResponseRedirect which can be used to redirect the user to the gateway. Otherwise, a GatewayError exception will
    be raised, containing the `error_code` and `error_message` reported by [Pay.ir](https://pay.ir).
    
    - `request`: The WSGIRequest object passed to the view.
    - `transaction`: A transaction object which will be used to save the received token.
    - `mobile`: A phone number which will be used to list the payer's saved card numbers in the gateway.
    - `valid_card_number`: If defined, the specified card is the only one that can be used to complete the transaction.
    - `callback`: The argument can be used to override the default callback specified for the gateway.

    Gateway objects also have another method, named `create_and_submit` which create the transaction object on their 
    own. You need to pass the account of the payer and the amount of the transaction to the method instead of the
    transaction argument.

-   Verification Method

    ```python
    find_and_verify(token)
    ```

    After the successful completion of a transaction, [Pay.ir](https://pay.ir) will redirect the user to the view you've 
    set as the callback. The view will receive two GET headers, `status` and `token`. Status will be `'1'` if the 
    transaction went through successfully, and contain `'0'` if it failed. The callback view must verify the transaction 
    with [Pay.ir](https://pay.ir) or else, the money will be returned to the payer's bank account in 30 minutes. Gateway
    objects have another method, `verify(transaction)`, which can be used if you've already queried the transaction 
    object based on the `token`.
    
    Both methods return two values, first one being the updated transaction object, and the second, a boolean flag which
    will be `True` only if the transaction was successfully verified with [Pay.ir](https://pay.ir) for the first time.
    If the `verified` attribute on the Transaction object and the returned boolean flag don't match, the user might be
    trying to visiting the redirected page for a second time.

## Django Admin

The application registers both models in the Admin Panel with customized structures. You can modify the said structures
by editing the `ModelAdmin`s implemented in the `admin.py` of the app. 

## Exceptions

All errors returned by the Pay.ir API will be raised as a `Gateway Error` which is a subclass of the `RuntimeError` 
class. The exceptions have two attributes, `error_code` and `error_message` which correspond to the values by the same
name returned by [Pay.ir](https://pay.ir) in case of a failure. The complete list of the possible errors can be found 
[here](https://docs.pay.ir/gateway/).

