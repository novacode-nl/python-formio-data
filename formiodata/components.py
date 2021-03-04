# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import json
import uuid

from collections import OrderedDict
from datetime import datetime

from formiodata.utils import base64_encode_url, decode_resource_template, fetch_dict_get_value


class Component:

    def __init__(self, raw, builder, **kwargs):
        # TODO or provide the Builder object?
        self.raw = raw
        self.builder = builder
        self._parent = None
        self.children = []

        # XXX uuid to ensure (hope this won't break anything)
        self.id = self.raw.get('id', str(uuid.uuid4()))

        # submission {key: value, ...}
        self.form = {}

        # i18n (language, translations)
        self.language = kwargs.get('language', 'en')
        self.i18n = kwargs.get('i18n', {})
        self.resources = kwargs.get('resources', {})
        if self.resources and isinstance(self.resources, str):
            self.resources = json.loads(self.resources)
        self.html_component = ""
        self.defaultValue = self.raw.get('defaultValue')

    def load_value(self, data):
        if self.input and data and data.get(self.key):
            self.value = data[self.key]

    def load(self, parent=None, data=None, renderer=None):
        if renderer:
            self.load_value(data)
            renderer.component_ids[self.id] = self

        if parent:
            self.parent = parent
            self.parent.children.append(self)

        # (Input) nested components (e.g. datagrid, editgrid)
        for component in self.raw.get('components', []):
            component_obj = self.builder.get_component_object(component)
            if not component_obj.id in self.builder.component_ids:
                self.builder.component_ids[component_obj.id] = component_obj
            component_obj.load(self, data, renderer)

        # (Layout) nested components (e.g. columns, panels)
        for k, vals in self.raw.copy().items():
            if isinstance(vals, list):
                for v in vals:
                    if 'components' in v:
                        for v_component in v['components']:
                            v_component_obj = self.builder.get_component_object(v_component)
                            v_component_obj.parent = self

                            if renderer and v_component_obj.id not in renderer.component_ids:
                                renderer.component_ids[v_component_obj.id] = v_component_obj
                                v_component_obj.load(self, data, renderer)
                            elif not renderer and v_component_obj.id not in self.builder.component_ids:
                                self.children.append(v_component_obj)
                                self.builder.component_ids[v_component_obj.id] = v_component_obj
                                v_component_obj.load(self, data, renderer)
                    elif isinstance(v, list):
                        # XXX still needed?
                        for sub_v in v:
                            if 'components' in sub_v:
                                self.load(sub_v.get('components'), self.raw)

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
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        if parent:
            self._parent = parent

    @property
    def type(self):
        return self.raw.get('type')

    @property
    def input(self):
        return self.raw.get('input')

    @property
    def valdidate(self):
        return self.raw.get('validate')

    @property
    def required(self):
        return self.raw.get('validate').get('required')

    @property
    def properties(self):
        return self.raw.get('properties')

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
        return self.form.get('value')

    @value.setter
    def value(self, value):
        self.form['value'] = self._encode_value(value)

    @property
    def raw_value(self):
        return self.form['raw_value']

    @raw_value.setter
    def raw_value(self, value):
        self.form['raw_value'] = value

    @property
    def hidden(self):
        return self.raw.get('hidden')

    def _encode_value(self, value):
        return value

    def render(self):
        self.html_component = '<p>%s</p>' % self.form.get('value')


# Basic

class textfieldComponent(Component):
    pass


class textareaComponent(Component):
    pass


class numberComponent(Component):
    pass


class passwordComponent(Component):
    pass


class checkboxComponent(Component):
    pass


class selectboxesComponent(Component):

    @property
    def values_labels(self):
        comp = self.builder.form_components.get(self.key)
        builder_values = comp.raw.get('values')
        values_labels = {}
        for b_val in builder_values:
            if self.value and b_val.get('value'):
                if self.i18n.get(self.language):
                    label = self.i18n[self.language].get(b_val['label'], b_val['label'])
                else:
                    label = b_val['label']
                val = {'key': b_val['value'], 'label': label, 'value': self.value.get(b_val['value'])}
                values_labels[b_val['value']] = val
        return values_labels


