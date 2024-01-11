# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from .layout_base import layoutComponentBase


class fieldsetComponent(layoutComponentBase):

    def load_data(self, data, is_form=False):
        for component in self.raw.get('components', []):
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
