# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from test_component import ComponentTestCase
from formiodata.components.editgrid import editgridComponent


class editgridComponentTestCase(ComponentTestCase):

    def test_object(self):
        editgrid = self.builder.components['editGrid']
        self.assertIsInstance(editgrid, editgridComponent)
        email = self.builder.input_components['email']
        self.assertNotIsInstance(email, editgridComponent)

    def test_get_key(self):
        editGrid = self.builder.components['editGrid']
        self.assertEqual(editGrid.key, 'editGrid')

    def test_get_type(self):
        editGrid = self.builder.components['editGrid']
        self.assertEqual(editGrid.type, 'editgrid')

    def test_get_label(self):
        editGrid = self.builder.components['editGrid']
        self.assertEqual(editGrid.label, 'Edit Grid')

    def test_paths(self):
        editGrid = self.builder.components['editGrid']
        # editgrid
        self.assertEqual(editGrid.builder_path_key, ['editGrid'])
        self.assertEqual(editGrid.builder_path_label, ['Edit Grid'])
        self.assertEqual(editGrid.builder_input_path_key, ['editGrid'])
        self.assertEqual(editGrid.builder_input_path_label, ['Edit Grid'])
        # editgrid inputs
        for pos, row_with_components in enumerate(editGrid.rows):
            for component in row_with_components.input_components.values():
                if component.key == 'textfield':
                    self.assertEqual(component.builder_path_key, ['editGrid', 'textField'])
                    self.assertEqual(component.builder_path_label, ['Edit Grid', 'Text Field'])
                    self.assertEqual(component.builder_input_path_key, ['editGrid', 'textField'])
                    self.assertEqual(component.builder_input_path_label, ['Edit Grid', 'Text Field'])
                if component.key == 'date':
                    self.assertEqual(component.builder_path_key, ['editGrid', 'datetime'])
                    self.assertEqual(component.builder_path_label, ['Edit Grid', 'Date'])
                    self.assertEqual(component.builder_input_path_key, ['editGrid', 'datetime'])
                    self.assertEqual(component.builder_input_path_label, ['Edit Grid', 'Date'])
                if component.key == 'textArea':
                    self.assertEqual(component.builder_path_key, ['editGrid', 'textArea'])
                    self.assertEqual(component.builder_path_label, ['Edit Grid', 'Text Area'])
                    self.assertEqual(component.builder_input_path_key, ['editGrid', 'textArea'])
                    self.assertEqual(component.builder_input_path_label, ['Edit Grid', 'Text Area'])
                if component.key == 'number':
                    self.assertEqual(component.builder_path_key, ['editGrid', 'number'])
                    self.assertEqual(component.builder_path_label, ['Edit Grid', 'Number'])
                    self.assertEqual(component.builder_input_path_key, ['editGrid', 'number'])
                    self.assertEqual(component.builder_input_path_label, ['Edit Grid', 'Number'])
                if component.key == 'checkbox':
                    self.assertEqual(component.builder_path_key, ['editGrid', 'checkbox'])
                    self.assertEqual(component.builder_path_label, ['Edit Grid', 'Checkbox'])
                    self.assertEqual(component.builder_input_path_key, ['editGrid', 'checkbox'])
                    self.assertEqual(component.builder_input_path_label, ['Edit Grid', 'Checkbox'])

    def test_get_row_labels(self):
        builder_editGrid = self.builder.components['editGrid']
        editGrid = self.form.input_components[builder_editGrid.key]

        self.assertEqual(len(editGrid.rows), 3)

        labels = ['Text Field', 'Text Area', 'Date', 'Select', 'Number', 'Checkbox']
        for key, label in editGrid.labels.items():
            self.assertIn(label , labels)

    def test_get_rows_values(self):
        builder_editGrid = self.builder.components['editGrid']
        editGrid = self.form.input_components[builder_editGrid.key]

        self.assertEqual(len(editGrid.rows), 3)

        textField_values = ['This is the FIRST row', 'This is the SECOND row', 'This is the THIRD row']
        date_values = ['2023-01-02', '2023-05-26', '2023-07-03']
        number_values = [123, 789, 456]
        checkbox_values = [True, False, False]
        textArea_values = ['The first textarea.\nSuch nice!', '', '']
        for pos, row_with_components in enumerate(editGrid.rows):
            for component in row_with_components.input_components.values():
                if component.key == 'textField':
                    self.assertEqual(textField_values[pos], component.value)
                if component.key == 'date':
                    self.assertIn(date_values[pos], component.value)
                if component.key == 'textArea':
                    self.assertIn(textArea_values[pos], component.value)
                if component.key == 'number':
                    self.assertIn(number_values[pos], component.value)
                if component.key == 'checkbox':
                    self.assertIn(checkbox_values[pos], component.value)
