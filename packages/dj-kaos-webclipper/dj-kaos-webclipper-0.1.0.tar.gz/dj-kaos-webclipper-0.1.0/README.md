# Django KAOS web clipper

Clip web pages html and store in Django

## Quick start

    pip install dj-kaos-webclipper

Add `webclipper` to `INSTALLED_APPS` if you want to use the generic webclip model, or extend `AbstractWebClip` if you
want to customize it on your application.

If you go with the generic WebClip model, you can get REST endpoint by using the router defined in `rest.routes`.

Your end users will send the title, URL and HTML content of the page using the REST API endpoint, and they get saved to
the models. You can extend the WebClip model in a proxy model, and extend `RawItemMixin` from the library, which gives
you an interface to parse the page using Scrapy's API.

## Development and Testing

### IDE Setup

Add the `example` directory to the `PYTHONPATH` in your IDE to avoid seeing import warnings in the `tests` modules. If
you are using PyCharm, this is already set up.

### Running the Tests

Install requirements

```
pip install -r requirements.txt
```

For local environment

```
pytest
```

For all supported environments

```
tox
```
