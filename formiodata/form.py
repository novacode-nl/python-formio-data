# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import json
import logging

from collections import OrderedDict
from copy import deepcopy

from formiodata.builder import Builder


class Form:

    def __init__(self, form_json, builder=None, builder_schema_json=None, lang='en', **kwargs):
        """
        @param form_json
        @param builder Builder
        @param builder_schema
        @param lang
        """
        if isinstance(form_json, dict):
            self.form = form_json
        else:
            self.form = json.loads(form_json)

        self.builder = builder
        self.builder_schema_json = builder_schema_json
        self.lang = lang

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
        self.builder = Builder(self.builder_schema_json, self.lang)

    def load_components(self):
        for key, component in self.builder.components.items():
            # New object, don't affect the Builder component
            component_obj = self.builder.get_component_object(component.raw)
            component_obj.load(component_owner=self, parent=None, data=self.form, all_data=self.form)
            self.components[key] = component_obj
            self.component_ids[component_obj.id] = component_obj

    @property
    def input(self):
        return self._input

    @property
    def data(self):
        logging.warning('DEPRECATION WARNING: data attr/property shall be deleted in a future version.')
        return self._data

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