class selectComponent(Component):

    @property
    def multiple(self):
        return self.raw.get('multiple')

    @property
    def value_label(self):
        comp = self.builder.form_components.get(self.key)
        values = comp.raw.get('data') and comp.raw['data'].get('values')
        for val in values:
            if val['value'] == self.value:
                label = val['label']
                if self.i18n.get(self.language):
                    return self.i18n[self.language].get(label, label)
                else:
                    return label
        else:
            return False

    @property
    def value_labels(self):
        comp = self.builder.form_components.get(self.key)
        values = comp.raw.get('data') and comp.raw['data'].get('values')
        value_labels = []
        for val in values:
            if val['value'] in self.value:
                if self.i18n.get(self.language):
                    value_labels.append(self.i18n[self.language].get(val['label'], val['label']))
                else:
                    value_labels.append(val['label'])
        return value_labels


class radioComponent(Component):

    @property
    def values_labels(self):
        comp = self.builder.form_components.get(self.key)
        builder_values = comp.raw.get('values')
        values_labels = {}

        for b_val in builder_values:
            if self.i18n.get(self.language):
                label = self.i18n[self.language].get(b_val['label'], b_val['label'])
            else:
                label = b_val['label']
            val = {'key': b_val['value'], 'label': label, 'value': b_val['value'] == self.value}
            values_labels[b_val['value']] = val
        return values_labels

    @property
    def value_label(self):
        comp = self.builder.form_components.get(self.key)
        builder_values = comp.raw.get('values')
        value_label = {}

        for b_val in builder_values:
            if b_val['value'] == self.value:
                if self.i18n.get(self.language):
                    return self.i18n[self.language].get(b_val['label'], b_val['label'])
                else:
                    return b_val['label']
        else:
            return False


class buttonComponent(Component):

    def load_value(self, data):
        # just bypass this
        pass


# Advanced

class emailComponent(Component):
    pass


class urlComponent(Component):
    pass


class phoneNumberComponent(Component):
    pass


# TODO: tags, address


class datetimeComponent(Component):

    def _format_mappings(self):
        """
        Dictionary of mappings between Formio Datetime component
        (key) to Python format (value).

        Formio uses the format codes refererend in:
        https://github.com/angular-ui/bootstrap/tree/master/src/dateparser/docs#uibdateparsers-format-codes
        """
        return {
            'year': {'yyyy': '%Y', 'yy': '%y', 'y': '%y'},
            'month': {'MMMM': '%B', 'MMM': '%b', 'MM': '%m', 'M': '%-m'},
            'day': {'dd': '%d', 'd': '%-d'},
            'hour': {'HH': '%HH', 'H': '%-H', 'hh': '%I', 'h': '%-I'},
            'minute': {'mm': '%M', 'm': '%-M'},
            'second': {'ss': '%S', 's': '%-S'},
            'am_pm': {'a': '%p'}
        }

    def _fromisoformat(self, value):
        # Backport of Python 3.7 datetime.fromisoformat
        if hasattr(datetime, 'fromisoformat'):
            # Python >= 3.7
            return datetime.fromisoformat(value)
        else:
            # Python < 3.7
            # replaces the fromisoformat, not available in Python < 3.7
            #
            # XXX following:
            # - Raises: '2021-02-25T00:00:00+01:00' does not match format '%Y-%m-%dT%H:%M%z'
            # - Due to %z not obtaing the colon in '+1:00' (tz offset)
            # - More info: https://stackoverflow.com/questions/54268458/datetime-strptime-issue-with-a-timezone-offset-with-colons
            # fmt_str =  r"%Y-%m-%dT%H:%M:%S%z"
            # return datetime.strptime(value, fmt_str)
            #
            # REQUIREMENT (TODO document, setup dependency or try/except raise exception)
            # - pip install dateutil
            # - https://dateutil.readthedocs.io/
            from dateutil.parser import parse
            return parse(value)

    @property
    def value(self):
        return super().value

    @value.setter
    def value(self, value):
        """ Inherit property setter the right way, URLs:
        - https://gist.github.com/Susensio/979259559e2bebcd0273f1a95d7c1e79
        - https://stackoverflow.com/questions/35290540/understanding-property-decorator-and-inheritance
        """
        # TODO: to improve these transformations (mappings and loops)

        if not value:
            return value

        component = self.builder.components.get(self.key)
        dt = self._fromisoformat(value)
        py_dt_format = formio_dt_format = component.raw.get('format')
        mapping = self._format_mappings()

        # year
        done = False
        for formio, py in mapping['year'].items():
            if not done and formio in formio_dt_format:
                py_dt_format = py_dt_format.replace(formio, py)
                done = True

        # month
        done = False
        for formio, py in mapping['month'].items():
            if not done and formio in formio_dt_format:
                py_dt_format = py_dt_format.replace(formio, py)
                done = True

        #day
        done = False
        for formio, py in mapping['day'].items():
            if not done and formio in formio_dt_format:
                py_dt_format = py_dt_format.replace(formio, py)
                done = True

        # hour
        done = False
        for formio, py in mapping['hour'].items():
            if not done and formio in formio_dt_format:
                py_dt_format = py_dt_format.replace(formio, py)
                done = True

        # minute
        done = False
        for formio, py in mapping['minute'].items():
            if not done and formio in formio_dt_format:
                py_dt_format = py_dt_format.replace(formio, py)
                done = True

        # second
        done = False
        for formio, py in mapping['second'].items():
            if not done and formio in formio_dt_format:
                py_dt_format = py_dt_format.replace(formio, py)
                done = True

        # 12 hours AM/PM
        done = False
        for formio, py in mapping['am_pm'].items():
            if not done and formio in formio_dt_format:
                py_dt_format = py_dt_format.replace(formio, py)
                done = True

        val = dt.strftime(py_dt_format)
        super(self.__class__, self.__class__).value.fset(self, val)

    def to_datetime(self):
        if not self.raw_value:
            return None
        dt = self._fromisoformat(self.raw_value)
        return dt

    def to_date(self):
        if not self.raw_value:
            return None
        return self.to_datetime().date()


