# Changelog

## 1.2.6

- Fix `datetimeComponent` value setter, to properyly parse when the
  `enableTime` property is `False`.\
  This fixes a bug/regression in version 1.2.3.
- Update README concerning the datetime component value.

## 1.2.5

Improve the load methods for components and `gridRow`, by passing
whether it applies to a Form `is_form`, otherwise it's obtained as a
Builder.

Ensure an empty form `gridRow` doesn't appear in a grid's `rows`
property, made possible by the other `is_form` change.

## 1.2.4

Implementation of "simple" validation required.

For a Form object the validation errors can be retrieved by the new
`validation_errors()` method.

The new component method `validation_errors()` can be extended and
returns either a dictionary or a list (for grid components) with the
validation errors.

## 1.2.3

Improve the `datetimeComponent` value setter, to properly parse a date
with a custom format, when the `enableTime` (new property) is `False`.

Provide the `component_class_mapping` (interface) in the keyword arguments of the Form (class) instantiation.

## 1.2.2

Refactored the `Component` class `conditionally_visible` method, to
call the following 2 methods which can be extended in component
subclasses:
- `conditional_visible_json_when`
- `conditional_visible_json_logic`

Implemented the `conditional_visible_json_when` method for the `selectboxesComponent`.\
Extended the unittest `ConditionalVisibilitySimpleTestCase` with simple conditional visibility for the `selectboxesComponent`.

## 1.2.1

Fix `get_component_object` (Builder) method to handle `ModuleNotFoundError`.\
Therefor implemented the `get_component_class` method to determine the class with a fallback to the base `Component` class.

## 1.2.0

New "component class mapping feature" for the Builder instantiation:\
Map a custom component type to an implemented component class, which is then loaded.

An example is available in the unittests of file: `tests/test_component_class_mapping.py`

Also refactored the Builder constructor, from some `kwargs` to keyword arguments.

## 1.1.0

Put component classes as files in the new `components` directory.\
Change the instantiation of a component in the `get_component_object` method of the `Builder` class.

**Warning**:

This changes the `import` declaration (path) of how components should be imported.

**Old style import:**:

```python
from formiodata.components import textfieldComponent
```

**New style import:**

```python
from formiodata.components.textfield import textfieldComponent
```

Also some additional minor improvements, e.g. remove unused imports and newlines.

## 1.0.5

Add Component properties:
- `tableView`: Display // Table View
- `disabled`: Display // Disabled

## 1.0.4

Add Component properties:
- `conditional`: Conditional // Simple Conditional
- `custom_conditional`: Conditional // Custom Conditional
- `templates`: Templates (eg templates for layout and (data) grids.)
- `logic`: Logic (trigger/action pairs).

## 1.0.3

Add the country_code property in the addressComponent.

## 1.0.2

Refactor builder component path properties, to store objects, with key and label getters.

## 1.0.1

Fix error in `get_component_object` (`builder.py`) => `NameError: name 'logging is not defined'`\
Accidentally removed the `import logging` in previous version 1.0.0

## 1.0.0

Implement builder component path properties (keys, labels).

`builder_path_key`
List of complete path components with keys. This includes layout components.

`builder_path_label`
List of complete path components with labels. This includes layout components.

`builder_input_path_key`
List of input components in path with keys. This only includes input components, so no layout components.

`builder_input_path_label`
List of input components in path with labels. This only includes input components, so no layout components.

Also propagate this as first official release 1.0.0

## 0.5.1

Fix `initEmpty` in `editgridComponent`, bug in previous version 0.5.0

## 0.5.0

Implement `initEmpty` in `editgridComponent`, which obtains a different key (`openWhenEmpty`) in the form builder schema.

## 0.4.11

Improvements:
- Add support for editGrid component (#33).
- Breaking change: in a dataGrid, renamed `gridRow` object's `datagrid` property to `grid`.
