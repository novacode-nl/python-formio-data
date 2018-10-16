# -*- coding: utf-8 -*-
# Copyright 2018 Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import json

from builder import Builder


class Form:

    def __init__(self, submission, builder=None, builder_schema_str=None, lang='en'):
        """
        @param submission_schema_str
        @param builder Builder
        @param builder_schema_str
        """
        self.submission_str = submission_str
        self.submission = json.loads(submission_str)
        
        self.builder = builder
        self.builder_schema_str = builder_schema_str
        self.lang = lang

        if self.builder and self.builder_schema_str:
            raise Exception("Constructor accepts either builder or builder_schema.")

        if self.builder:
            assert isinstance(self.builder, Builder)
        elif self.builder_schema_str:
            assert isinstance(self.builder_schema_str, basestring)
        else:
            raise Exception("Provide either the argument: builder or builder_schema_str.")

        if self.builder is None and self.builder_schema_str:
            self.set_builder_by_builder_schema()

        self.components = {}
        self.init_components()

    def set_builder_by_builder_schema_str(self):
        self.builder = Builder(self.builder_schema_str, self.lang)

    def init_components(self):
        for key, component in self.builder.components.items():
            # Rather lazy check, but sane.
            if not self.submission.get(key):
                continue
            
            component_submission = self.submission.get(key)

            # Instantiate the compoent class
            component_class = globals()[component.__class__.__name__]
            component_obj = component_class(self.builder, component_submission)

            if component_obj is not None:
                component_obj.init_submission_attrs(component_submission)
                self.components[key] = component_obj


class Submission:

    def __init__(self, form):
        self._form = form

    def _getattr__(self, key):
        if self._form.builder.components.get(key):
            return self._form.component.get(key)
        else:
            return None
