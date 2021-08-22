# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import calendar
import json
import uuid
import logging

from collections import OrderedDict
from datetime import datetime

from formiodata.utils import base64_encode_url, decode_resource_template, fetch_dict_get_value


class Component:

    _none_value = None

    def __init__(self, raw, builder, **kwargs):
        self.raw = raw
        self.builder = builder

        self._parent = None
        self._component_owner = None
        # components can also be seen as children
        self.components = OrderedDict()

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

    def load(self, component_owner, parent=None, data=None, all_data=None):
        self.component_owner = component_owner

        if parent:
            self.parent = parent

        self._all_data = all_data
        self.load_data(data)

        self.builder.component_ids[self.id] = self

    def load_data(self, data, load_children=True):
        if self.input and data:
            try:
                self.value = data[self.key]
                self.raw_value = data[self.key]
            except KeyError:
                # NOTE: getter will read out defaultValue if it's missing in self.form
                # TODO: Is this the right approach?
                pass

        if not load_children:
            return

        # (Input) nested components (e.g. datagrid, editgrid)
        for component in self.raw.get('components', []):
            # Only determine and load class if component type.
            if 'type' in component:
                component_obj = self.builder.get_component_object(component)
                component_obj.load(self.child_component_owner, parent=self, data=data, all_data=self._all_data)

        # TODO: This code is iffy and tries to be generic for unknown components.
        # Maybe only call this (and the above) if not an input component?
        # (Layout) nested components (e.g. columns, panels)
        for k, vals in self.raw.copy().items():
            if k == 'components':
                continue # Already processed above, don't process subcomponents twice (#17)

            if isinstance(vals, list):
                for v in vals:
                    if 'components' in v:
                        for v_component in v['components']:
                            v_component_obj = self.builder.get_component_object(v_component)
                            v_component_obj.load(self.child_component_owner, parent=self, data=data, all_data=self._all_data)
                    elif isinstance(v, list):
                        # table component etc. which holds even deeper lists with components
                        for list_v in v:
                            if 'components' in list_v:
                                for list_v_component in list_v.get('components'):
                                    if list_v_component.get('type'):
                                        list_v_component_obj = self.builder.get_component_object(list_v_component)
                                        if list_v_component_obj.id not in self.builder.component_ids:
                                            list_v_component_obj.load(self.child_component_owner, parent=self, data=data, all_data=self._all_data)

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
    def validate(self):
        return self.raw.get('validate')

    @property
    def required(self):
        return self.raw.get('validate').get('required')

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
        self.html_component = '<p>%s</p>' % self.value

    @property
    def conditionally_visible(self):
        """
        If conditional visibility applies, evaluate to see if it is visible.
        Note that the component can also be hidden, which is a separate concept.
        """
        try:
            cond = self.raw['conditional']
            if cond.get('json'):
                # Optional package
                try:
                    from json_logic import jsonLogic
                    context = {'data': self._all_data}
                    try:
                        context['row'] = self.component_owner.row
                    except AttributeError:
                        pass # only datagrid rows have a "row" attribute
                    return jsonLogic(cond['json'], context)
                except ImportError:
                    logger = logging.getLogger(__name__)
                    logger.warn(f'Could not load json logic extension; will not evaluate visibility of {self.__class__.__name__} {self.id} ("{self.key}")')
                    return True

            elif cond.get('when'):
                triggering_component = self.component_owner.input_components[cond['when']]
                triggering_value = cond['eq']
                if triggering_component.value == triggering_value:
                    return cond['show']
                else:
                    return not cond['show']
        except KeyError:
            # Unknown component or no 'when', 'eq' or 'show' property
            pass

        # By default, it's visible
        return True

    @property
    def is_visible(self):
        return not self.hidden and self.conditionally_visible

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
        comp = self.component_owner.input_components.get(self.key)
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
        comp = self.component_owner.input_components.get(self.key)
        data_type = comp.raw.get('dataType')
        values = comp.raw.get('data') and comp.raw['data'].get('values')
        for val in values:
            if data_type == 'number':
                data_val = int(val['value'])
            else:
                data_val = val['value']

            if data_val == self.value:
                label = val['label']
                if self.i18n.get(self.language):
                    return self.i18n[self.language].get(label, label)
                else:
                    return label
        else:
            return False

    @property
    def value_labels(self):
        comp = self.component_owner.input_components.get(self.key)
        data_type = comp.raw.get('dataType')
        values = comp.raw.get('data') and comp.raw['data'].get('values')
        value_labels = []
        for val in values:
            if data_type == 'number':
                data_val = int(val['value'])
            else:
                data_val = val['value']

            if self.value and data_val in self.value:
                if self.i18n.get(self.language):
                    value_labels.append(self.i18n[self.language].get(val['label'], val['label']))
                else:
                    value_labels.append(val['label'])
        return value_labels


