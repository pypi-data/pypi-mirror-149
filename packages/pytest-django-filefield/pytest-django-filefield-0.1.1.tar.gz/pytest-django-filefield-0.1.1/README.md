pytest-django-filefield
=======================
Patch the storage of your models' `FileField`s effortlessly.  
Best served with `pytest-django` and your own fixtures.

Install and enable the plugin:
```bash
pip install pytest-django-filefield
```

Roll your fixture:
```python
# conftest.py
from django.core.files import storage
from django.db import models

@pytest.fixture
def fake_storage(monkeypatch, tmp_path) 
    storage = storage.FileSystemStorage(location=tmp_path)
    monkeypatch.setattr(models.FileField, "storage", storage)
    return storage
```
Have it scoped however you want, or just mark as `autouse=True` and forget about it.


This simple hack is packaged as a pytest plugin to make it work with `pytest-django`, because there is [no simpler way to inject custom code before it calls `django.setup()`](https://pytest-django.readthedocs.io/en/latest/configuring_django.html#changing-your-app-before-django-gets-set-up).


## Do I even need this?
There's a good chance that you don't! But let's first recap on some of the ways to patch the storage, given a model somewhat like below: 

```python
class Contract(models.Model):
    document = models.FileField(storage=DocumentStorage())
```

### Just patch the field
`storage` is an instance attribute of each `FileField`, so the most straightforward and robust way would be to just find the field instance and patch the attribute: 

```python
def test_document_upload(monkeypatch, my_fake_storage):
    document_field = Contract._meta.get_field_by_name("document")[0]
    monkeypatch.setattr(document_field, "storage", my_fake_storage)

    upload_contract_document()

    assert_results(my_fake_storage)
```

The requirement here is that you know which fields of which models should be patched, and make sure to get it right for corresponding tests. This could become quite noisy and/or tedious to maintain. However, the approach is beneficial if there is quite a number of different storages, especially different storages used within the same model.

If the project uses a single storage for everything, or just a handful of them, such flexibility might be overkill.

### Define a different storage for tests
Extract the name of the storage class into `settings.py`, use a different settings file for tests (which you should anyway) with a different value there. This way the storage is replaced before Django is even initialized.

```python
# settings.py
DOCUMENT_STORAGE = 'myapp.storages.DocumentStorage'

# settings_test.py
DOCUMENT_STORAGE = 'myapp.tests.storages.FakeDocumentStorage'
```

```python
# models.py
class Contract(models.Model):
    document = models.FileField(
        storage=import_string(settings.DOCUMENT_STORAGE)()
    )

# tests/test_contract.py
def test_document_upload():
    document_field = Contract._meta.get_field_by_name("document")[0]

    upload_contract_document()

    assert_results(document_field.storage)
```
Patching not required, each field still has its own instance of a test storage, but all the objects using that field share the same storage for the whole test session. Which is already good enough and you may just stop here!

### Patch all the storages, with configurable scope
This is what the plugin enables. It replaces `FileField().storage`, which is normally an instance attribute, with a property of the same name. A property is defined in a class, so this forces all the `"storage"` attribute lookups to be done on a class. You now don't have to hunt down every `FileField` instance and can just patch the class property instead.

The drawback is that any and all `FileField`s are patched for duration of the fixture's scope. Since the narrowest scope is `function`, this may (only) be a problem if a single test needs to check the behaviours of multiple storages in isolation.   

### Summary
As always, choose what works best for your specific project!

| | Manual patch | Storage from settings | This plugin |
|-|-|-|-|
| function-scoped storage      | x |   | x |
| field-scoped storage         | x |   |   |
| no model changes required    | x |   | x |
| low/no maintenance           |   | x | x |
