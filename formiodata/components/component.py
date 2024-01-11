# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import json
import uuid
import logging

from collections import OrderedDict


logger = logging.getLogger(__name__)


class Component:

    _none_value = None

    def __init__(self, raw, builder, **kwargs):
        self.raw = raw
        self.builder = builder

        self._parent = None
        self._component_owner = None
        # components can also be seen as children
        self.components = OrderedDict()

        # List of complete path components. This includes layout
        # components.
        self.builder_path = []
        # includes input components, so no layout components.
        self.builder_input_path = []

        # XXX uuid to ensure (hope this won't break anything)
        self.id = self.raw.get('id', str(uuid.uuid4()))

        # submission at this level {key: value, ...}
        # This includes a pseudo 'value' key which always encodes the current
        # component's value.  NOTE: This should be refactored away for conditionals
        # to work 100% correct when there's another element with a "value" key.
        self.form = {}
        # Full raw data from the root on up {key: value, ...}
        self._all_data = {}

        # i18n (language, translations)
        self.language = kwargs.get('language', 'en')
        self.i18n = kwargs.get('i18n', {})
        self.resources = kwargs.get('resources', {})
        if self.resources and isinstance(self.resources, str):
            self.resources = json.loads(self.resources)
        self.html_component = ""
        self.defaultValue = self.raw.get('defaultValue')

    def load(self, component_owner, parent=None, data=None, all_data=None, is_form=False):
        self.component_owner = component_owner

        if parent:
            self.parent = parent

        self._all_data = all_data
        self.load_data(data, is_form=is_form)

        self.builder.component_ids[self.id] = self

        # path
        self.set_builder_paths()
        builder_path_keys = [p.key for p in self.builder_path]
        builder_path_key = '.'.join(builder_path_keys)
        self.builder.components_path_key[builder_path_key] = self

    def load_data(self, data, is_form=False):
        if self.input and data:
            try:
                self.value = data[self.key]
                self.raw_value = data[self.key]
            except KeyError:
                # NOTE: getter will read out defaultValue if it's missing in self.form
                # TODO: Is this the right approach?
                pass

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id=False):
        if not id:
            id = str(uuid.uuid4())
        self._id = id

    @property
    def key(self):
        return self.raw.get('key')

    @property
    def type(self):
        return self.raw.get('type')

    @property
    def input(self):
        return self.raw.get('input')

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        if parent:
            self._parent = parent
            self._parent.components[self.key] = self

    @property
    def is_form_component(self):
        return bool(self.input)

    @property
    def component_owner(self):
        """The component's "owner".  This is usually the Builder class which
        created it.  But if this component is inside a datagrid
        component which may clone the form element, then the datagrid
        is the owner.  Each component adds itself to the `input_components`
        property its owner.
        """
        return self._component_owner

    @component_owner.setter
    def component_owner(self, component_owner):
        self._component_owner = component_owner
        if self.is_form_component:
            self._component_owner.input_components[self.key] = self

    @property
    def child_component_owner(self):
        """The owner object for child components, to use in the recursion"""
        return self.component_owner

    @property
    def builder_path_key(self):
        return [p.key for p in self.builder_path]

    @property
    def builder_path_label(self):
        return [p.label for p in self.builder_path]

    @property
    def builder_input_path_key(self):
        return [p.key for p in self.builder_input_path]

    @property
    def builder_input_path_label(self):
        return [p.label for p in self.builder_input_path]

    def set_builder_paths(self):
        builder_path = [self]
        builder_input_path = []
        if self.is_form_component:
            if self.builder.load_path_objects:
                builder_input_path.append(self)
        parent = self.parent
        while parent:
            if hasattr(parent, 'key'):
                if self.builder.load_path_objects:
                    builder_path.append(parent)
                if parent.is_form_component:
                    if self.builder.load_path_objects:
                        builder_input_path.append(parent)
                parent = parent.parent
            elif parent.__class__.__name__ == 'gridRow':
                parent = parent.grid
            else:
                parent = parent.component_owner
        builder_path.reverse()
        self.builder_path = builder_path
        # input path
        builder_input_path.reverse()
        self.builder_input_path = builder_input_path

    @property
    def validate(self):
        return self.raw.get('validate')

    @property
    def required(self):
        return self.raw.get('validate', {}).get('required')

    @property
    def properties(self):
        return self.raw.get('properties')

    @property
    def clearOnHide(self):
        if 'clearOnHide' in self.raw:
            return self.raw.get('clearOnHide')
        else:
            return None

    @property
    def label(self):
        label = self.raw.get('label')
        if self.i18n.get(self.language):
            return self.i18n[self.language].get(label, label)
        else:
            return label

    @label.setter
    def label(self, value):
        if self.raw.get('label'):
            self.raw['label'] = value

    @property
    def value(self):
        if self.clearOnHide is not None and not self.clearOnHide:
            default = self.defaultValue
        else:
            default = self._none_value
        return self.form.get('value', default)

    @value.setter
    def value(self, value):
        self.set_value(value)

    def _set_value(self, value):
        self.form['value'] = self._encode_value(value)

    @property
    def raw_value(self):
        return self.form['raw_value']

    @raw_value.setter
    def raw_value(self, value):
        self._set_raw_value(value)

    def _set_raw_value(self, value):
        self.form['raw_value'] = value

    def set_value(self, value):
        """ Set raw_value and value at once! """
        self._set_raw_value(value)
        self._set_value(value)

    @property
    def hidden(self):
        return self.raw.get('hidden')

    @property
    def tableView(self):
        return self.raw.get('tableView')

    @property
    def disabled(self):
        return self.raw.get('disabled')

    @property
    def conditional(self):
        return self.raw.get('conditional')

    @property
    def customConditional(self):
        return self.raw.get('customConditional')

    @property
    def templates(self):
        return self.raw.get('templates')

    @property
    def logic(self):
        return self.raw.get('logic')

    def _encode_value(self, value):
        return value

    def render(self):
        if self.value is not None:
            self.html_component = '<p>%s</p>' % self.value

    @property
    def conditionally_visible(self):
        """
        If conditional visibility applies, evaluate to see if it is visible.
        Note that the component can also be hidden, which is a separate concept.

        IMPORTANT
        =========
        Currently JSONLogic (json) precedes the Simple (when).
        This causes backward compatibility issues when changing the priority order.
        """
        try:
            cond = self.raw['conditional']
            if cond.get('json'):
                return self.conditional_visible_json_logic()
            elif cond.get('when'):
                return self.conditional_visible_when()
        except KeyError:
            # Unknown component or no 'when', 'eq' or 'show' property
            pass

        # By default, it's visible
        return True

    def conditional_visible_when(self):
        cond = self.raw['conditional']
        triggering_component = self.component_owner.input_components[cond['when']]
        triggering_value = cond['eq']
        if triggering_component.value == triggering_value:
            return cond['show']
        else:
            return not cond['show']

    def conditional_visible_json_logic(self):
        # Optional package
        try:
            from json_logic import jsonLogic
            context = {'data': self._all_data}
            try:
                context['row'] = self.component_owner.row
            except AttributeError:
                pass  # only datagrid rows have a "row" attribute
            cond = self.raw['conditional']
            return jsonLogic(cond['json'], context)
        except ImportError:
            logger.warning(f'Could not load json logic extension; will not evaluate visibility of {self.__class__.__name__} {self.id} ("{self.key}")')
            return True

    @property
    def is_visible(self):
        conditional = self.raw.get('conditional')
        if conditional and (conditional.get('json') or conditional.get('when')):
            # Not implement (JavaScript):
            # conditional_show = self.raw.get('show')
            return self.conditionally_visible
        else:
            return not self.hidden

    def validation_errors(self):
        errors = {}
        if self.required and not self.value:
            msg_tmpl = '{{field}} is required'
            if self.i18n.get(self.language):
                msg_tmpl = self.i18n[self.language].get(msg_tmpl, msg_tmpl)
            errors['required'] = msg_tmpl.replace('{{field}}', self.label)
        return errors
