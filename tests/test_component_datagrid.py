# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from test_component import ComponentTestCase
from formiodata.components import datagridComponent


class datagridComponentTestCase(ComponentTestCase):

    def test_object(self):
        # TextfieldComponent
        dataGrid = self.builder.components['dataGrid']
        self.assertIsInstance(dataGrid, datagridComponent)

        # Not TextfieldComponent
        email = self.builder.form_components['email']
        self.assertNotIsInstance(email, datagridComponent)
        submit = self.builder.form_components['submit']
        self.assertNotIsInstance(submit, datagridComponent)

    def test_get_key(self):
        dataGrid = self.builder.components['dataGrid']
        self.assertEqual(dataGrid.key, 'dataGrid')

    def test_get_type(self):
        dataGrid = self.builder.components['dataGrid']
        self.assertEqual(dataGrid.type, 'datagrid')

    def test_get_label(self):
        dataGrid = self.builder.components['dataGrid']
        self.assertEqual(dataGrid.label, 'Data Grid')

    def test_get_row_labels(self):
        dataGrid = self.form.components['dataGrid']

        self.assertEqual(len(dataGrid.rows), 2)

        labels = ['Text Field', 'Checkbox']
        for key, label in dataGrid.labels.items():
            self.assertIn(label , labels)

    def test_get_rows_values(self):
        dataGrid = self.form.components['dataGrid']

        self.assertEqual(len(dataGrid.rows), 2)

        textField_values = ['abc', 'def']
        checkbox_values = [True, False]
        for row_dict in dataGrid.rows:
            self.assertIn(row_dict['textField']['_object'].value , textField_values)
            self.assertIn(row_dict['checkbox']['_object'].value , checkbox_values)