class timeComponent(Component):
    pass


class currencyComponent(Component):
    pass


class surveyComponent(Component):
    pass


class signatureComponent(Component):
    pass


# Layout components

class htmlelementComponent(Component):
    pass


class contentComponent(Component):
    pass


class layoutComponentBase(Component):

    def propagate_children(self, data=[]):
        # EXAMPLE data, e.g. of a columnComponent with data from components:
        # - email => textComponent
        # - typeOfEmail => selectComponent
        #
        # [{'email': 'personal@example.com'}, {'typeOfEmail': 'personal'}]

        new_layout_comp = self.builder.get_component_object(self.raw)

        for key_val in data:
            for key, val in key_val.items():
                for child in self.children:
                    if key == child.key:
                        raw = child.raw
                        new_comp = self.builder.get_component_object(raw)
                        new_comp.value = val
                        new_layout_comp.children.append(new_comp)
        return new_layout_comp


class columnsComponent(layoutComponentBase):

    @property
    def rows(self):
        rows = []

        row = []
        col_data = {'column': None, 'components': []}
        total_width = 0

        for col in self.raw['columns']:
            components = []

            for col_comp in col['components']:
                for child in self.children:
                    if col_comp['id'] == child.id:
                        components.append(child)

            if col['width'] >= 12:
                # add previous (loop) row
                if row:
                    rows.append(row)

                # init new row and add to rows
                row = [{'column': col, 'components': components}]
                rows.append(row)

                # init next loop (new row and total_width)
                row = []
                total_width = 0
            elif total_width >= 12:
                # add previous (loop) row
                rows.append(row)
                row = []
                # init new row for next loop
                col_data = {'column': col, 'components': components}
                rows.append(col_data)
                total_width = col['width']
            else:
                if not row:
                    row = [{'column': col, 'components': components}]
                else:
                    col_data = {'column': col, 'components': components}
                    row.append(col_data)
                total_width += col['width']
        if row:
            # add last generated row
            rows.append(row)
        return rows


class fieldsetComponent(layoutComponentBase):
    pass


class panelComponent(layoutComponentBase):

    @property
    def title(self):
        title = self.raw.get('title')
        if not title:
            title = self.raw.get('label')

        if self.i18n.get(self.language):
            return self.i18n[self.language].get(title, title)
        else:
            return title


class tableComponent(layoutComponentBase):
    pass


class tabsComponent(layoutComponentBase):
    pass


# Data components

