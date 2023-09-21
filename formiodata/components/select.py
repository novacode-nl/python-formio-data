# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from .component import Component


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
