# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from test_component import ComponentTestCase
from formiodata.components.datagrid import datagridComponent


class datagridComponentTestCase(ComponentTestCase):

    def test_object(self):
        dataGrid = self.builder.components['dataGrid']
        self.assertIsInstance(dataGrid, datagridComponent)
        email = self.builder.input_components['email']
        self.assertNotIsInstance(email, datagridComponent)

    def test_get_key(self):
        dataGrid = self.builder.components['dataGrid']
        self.assertEqual(dataGrid.key, 'dataGrid')

    def test_get_type(self):
        dataGrid = self.builder.components['dataGrid']
        self.assertEqual(dataGrid.type, 'datagrid')

    def test_get_label(self):
        dataGrid = self.builder.components['dataGrid']
        self.assertEqual(dataGrid.label, 'Data Grid')

    def test_paths(self):
        dataGrid = self.builder.components['dataGrid']
        # datagrid
        self.assertEqual(dataGrid.builder_path_key, ['dataGrid'])
        self.assertEqual(dataGrid.builder_path_label, ['Data Grid'])
        self.assertEqual(dataGrid.builder_input_path_key, ['dataGrid'])
        self.assertEqual(dataGrid.builder_input_path_label, ['Data Grid'])
        # datagrid inputs
        for pos, row_with_components in enumerate(dataGrid.rows):
            for component in row_with_components.input_components.values():
                if component.key == 'textField':
                    self.assertEqual(component.builder_path_key, ['dataGrid', 'textField'])
                    self.assertEqual(component.builder_path_label, ['Data Grid', 'Text Field'])
                    self.assertEqual(component.builder_input_path_key, ['dataGrid', 'textField'])
                    self.assertEqual(component.builder_input_path_label, ['Data Grid', 'Text Field'])
                if component.key == 'checkbox':
                    self.assertEqual(component.builder_path_key, ['dataGrid', 'checkbox'])
                    self.assertEqual(component.builder_path_label, ['Data Grid', 'Checkbox'])
                    self.assertEqual(component.builder_input_path_key, ['dataGrid', 'checkbox'])
                    self.assertEqual(component.builder_input_path_label, ['Data Grid', 'Checkbox'])

    def test_get_row_labels(self):
        builder_dataGrid = self.builder.components['dataGrid']
        dataGrid = self.form.input_components[builder_dataGrid.key]

        self.assertEqual(len(dataGrid.rows), 2)

        labels = ['Text Field', 'Checkbox']
        for key, label in dataGrid.labels.items():
            self.assertIn(label , labels)

    def test_get_rows_values(self):
        builder_dataGrid = self.builder.components['dataGrid']
        dataGrid = self.form.input_components[builder_dataGrid.key]

        self.assertEqual(len(dataGrid.rows), 2)

        textField_values = ['abc', 'def']
        checkbox_values = [True, False]
        for pos, row_with_components in enumerate(dataGrid.rows):
            for component in row_with_components.input_components.values():
                if component.key == 'textField':
                    self.assertEqual(textField_values[pos], component.value)
                if component.key == 'checkbox':
                    self.assertEqual(checkbox_values[pos], component.value)
