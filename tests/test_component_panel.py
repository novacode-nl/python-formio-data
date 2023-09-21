# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from test_component import ComponentTestCase
from formiodata.components.panel import panelComponent


class panelComponentTestCase(ComponentTestCase):

    def test_object(self):
        # TextfieldComponent
        panel = self.builder.components['panel']
        self.assertIsInstance(panel, panelComponent)

        # Not TextfieldComponent
        email = self.builder.input_components['email']
        self.assertNotIsInstance(email, panelComponent)

    def test_get_key(self):
        panel = self.builder.components['panel']
        self.assertEqual(panel.key, 'panel')

    def test_get_type(self):
        panel = self.builder.components['panel']
        self.assertEqual(panel.type, 'panel')

    def test_get_label(self):
        panel = self.builder.components['panel']
        self.assertEqual(panel.label, 'Panel')

    def test_get_title(self):
        panel = self.builder.components['panel']
        self.assertEqual(panel.title, 'My Favourites')

    # i18n translations
    def test_get_title_i18n_nl(self):
        panel = self.builder_i18n_nl.components['panel']
        self.assertEqual(panel.title, 'Mijn favorieten')
