# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.
import json
from collections import OrderedDict
from datetime import datetime

from formiodata.utils import base64_encode_url, decode_resource_template, fetch_dict_get_value


class Component:

    def __init__(self, raw, builder, **kwargs):
        # TODO or provide the Builder object?
        self.raw = raw
        self.builder = builder
        self.form = {}

        # i18n (language, translations)
        self.language = kwargs.get('language', 'en')
        self.i18n = kwargs.get('i18n', {})
        self.resources = kwargs.get('resources', {})
        if self.resources and isinstance(self.resources, str):
            self.resources = json.loads(self.resources)
        self.html_component = ""
        self.defaultValue = self.raw.get('defaultValue')

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
        self.form['value'] = value

    @property
    def raw_value(self):
        return self.form['raw_value']

    @raw_value.setter
    def raw_value(self, value):
        self.form['raw_value'] = value

    @property
    def hidden(self):
        return self.raw.get('hidden')

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
            # == Python 3.7
            return datetime.fromisoformat(value)
        else:
            # < Python 3.7
            fmt_str =  r"%Y-%m-%dT%H:%M:%S.%f" # replaces the fromisoformatm, not available in python 3.6
            return datetime.datetime.strptime(value, fmt_str)

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
        component = self.builder.components.get(self.key)
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


class columnsComponent(Component):
    pass


class fieldsetComponent(Component):
    pass


class panelComponent(Component):

    @property
    def title(self):
        component = self.builder.components.get(self.key)
        title = component.raw.get('title')
        if not title:
            title = component.raw.get('label')

        if self.i18n.get(self.language):
            return self.i18n[self.language].get(title, title)
        else:
            return title


class tableComponent(Component):
    pass


class tabsComponent(Component):
    pass


# Data components

class datagridComponent(Component):

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

    @property
    def rows(self):
        rows = []
        components = self.builder.components

        # Sanity check is really needed.
        # TODO add test for empty datagrid value.
        if not self.value:
            return rows

        for row_dict in self.value:
            row = OrderedDict()
            for key, val in row_dict.items():
                # Copy component raw (dict), to ensure no binding and overwrite.
                component = components[key].raw.copy()
                component_obj = self.builder.get_component_object(component)
                if component_obj.input:
                    component_obj.value = val
                component['_object'] = component_obj
                row[key] = component
            rows.append(row)
        return rows


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
