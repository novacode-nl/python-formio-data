# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from test_component import ComponentTestCase
from formiodata.components.selectboxes import selectboxesComponent


class selectboxesComponentTestCase(ComponentTestCase):

    def setUp(self):
        super(selectboxesComponentTestCase, self).setUp()
        self.selectboxes_value = {
            "north": True,
            "east": False,
            "south": True,
            "west": False,
        }
        self.selectboxes_values_labels = {
            "north": {"key": "north", "label": "North", "value": True},
            "east": {"key": "east", "label": "East", "value": False},
            "south": {"key": "south", "label": "South", "value": True},
            "west": {"key": "west", "label": "West", "value": False},
        }
        self.selectboxes_values_labels_i18n_nl = {
            "north": {"key": "north", "label": "Noord", "value": True},
            "east": {"key": "east", "label": "Oost", "value": False},
            "south": {"key": "south", "label": "Zuid", "value": True},
            "west": {"key": "west", "label": "West", "value": False},
        }

    def test_object(self):
        # selectboxesComponent
        selectBoxes = self.builder.input_components['selectBoxes']
        self.assertIsInstance(selectBoxes, selectboxesComponent)

        # Not selectboxesComponent
        email = self.builder.input_components['email']
        self.assertNotIsInstance(email, selectboxesComponent)

    def test_get_key(self):
        selectBoxes = self.builder.input_components['selectBoxes']
        self.assertEqual(selectBoxes.key, 'selectBoxes')

    def test_get_type(self):
        selectBoxes = self.builder.input_components['selectBoxes']
        self.assertEqual(selectBoxes.type, 'selectboxes')

    def test_get_label(self):
        selectBoxes = self.builder.input_components['selectBoxes']
        self.assertEqual(selectBoxes.label, 'Select Boxes')

    def test_set_label(self):
        selectBoxes = self.builder.input_components['selectBoxes']
        self.assertEqual(selectBoxes.label, 'Select Boxes')
        selectBoxes.label = 'Other Select Boxes'
        self.assertEqual(selectBoxes.label, 'Other Select Boxes')

    def test_get_form(self):
        selectBoxes = self.form.input_components['selectBoxes']
        self.assertEqual(selectBoxes.label, 'Select Boxes')
        self.assertEqual(selectBoxes.value, self.selectboxes_value)
        self.assertEqual(selectBoxes.values_labels, self.selectboxes_values_labels)
        self.assertEqual(selectBoxes.type, 'selectboxes')

    def test_get_form_data(self):
        selectBoxes = self.form.input.selectBoxes
        self.assertEqual(selectBoxes.label, 'Select Boxes')
        self.assertEqual(selectBoxes.value, self.selectboxes_value)
        self.assertEqual(selectBoxes.values_labels, self.selectboxes_values_labels)
        self.assertEqual(selectBoxes.type, 'selectboxes')

    # i18n translations
    def test_get_label_i18n_nl(self):
        food = self.builder_i18n_nl.input_components['selectBoxes']
        self.assertEqual(food.label, 'Select aanvink opties')

    def test_get_form_data_i18n_nl(self):
        self.assertEqual(self.form_i18n_nl.input.selectBoxes.label, 'Select aanvink opties')
        self.assertEqual(self.form_i18n_nl.input.selectBoxes.value, self.selectboxes_value)
        self.assertEqual(
            self.form_i18n_nl.input.selectBoxes.values_labels,
            self.selectboxes_values_labels_i18n_nl,
        )