class radioComponent(Component):

    def _encode_value(self, value):
        # A number value got casted to integer, by json.loads().
        # Ensure this becomes a string.
        return str(value)

    @property
    def values_labels(self):
        comp = self.component_owner.input_components.get(self.key)
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
        comp = self.component_owner.input_components.get(self.key)
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

    @property
    def is_form_component(self):
        return False

    def load_data(self, data):
        # just bypass this
        pass


# Advanced

class emailComponent(Component):
    pass


class urlComponent(Component):
    pass


class phoneNumberComponent(Component):
    pass


# TODO: tags

class addressComponent(Component):

    _none_value = {}

    # XXX other providers not analysed and implemented yet.
    PROVIDER_GOOGLE = 'google'

    def load_data(self, data):
        super(addressComponent, self).load_data(data, load_children=False)

    def _address_google(self, get_type, notation='long_name'):
        comps = self.value.get('address_components')
        if not comps:
            return None
        else:
            for comp in comps:
                if comp.get('types') and get_type in comp['types']:
                    return comp.get(notation)
            return None

    @property
    def provider(self):
        return self.raw.get('provider')

    @property
    def postal_code(self):
        if self.provider == self.PROVIDER_GOOGLE:
            return self._address_google('postal_code')
        else:
            return None

    @property
    def street_name(self):
        if self.provider == self.PROVIDER_GOOGLE:
            return self._address_google('route')
        else:
            return None

    @property
    def street_number(self):
        if self.provider == self.PROVIDER_GOOGLE:
            return self._address_google('street_number')
        else:
            return None

    @property
    def city(self):
        if self.provider == self.PROVIDER_GOOGLE:
            return self._address_google('locality')
        else:
            return None

    @property
    def country(self):
        if self.provider == self.PROVIDER_GOOGLE:
            return self._address_google('country')
        else:
            return None


