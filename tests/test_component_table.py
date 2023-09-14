# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from test_component import ComponentTestCase
from formiodata.components.table import tableComponent


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
        table = self.form.components[builder_table.key]

        self.assertEqual(len(table.rows), 2)

        labels = ['Text Field', 'Checkbox']
        for row in table.rows:
            for col in row:
                for comp in col['components']:
                    self.assertIn(comp.label , labels)

    def test_get_rows_values(self):
        builder_table = self.builder.components['table']
        table = self.form.components[builder_table.key]

        self.assertEqual(len(table.rows), 2)

        # Accessing directly...
        self.assertEqual(table.components['textField'].value, 'Elephant')
        self.assertEqual(table.components['checkbox'].value, True)
        self.assertEqual(table.components['textField1'].value, 'Lion')
        self.assertEqual(table.components['checkbox1'].value, False)

        # Or through rows/cols:
        self.assertEqual(table.rows[0][0]['components'][0], table.components['textField'])
        self.assertEqual(table.rows[0][1]['components'][0], table.components['checkbox'])
        self.assertEqual(table.rows[1][0]['components'][0], table.components['textField1'])
        self.assertEqual(table.rows[1][1]['components'][0], table.components['checkbox1'])
