# -*- coding: utf-8 -*-
# Copyright 2018 Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import json


class Builder:

    def __init__(self, schema_str, lang='en', **kwargs):
        self.schema_str = schema_str
        self.schema = json.loads(schema_str)

        self.lang = lang
        self.context = None
        if kwargs.get('context', False):
            self._context(kwargs['context'])

        self.components = {}
        self.set_components()

    def set_components(self):
        root_components = self.schema.get('components')
        if root_components:
            self.components = self.extract_components(root_components)

    def extract_components(self, components, cons={}):
        for comp in components:
            if comp.get('key'):
                cons[comp['key']] = {
                    'raw': comp,
                    'component': self.get_component_object(comp)
                }

                if comp.get('components'):
                    self.extract_components(comp.get('components'), cons)
            elif comp.get('type') == 'columns':
                # TODO Check more type (cases) needed here.
                for col in comp.get('columns'):
                    self.extract_components(col.get('components'), cons)
        return cons

    def get_component_object(self, comp):
        return comp
