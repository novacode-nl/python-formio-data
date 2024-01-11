# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import json
import logging
import re

from collections import defaultdict, OrderedDict

from formiodata.builder import Builder


class Form:

    def __init__(
        self,
        form_json,
        builder=None,
        builder_schema_json=None,
        lang="en",
        component_class_mapping={},
        **kwargs
    ):
        """
        @param form_json
        @param builder Builder
        @param builder_schema_json
        @param lang
        """
        if isinstance(form_json, dict):
            self.form = form_json
        else:
            self.form = json.loads(form_json)

        self.builder = builder
        self.builder_schema_json = builder_schema_json
        self.lang = lang
        self.component_class_mapping = component_class_mapping

        if self.builder and self.builder_schema_json:
            raise Exception("Constructor accepts either builder or builder_schema_json.")

        if self.builder:
            assert isinstance(self.builder, Builder)
        elif self.builder_schema_json:
            assert isinstance(self.builder_schema_json, str)
        else:
            raise Exception("Provide either the argument: builder or builder_schema_json.")

        if self.builder is None and self.builder_schema_json:
            self.set_builder_by_builder_schema_json()

        # defaults to English (en) date/time format
        self.date_format = kwargs.get('date_format', '%m/%d/%Y')
        self.time_format = kwargs.get('time_format', '%H:%M:%S')

        self.input_components = {}

        self.components = OrderedDict()
        self.component_ids = {}

        self.load_components()
        self._input = self._data = FormInput(self)

    def set_builder_by_builder_schema_json(self):
        self.builder = Builder(
            self.builder_schema_json,
            language=self.lang,
            component_class_mapping=self.component_class_mapping
        )

    def load_components(self):
        for key, component in self.builder.components.items():
            # New object, don't affect the Builder component
            component_obj = self.builder.get_component_object(component.raw)
            component_obj.load(
                component_owner=self,
                parent=None,
                data=self.form,
                all_data=self.form,
                is_form=True,
            )
            self.components[key] = component_obj
            self.component_ids[component_obj.id] = component_obj

    @property
    def input(self):
        return self._input

    @property
    def data(self):
        logging.warning('DEPRECATION WARNING: data attr/property shall be deleted in a future version.')
        return self._data

    def get_component_by_path(self, component_path):
        """
        Get component object by path

        (Eg provided by the Formio.js JS/API).
        Especially handy for data Components eg datagridComponent.

        Example path:
        dataGrid[0].lastname => lastname in the first row [0] of a datagrid

        # Example path_nodes:
        # dataGrid[0].lastname => ['dataGrid[0]', 'lastname']

        @param component_path: the Formio.js JS/API path
        @return component: a Component object
        """
        path_nodes = component_path.split('.')
        # Example path_nodes:
        # dataGrid[0].lastname => ['dataGrid[0]', 'lastname']
        components = self.input_components
        for path_node in path_nodes:
            # eg: regex search '[0]' in 'dataGrid[0]'
            m = re.search(r"\[([A-Za-z0-9_]+)\]", path_node)
            if m:
                idx_notation = m.group(0)  # eg: '[0]', '[1]', etc
                idx = int(m.group(1))  # eg: 0, 1, etc
                key = path_node.replace(idx_notation, '')
                component = components[key]
                if hasattr(component, 'rows'):
                    components = component.rows[idx].input_components
            else:
                component = components[path_node]
        return component

    def validation_errors(self):
        """
        @return errors dict: Dictionary where key is component key and
            value is a Dictionary with errors.
        """
        errors = defaultdict(dict)
        for component_key, component in self.input_components.items():
            component_errors = component.validation_errors()
            if isinstance(component_errors, dict):
                for error_type, val in component_errors.items():
                    vals = {error_type: val}
                    errors[component_key].update(vals)
            elif isinstance(component_errors, list):
                errors[component_key] = component_errors
        return errors

    def render_components(self, force=False):
        for key, component in self.input_components.items():
            if force or component.html_component == "":
                if component.is_visible:
                    component.render()
                else:
                    component.html_component = ""


class FormInput:

    def __init__(self, form):
        self._form = form

    def __getattr__(self, key):
        return self._form.input_components.get(key)
