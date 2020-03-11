# Django Pay.ir

Django Pay.ir is a pluggable application that integrates Pay.ir services into your website. The application introduces 
two new models to your system that encapsulate Pay.ir API calls as object methods. Django Pay.ir has been tested on and 
supports:

- Python 3.7+
- Django 2.2.11 (Latest LTS Release)

# Quick Start

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

# Documentation

Visit the development documentations at https://github.com/farahmand-m/django-payir/wiki.