class datagridComponent(Component):

    def __init__(self, raw, builder, **kwargs):
        self.rows = []
        super().__init__(raw, builder, **kwargs)

    def load(self, parent=None, data=None, renderer=None):
        super(datagridComponent, self).load(parent, data, renderer)
        if data:
            self._load_rows(data, renderer)

    def _load_rows(self, data, renderer):
        rows = []

        for row in self.value:
            # EXAMPLE row:
            # [{'email': 'personal@example.com'}, {'typeOfEmail': 'personal'}]

            new_row = []
            slots_todo = []
            slots_done = []

            for slot in row:
                # EXAMPLE slot:
                # {'email': 'personal@example.com'}
                for key, val in slot.items():
                    # EXAMPLE:
                    # key => 'email'
                    # val => 'personal@example.com'
                    for child in self.children:
                        if key == child.key:
                            raw = child.raw
                            new_slot = self.builder.get_component_object(raw)
                            new_slot.value = val
                            new_row.append(new_slot)
                            slots_done.append(key)
                    if key not in slots_done:
                        slots_todo.append(slot)
            if slots_todo:
                for child in self.children:
                    if hasattr(child, 'propagate_children'):
                        new_row.append(child.propagate_children(slots_todo))
            if new_row:
                rows.append(new_row)
        self.rows = rows

    @property
    def value(self):
        return super().value

    @value.setter
    def value(self, value=[]):
        rows = []
        for row in value:
            add_row = []
            for key, val in row.items():
                component = self.builder.components.get(key)
                rec = {key: component._encode_value(val)}
                add_row.append(rec)
            rows.append(add_row)
        super(self.__class__, self.__class__).value.fset(self, rows)

    @property
    def labels(self):
        labels = OrderedDict()
        for comp in self.raw['components']:
            if self.i18n.get(self.language):
                label = self.i18n[self.language].get(comp['label'], comp['label'])
            else:
                label = comp['label']
            labels[comp['key']] = label
        return labels


# Premium components

class fileComponent(Component):

    def __init__(self, raw, builder, **kwargs):
        super().__init__(raw, builder, **kwargs)

    @property
    def storage(self):
        return self.raw.get('storage')

    @property
    def url(self):
        return self.raw.get('url')

    @property
    def base64(self):
        if self.storage == 'url':
            res = ''
            for val in self.form.get('value'):
                name = val.get('name')
                url = val.get('url')
                res += base64_encode_url(url)
            return res
        elif self.storage == 'base64':
            return super().value

    # @value.setter
    # def value(self, value):
    #     """ Inherit property setter the right way, URLs:
    #     - https://gist.github.com/Susensio/979259559e2bebcd0273f1a95d7c1e79
    #     - https://stackoverflow.com/questions/35290540/understanding-property-decorator-and-inheritance
    #     """
    #     super(self.__class__, self.__class__).value.fset(self, value)


class resourceComponent(Component):

    def __init__(self, raw, builder, **kwargs):
        super().__init__(raw, builder, **kwargs)
        self.item_data = {}
        self.template_label_keys = decode_resource_template(self.raw.get('template'))
        self.compute_resources()

    def compute_resources(self):
        if self.resources:
            resource_id = self.raw.get('resource')
            if resource_id and not resource_id == "" and resource_id in self.resources:
                resource_list = self.resources[resource_id]
                self.raw['data'] = {"values": []}
                for item in resource_list:
                    label = fetch_dict_get_value(item, self.template_label_keys[:])
                    self.raw['data']['values'].append({
                        "label": label,
                        "value": item['_id']['$oid']
                    })

    @property
    def value_label(self):
        comp = self.builder.form_components.get(self.key)
        values = comp.raw.get('data') and comp.raw['data'].get('values')
        for val in values:
            if val['value'] == self.value:
                label = val['label']
                if self.i18n.get(self.language):
                    return self.i18n[self.language].get(label, label)
                else:
                    return label
        else:
            return False

    @property
    def value_labels(self):
        comp = self.builder.form_components.get(self.key)
        values = comp.raw.get('data') and comp.raw['data'].get('values')
        value_labels = []
        for val in values:
            if val['value'] in self.value:
                if self.i18n.get(self.language):
                    value_labels.append(self.i18n[self.language].get(val['label'], val['label']))
                else:
                    value_labels.append(val['label'])
        return value_labels

    @property
    def data(self):
        return self.raw.get('data')

    @property
    def values(self):
        return self.raw.get('data').get('values')
