# formio-data (Python)

formio.js (JSON Form Builder) data API for Python.

For information about the formio.js project, see https://github.com/formio/formio.js

## Introduction

**python-formio-data** is a Python package, which loads and transforms
formio.js **Builder JSON** and **Form JSON** into **usable Python objects**.  It's main
aim is to provide easy access to a Form its components/fields, also
captured as **Python objects**, which makes this API very versatile and usable.

**Notes about terms:**
  - **Builder:** The Form Builder which is the design/blueprint of a Form.
  - **Form:** A filled-in Form, aka Form submission.
  - **Component:** Input (field) or layout component in the Form Builder and Form.

## Features

  - Compatible with Python 3.3 and later
  - Constructor of the **Builder** and **Form** class, only requires
    the JSON and an optional language code for translations.
  - Get a Form object its Components as a usable object e.g. datetime, boolean, dict (for select component) etc.
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

### Optional dependencies

To support conditional visibility using JSON logic, you can install
the `json-logic-qubit` package (the `json-logic` package it is forked
off of is currently unmaintained).  It's also possible to install it
via the pip feature `json_logic` like so:

```sh
pip(3) install -U formio-data[json_logic]
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
# builder_json is a formio.js Builder JSON document (text/string)
# form_json is a formio.js Form JSON document (text/string)
>>
>> builder = Builder(builder_json)
>> form = Form(builder, form_json)

##################
# input components
##################

# textfield label
>> print(form.input_components['firstname'].label)
'First Name'

# textfield value
>> print(form.input_components['firstname'].value)
'Bob'

# datetime label
>> print(form.input_components['birthday'].label)
'Birthday'

# datetime value
>> print(form.input_components['birthday'].value)
datetime.date(2009 10 16)

# datagrid (rows property)
>> print(form.input_components['datagridMeasurements'].rows)
[
  {'measurementDatetime': <datetimeComponent>, 'measurementFahrenheit': <numberComponent>}, 
  {'measurementDatetime': <datetimeComponent>, 'measurementFahrenheit': <numberComponent>}
]

>> for row in form.input_components['datagridMeasurements'].rows:
>>    dtime = row['measurementDatetime']
>>    fahrenheit = row['measurementFahrenheit']
>>    print(%s: %s, %s: %s' % (dt.label, dt.value, fahrenheit.label, fahrenheit.value))

Datetime: datetime.datetime(2021, 5, 8, 11, 39, 0, 296487), Fahrenheit: 122
Datetime: datetime.datetime(2021, 5, 8, 11, 41, 5, 919943), Fahrenheit: 131

# alternative example, by getattr
>> print(form.data.firstname.label)
'First Name'

>> print(form.data.firstname.value)
'Bob'

#################################
# components (layout, input etc.)
#################################

# columns
>> print(form.components['addressColumns'])
<columnsComponent>

>> print(form.components['addressColumns'].rows)
[ 
  {'firstName': <textfieldComponent>, 'lastName: <textfieldComponent>}, 
  {'email': <emailComponent>, 'companyName: <textfieldComponent>}
]
```

## Unit tests

**Note:**

Internet access is recommended for running the `filecStorageUrlComponentTestCase`, because this also tests the URL Storage (type).\
If no internet access, this test won't fail and a WARNING shall be logged regarding a ConnectionError.

### Run all unittests

From toplevel directory:

```
python(3) -m unittest
```

### Run all component unittests

```
python(3) -m unittest tests/test_nested_components.py
```

### Run specific component unittest

```
python3 -m unittest tests.test_component_day.dayComponentTestCase.test_get_form_dayMonthYear
```
