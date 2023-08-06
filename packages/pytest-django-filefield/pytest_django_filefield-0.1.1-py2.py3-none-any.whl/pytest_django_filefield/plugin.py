import pytest


@pytest.hookimpl(hookwrapper=True)
def pytest_load_initial_conftests(early_config, parser, args):
    try:
        from django.db import models
    except ImportError:
        pass
    else:

        class PatchableStorageFileField(models.FileField):
            @property  # type: ignore
            def storage(self):
                return self._storage

            @storage.setter
            def storage(self, value):
                self._storage = value

        models.FileField = PatchableStorageFileField

    yield
