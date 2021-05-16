# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import json
import logging
import uuid

from collections import OrderedDict
from copy import deepcopy

from formiodata import components


class Builder:

    def __init__(self, schema_json, **kwargs):
        """
        @param schema_json
        @param lang
        """
        if isinstance(schema_json, dict):
            self.schema = schema_json
        else:
            self.schema = json.loads(schema_json)

        self.language = kwargs.get('language', 'en')
        # i18n (translations)
        self.i18n = kwargs.get('i18n', {})
        self.resources = kwargs.get('resources', {})

        # Raw components from the schema
        self._raw_components = []

        # Raw components enriched with Component(object) API.
        self.raw_components = []

        # Key/value dictionay of all components for instant access.
        self.components = OrderedDict()
        self.component_ids = {}

        # Key/value dictionay of Form input-only components (i.e., no layout components) for instant access.
        self.input_components = {}

        # Set/load component attrs intialized above.
        self.load_components()

        # TODO kwargs['component_cls']
        # Custom component classes
        self._component_cls = []

    def load_components(self):
        self._raw_components = self.schema.get('components')
        self.raw_components = deepcopy(self.schema.get('components'))
        if self.raw_components:
            self._load_components(self.raw_components)

    def _load_components(self, components, parent=None):
        """
        @param components
        """
        for component in components:
            # Only determine and load class if component type.
            if 'type' in component:
                component_obj = self.get_component_object(component)
                # start and traverse from toplevel
                component_obj.load(component_owner=self, parent=None, data=None)
                self.components[component_obj.key] = component_obj

    def get_component_object(self, component):
        """
        @param component
        """
        component_type = component.get('type')
        if component_type:
            try:
                cls_name = '%sComponent' % component_type
                cls = getattr(components, cls_name)
                component_obj = cls(component, self, language=self.language, i18n=self.i18n, resources=self.resources)
                return component_obj
            except AttributeError as e:
                # TODO try to find/load first from self._component_cls else
                # re-raise exception or silence (log error and return False)
                logging.error(e)
                # TODO: implement property (by kwargs) whether to return
                # (raw) Component object or throw exception,
                return components.Component(component, self)
        else:
            msg = "Can't instantiate a (raw) component without a type.\n\n" \
                "Component raw data\n" \
                "==================\n" \
                "%s\n"
            logging.warning(msg % component)
            return False


    @property
    def form(self):
        """
        Placeholder form dict, always empty.  Useful in contexts where the component owner's form
        is requested because there is a need for form data.
        """
        return {}
