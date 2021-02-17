# formio-data (Python)

Form.io (JSON) data API for Python.

For information about Form.io, see [Form.io homepage](https://www.form.io)

## Introduction

**python-formio-data** is a Python package, which loads and transforms
Form.io **Builder JSON** and **Form JSON** into **usable Python objects**.  It's main
aim is to provide easy access to a Form its components/fields, also
captured as **Python objects**, which makes this API very versatile and usable.

**Notes about terms:**
  - "Builder" could be read/seen as "Builder Form"
  - "Form" could be read/seen as "Form"
  - "Component" could be read/seen as "Field"

## Features

  - Compatible with Python 3.3 and later
  - Constructor of the **Builder** and **Form** class, only requires
    the JSON and an optional language code for translations.
  - Get a Form object its Components/Fields as a usable object e.g. DateTime, Boolean, Dict (for select component) etc.
  - Open source (MIT License)

## Installation

The source code is currently hosted on GitHub at:
https://github.com/novacode-nl/python-formio-data

**PyPI - Python Package Index**

Binary installers for the latest released version are available at the [Python
Package Index](https://pypi.python.org/pypi/formio-data)

```sh
pip(3) install formio-data
```

**Source Install**

Convenient for developers. Also useful for running the (unit)tests.

```sh
git clone git@github.com:novacode-nl/python-formio-data.git
pip(3) install -U -e python-formio-data
```

## License
[MIT](LICENSE)

## Contributing
All contributions, bug reports, bug fixes, documentation improvements, enhancements and ideas are welcome.

## Usage examples

For more examples of usage, see the unit-tests.

``` python
>> from formiodata import Builder, Form
>>
# builder_json is a Form.io Builder JSON document (text/string)
# form_json is a Form.io Form JSON document (text/string)
>>
>> builder = Builder(builder_json)
>> form = Form(builder, form_json)

# Text Field (control)
>> print(form.data.firstname.label)
'First Name'

# Value as Python string too
>> print(form.data.firstname.value)
'Bob'

# Date (control)
>> print(form.data.birthday.label)
'Birthday'

# Value as Python Date object
>> print(form.data.birthday.value)
datetime.date(2009 10 16)
```

## Unit tests

**Notes:**
- Internet access is required for running the
  `filecStorageUrlComponentTestCase`. It tests the URL Storage (type).

### Run all unittests

From toplevel directory:

```
python(3) -m unittest
```

### Run component unittests

```
python(3) -m unittest tests/test_*.py
```