class datetimeComponent(Component):

    def _format_mappings(self):
        """
        Dictionary of mappings between Formio Datetime component
        (key) to Python format (value).

        Formio uses the format codes referenced in:
        https://github.com/angular-ui/bootstrap/tree/master/src/dateparser/docs#uibdateparsers-format-codes
        """
        return {
            'year': {'yyyy': '%Y', 'yy': '%y', 'y': '%y'},
            'month': {'MMMM': '%B', 'MMM': '%b', 'MM': '%m', 'M': '%-m'},
            'day': {'dd': '%d', 'd': '%-d'},
            'hour': {'HH': '%H', 'H': '%-H', 'hh': '%I', 'h': '%-I'},
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

        component = self.component_owner.input_components.get(self.key)
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


class dayComponent(Component):

    @property
    def dayFirst(self):
        return self.raw.get('dayFirst')

    @property
    def value(self):
        return super().value

    @value.setter
    def value(self, value):
        """
        Notes:
        - value format: dd/dd/yyyy
        - Empty value: '00/00/0000'
        """
        val = OrderedDict()
        fields = self.raw['fields']

        # XXX Maybe future formio versions have more formatting possibilites.
        if self.dayFirst:
            if not fields['day'].get('hide'):
                day_val = value[0:2]
                if day_val != '00':
                    val['day'] = int(day_val)
                else:
                    val['day'] = None
            if not fields['month'].get('hide'):
                month_val = value[3:5]
                if month_val != '00':
                    val['month'] = int(month_val)
                else:
                    val['month'] = None
        else:
            if not fields['month'].get('hide'):
                month_val = value[0:2]
                if month_val != '00':
                    val['month'] = int(month_val)
                else:
                    val['month'] = None
            if not fields['day'].get('hide'):
                day_val = value[3:5]
                if day_val != '00':
                    val['day'] = int(day_val)
                else:
                    val['day'] = None

        if not fields['year'].get('hide'):
            if not fields['year'].get('hide'):
                year_val = value[6:10]
                if year_val != '0000':
                    val['year'] = int(year_val)
                else:
                    val['year'] = None

        super(self.__class__, self.__class__).value.fset(self, val)

    @property
    def day(self):
        fields = self.raw['fields']
        if not fields['day'].get('hide'):
            return self.value['day']
        else:
            return None

    @property
    def month(self):
        fields = self.raw['fields']
        if not fields['month'].get('hide'):
            return self.value['month']
        else:
            return None

    @property
    def month_name(self):
        fields = self.raw['fields']
        if self.value['month'] and not fields['month'].get('hide'):
            month_name = calendar.month_name[self.value['month']]
            if self.i18n.get(self.language):
                return self.i18n[self.language].get(month_name, month_name)
            else:
                return month_name
        else:
            return None

    @property
    def year(self):
        fields = self.raw['fields']
        if not fields['year'].get('hide'):
            return self.value['year']
        else:
            return None


class timeComponent(Component):
    pass


class currencyComponent(Component):
    pass


class surveyComponent(Component):

    @property
    def values_labels(self):
        comp = self.component_owner.input_components.get(self.key)
        builder_values = comp.raw.get('values')
        labels = []
        for val in builder_values:
            if self.i18n.get(self.language):
                label = self.i18n[self.language].get(val['label'], val['label'])
            else:
                label = val['label']
            labels.append(label)
        return labels

    @property
    def grid(self):
        comp = self.component_owner.input_components.get(self.key)
        builder_questions = comp.raw.get('questions')
        builder_values = comp.raw.get('values')
        grid = []
        for question in builder_questions:
            # question
            if self.i18n.get(self.language):
                question_label = self.i18n[self.language].get(question['label'], question['label'])
            else:
                question_label = question['label']
            question_dict = {'question_value': question['value'], 'question_label': question_label, 'values': []}

            # value
            values = []
            for b_val in builder_values:
                if self.i18n.get(self.language):
                    val_label = self.i18n[self.language].get(b_val['label'], b_val['label'])
                else:
                    val_label = b_val['label']

                value = {
                    'label': val_label,
                    'value': b_val['value'],
                    'checked': False # default as fallback (if new values in builder)
                }

                if self.value.get(question['value']):
                    value['checked'] = self.value[question['value']] == b_val['value']

                question_dict['values'].append(value)

            # append
            grid.append(question_dict)
        return grid

class signatureComponent(Component):
    pass


# Layout components

class htmlelementComponent(Component):

    @property
    def html(self):
        html = '<%s>%s</%s>' % (self.raw['tag'], self.raw['content'], self.raw['tag'])
        return html

class contentComponent(Component):
    pass


class layoutComponentBase(Component):
    pass


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
                for key, comp in self.components.items():
                    if col_comp['id'] == comp.id:
                        components.append(comp)

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
                row.append(col_data)
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


    def render(self):
        html_rows = []
        for row in self.rows:
            html_cells = []
            for col in row:
                for component in col['components']:
                    if component.is_visible:
                        component.render()
                    else:
                        component.html_component = ''
                    html_cells.append('<td>'+component.html_component+'</td>')

            html_rows.append('<tr>'+(''.join(html_cells))+'</tr>')

        self.html_component = '<table>'+(''.join(html_rows))+'</table>'


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

    @property
    def rows(self):
        rows = []
        for row in self.raw['rows']:
            row_components = []

            for cols in row:
                for col_comp in cols['components']:
                    for key, comp in self.components.items():
                        if col_comp['id'] == comp.id:
                            row_components.append(comp)
            rows.append(row_components)
        return rows


class tabsComponent(layoutComponentBase):

    @property
    def tabs(self):
        tabs = []
        for tab in self.raw['components']:
            add_tab = {
                'tab': tab,
                'components': []
            }
            for comp in tab['components']:
                for key, comp in self.components.items():
                    if comp['key'] == comp.key:
                        add_tab['components'].append(comp[1])
            tabs.append(add_tab)
        return tabs


# Data components

class datagridComponent(Component):

    class gridRow:
        """Not *really* a component, but it implements the same
        partial interface with input_components and components.
        TODO: Consider if there should be a shared base component for
        this (ComponentOwner?)
        """
        def __init__(self, datagrid, data):
            self.datagrid = datagrid
            self.builder = datagrid.builder
            self.input_components = {}
            self.components = OrderedDict()
            self.form = datagrid.form
            self.row = data
            self.html_component = ''

            datagrid.create_component_objects(self, data)

        def render(self):
            html_components = []
            for component in self.components.values():
                if component.is_visible:
                    component.render()
                else:
                    component.html_component = ''
                html_components.append('<td>'+component.html_component+'</td>')

            self.html_component = '<tr>'+(''.join(html_components))+'</tr>'


    def __init__(self, raw, builder, **kwargs):
        # TODO when adding other data/grid components, create new
        # dataComponent class these can inherit from.
        self.input_components = {}
        self.rows = []
        super().__init__(raw, builder, **kwargs)
        self.form = {'value': []}

    def create_component_objects(self, parent, data):
        """This is a weird one, it creates component object for the
        "blueprint" inside the Builder, with parent = dataGrid, and in
        a form on each grid row with parent = gridRow
        """
        for component in self.raw.get('components', []):
            # Only determine and load class if component type.
            if 'type' in component:
                component_obj = parent.builder.get_component_object(component)
                component_obj.load(component_owner=parent, parent=parent, data=data, all_data=self._all_data)
                parent.components[component_obj.key] = component_obj

    def load_data(self, data):
        # Always instantiate child components, even if no data.
        # This makes it exist both in the builder and in the form.
        self.create_component_objects(self, data)

        # TODO: Make sure data is always a dict here?
        if data and data.get(self.key):
            self._load_rows(data[self.key])
            self.value = data[self.key]
            self.raw_value = data[self.key]
        elif not self.initEmpty:
            self.rows = [self.gridRow(self, None)]

    def _load_rows(self, data):
        rows = []

        for row in data:
            # EXAMPLE row (which is an entry in the data list):
            # {'email': 'personal@example.com', 'typeOfEmail': 'personal'}
            new_row = self.gridRow(self, row)

            if new_row:
                rows.append(new_row)
        self.rows = rows

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
    def is_form_component(self):
        # NOTE: A datagrid is not _really_ a form component, but it
        # has a key in the JSON for loading the form, so it acts as
        # such, and it will create an entry in the "input_components"
        # property of its owner.
        return True


    @property
    def child_component_owner(self):
        return self

    @property
    def initEmpty(self):
        return self.raw.get('initEmpty')

    def render(self):
        for row in self.rows:
            row.render()
        self.html_component = '<table>'+(''.join([row.html_component for row in self.rows]))+'</table>'


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
        comp = self.component_owner.input_components.get(self.key)
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
        comp = self.component_owner.input_components.get(self.key)
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
