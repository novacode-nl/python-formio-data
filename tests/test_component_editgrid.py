# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from test_component import ComponentTestCase
from formiodata.components import editgridComponent


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

    def test_get_row_labels(self):
        builder_editGrid = self.builder.components['editGrid']
        editGrid = self.form.input_components[builder_editGrid.key]

        self.assertEqual(len(editGrid.rows), 2)

        labels = ['Text Field', 'Date', 'Number', 'Checkbox']
        for key, label in editGrid.labels.items():
            self.assertIn(label , labels)

    def test_get_rows_values(self):
        builder_editGrid = self.builder.components['editGrid']
        editGrid = self.form.input_components[builder_editGrid.key]

        self.assertEqual(len(editGrid.rows), 2)

        textField_values = ['This is the FIRST row', 'This is the SECOND row', 'This is the THIRD row']
        date_values = ['2023-01-02', '2023-05-26', '2023-07-03']
        number_values = [123, 789, 456]
        checkbox_values = [True, False]
        for row_with_components in editGrid.rows:
            for component in row_with_components.input_components.values():
                if component.key == 'textField':
                    self.assertIn(component.value , textField_values)
                if component.key == 'date':
                    self.assertIn(component.value , date_values)
                if component.key == 'number':
                    self.assertIn(component.value , number_values)
                if component.key == 'checkbox':
                    self.assertIn(component.value , checkbox_values)
