# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from .component import Component


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

    def conditional_visible_when(self):
        cond = self.raw['conditional']
        triggering_component = self.component_owner.input_components[cond['when']]
        triggering_value = cond['eq']
        if triggering_component.value and triggering_component.value.get(
            triggering_value
        ):
            return cond['show']
        else:
            return not cond['show']
