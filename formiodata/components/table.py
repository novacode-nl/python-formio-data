# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from .layout_base import layoutComponentBase


class tableComponent(layoutComponentBase):
    def __init__(self, raw, builder, **kwargs):
        self.rows = []
        super().__init__(raw, builder, **kwargs)

    def load_data(self, data, is_form=False):
        self.rows = []

        for data_row in self.raw.get('rows', []):
            row = []

            for col in data_row:
                components = []
                for component in col['components']:
                    # Only determine and load class if component type.
                    if 'type' in component:
                        component_obj = self.builder.get_component_object(component)
                        component_obj.load(
                            self.child_component_owner,
                            parent=self,
                            data=data,
                            all_data=self._all_data,
                            is_form=is_form,
                        )
                        components.append(component_obj)

                row.append({'column': col, 'components': components})

            self.rows.append(row)
