# Changelog

## 1.0.0

Implement component (object) path properties in a builder (object) context.

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
