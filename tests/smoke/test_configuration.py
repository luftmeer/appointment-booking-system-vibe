from importlib import import_module

from django.conf import settings


def test_django_configuration_imports() -> None:
    url_configuration = import_module(settings.ROOT_URLCONF)

    assert settings.ROOT_URLCONF == "config.urls"
    assert url_configuration.__name__ == settings.ROOT_URLCONF
