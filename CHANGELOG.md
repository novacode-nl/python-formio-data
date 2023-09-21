# Changelog

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
