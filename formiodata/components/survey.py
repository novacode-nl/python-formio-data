# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from .component import Component


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
            for b_val in builder_values:
                if self.i18n.get(self.language):
                    val_label = self.i18n[self.language].get(b_val['label'], b_val['label'])
                else:
                    val_label = b_val['label']

                value = {
                    'label': val_label,
                    'value': b_val['value'],
                    'checked': False  # default as fallback (if new values in builder)
                }

                if self.value.get(question['value']):
                    value['checked'] = self.value[question['value']] == b_val['value']

                question_dict['values'].append(value)

            # append
            grid.append(question_dict)
        return grid
