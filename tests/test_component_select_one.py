# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from test_component import ComponentTestCase
from formiodata.components.select import selectComponent


class selectOneComponentTestCase(ComponentTestCase):

    def test_object(self):
        # selectComponent
        season = self.builder.input_components['favouriteSeason']
        self.assertIsInstance(season, selectComponent)

        # Not selectComponent
        email = self.builder.input_components['email']
        self.assertNotIsInstance(email, selectComponent)

    def test_get_key(self):
        season = self.builder.input_components['favouriteSeason']
        self.assertEqual(season.key, 'favouriteSeason')

    def test_get_type(self):
        season = self.builder.input_components['favouriteSeason']
        self.assertEqual(season.type, 'select')

    def test_get_label(self):
        season = self.builder.input_components['favouriteSeason']
        self.assertEqual(season.label, 'Favourite Season')

    def test_set_label(self):
        season = self.builder.input_components['favouriteSeason']
        self.assertEqual(season.label, 'Favourite Season')
        season.label = 'Which Season'
        self.assertEqual(season.label, 'Which Season')

    def test_get_form(self):
        season = self.form.input_components['favouriteSeason']
        self.assertEqual(season.label, 'Favourite Season')
        self.assertEqual(season.value, 'autumn')
        self.assertEqual(season.value_label, 'Autumn')
        self.assertEqual(season.type, 'select')

    def test_get_form_data(self):
        season = self.form.input.favouriteSeason
        self.assertEqual(season.label, 'Favourite Season')
        self.assertEqual(season.value, 'autumn')
        self.assertEqual(season.value_label, 'Autumn')
        self.assertEqual(season.type, 'select')

    # i18n translations
    def test_get_label_i18n_nl(self):
        season = self.builder_i18n_nl.input_components['favouriteSeason']
        self.assertEqual(season.label, 'Favoriete seizoen')

    def test_get_form_data_i18n_nl(self):
        self.assertEqual(self.form_i18n_nl.input.favouriteSeason.label, 'Favoriete seizoen')
        self.assertEqual(self.form_i18n_nl.input.favouriteSeason.value, 'autumn')
        self.assertEqual(self.form_i18n_nl.input.favouriteSeason.value_label, 'Herfst')
