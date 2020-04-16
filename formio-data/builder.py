# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import json
import logging

import components


class Builder:

    def __init__(self, schema_json, lang='en', **kwargs):
        """
        @param schema_json
        @param lang
        """
        self.schema = json.loads(schema_json)

        self.lang = lang
        self.context = None
        if kwargs.get('context', False):
            self._context(kwargs['context'])

        self.components = {}
        self.set_components()

        # TODO kwargs['component_cls']
        # Custom component classes
        self._component_cls = []

    def set_components(self):
        root_components = self.schema.get('components')
        if root_components:
            self.components = self.load_components(root_components)

    def load_components(self, components, cons={}):
        for comp in components:
            if comp.get('key'):
                cons[comp['key']] = self.get_component_object(comp)
                if comp.get('components'):
                    self.load_components(comp.get('components'), cons)
            elif comp.get('type') == 'columns':
                # TODO Check more type (cases) needed here.
                for col in comp.get('columns'):
                    self.load_components(col.get('components'), cons)
        return cons

    def get_component_object(self, comp):
        comp_type = comp.get('type')
        if comp_type:
            try:
                cls_name = '%sComponent' % comp_type
                cls = getattr(components, cls_name)
                return cls(comp)
            except AttributeError as e:
                # TODO try to find/load first from self._component_cls else
                # re-raise exception or silence (log error and return False)
                logging.error(e)
                return components.Component(comp)
        else:
            return False
