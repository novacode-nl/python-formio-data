# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from test_component import ComponentTestCase
from formiodata.components import tableComponent


class tableComponentTestCase(ComponentTestCase):

    def test_object(self):
        # tableComponent
        table = self.builder.components['table']
        self.assertIsInstance(table, tableComponent)

        # Not tableComponent
        email = self.builder.input_components['email']
        self.assertNotIsInstance(email, tableComponent)

    def test_get_key(self):
        table = self.builder.components['table']
        self.assertEqual(table.key, 'table')

    def test_get_type(self):
        table = self.builder.components['table']
        self.assertEqual(table.type, 'table')

    def test_get_label(self):
        table = self.builder.components['table']
        self.assertEqual(table.label, 'Table')

    def test_get_row_labels(self):
        builder_table = self.builder.components['table']
        table = self.form.input_components[builder_table.key]

        self.assertEqual(len(table.rows), 2)

    def test_get_rows_values(self):
        builder_table = self.builder.components['table']
        table = self.form.components[builder_table.key]

        self.assertEqual(len(table.rows), 2)

        textField_values = ['Elephant', 'Lion']
        checkbox_values = [True, False]
        for row_with_components in table.rows:
            for component in row_with_components.input_components.values():
                if component.type == 'textfield':
                    self.assertIn(component.value , textField_values)
                if component.type == 'checkbox':
                    self.assertIn(component.value , checkbox_values)
