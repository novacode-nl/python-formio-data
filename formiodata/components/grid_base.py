# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from collections import OrderedDict

from .component import Component


class baseGridComponent(Component):

    class gridRow:
        """Not *really* a component, but it implements the same
        partial interface with input_components and components.
        TODO: Consider if there should be a shared base component for
        this (ComponentOwner?)
        """
        def __init__(self, grid, data):
            self.grid = grid
            self.builder = grid.builder
            self.builder_path = None
            self.input_components = {}
            self.components = OrderedDict()
            self.form = grid.form
            self.row = data
            self.html_component = ''
            grid.create_component_objects(self, data)

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
        "blueprint" inside the Builder, with parent = grid, and in
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
        # NOTE: A grid is not _really_ a form component, but it
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
