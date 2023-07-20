# Changelog

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
