# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from test_component import ComponentTestCase
from formiodata.components import selectComponent


class selectMultipleComponentTestCase(ComponentTestCase):

    def test_object(self):
        # selectComponent
        food = self.builder.form_components['favouriteFood']
        self.assertIsInstance(food, selectComponent)

        # Not selectComponent
        email = self.builder.form_components['email']
        self.assertNotIsInstance(email, selectComponent)

    def test_get_key(self):
        food = self.builder.form_components['favouriteFood']
        self.assertEqual(food.key, 'favouriteFood')

    def test_get_type(self):
        food = self.builder.form_components['favouriteFood']
        self.assertEqual(food.type, 'select')

    def test_get_label(self):
        food = self.builder.form_components['favouriteFood']
        self.assertEqual(food.label, 'Favourite Food')

    def test_set_label(self):
        food = self.builder.form_components['favouriteFood']
        self.assertEqual(food.label, 'Favourite Food')
        food.label = 'Gimme which Food'
        self.assertEqual(food.label, 'Gimme which Food')

    def test_get_form(self):
        food = self.form.components['favouriteFood']
        self.assertEqual(food.label, 'Favourite Food')
        self.assertEqual(food.value, ['mexican', 'chinese'])
        self.assertEqual(food.value_labels, ['Mexican', 'Chinese'])
        self.assertEqual(food.value_label, False)
        self.assertEqual(food.type, 'select')
        
    def test_get_form_data(self):
        food = self.form.data.favouriteFood
        self.assertEqual(food.label, 'Favourite Food')
        self.assertEqual(food.value, ['mexican', 'chinese'])
        self.assertEqual(food.value_labels, ['Mexican', 'Chinese'])
        self.assertEqual(food.value_label, False)
        self.assertEqual(food.type, 'select')

    # i18n translations
    def test_get_label_i18n_nl(self):
        food = self.builder_i18n_nl.form_components['favouriteFood']
        self.assertEqual(food.label, 'Lievelingseten')

    def test_get_form_data_i18n_nl(self):
        self.assertEqual(self.form_i18n_nl.data.favouriteFood.label, 'Lievelingseten')
        self.assertEqual(self.form_i18n_nl.data.favouriteFood.value, ['mexican', 'chinese'])
        self.assertEqual(self.form_i18n_nl.data.favouriteFood.value_labels, ['Mexican', 'Chinese'])
