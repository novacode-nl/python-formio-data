# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from .layout_base import layoutComponentBase


class tabsComponent(layoutComponentBase):

    def load_data(self, data, is_form=False):
        self.tabs = []

        for data_tab in self.raw.get('components', []):
            tab = {'tab': data_tab, 'components': []}

            for component in data_tab['components']:
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
                    tab['components'].append(component_obj)

            self.tabs.append(tab)
