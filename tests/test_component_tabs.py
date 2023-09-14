# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from test_component import ComponentTestCase
from formiodata.components.tabs import tabsComponent
from formiodata.components.textfield import textfieldComponent
from formiodata.components.number import numberComponent


class tabsComponentTestCase(ComponentTestCase):

    def test_object(self):
        tabs = self.builder.components['tabs']
        self.assertIsInstance(tabs, tabsComponent)

        # Not tabsComponent
        email = self.builder.input_components['email']
        self.assertNotIsInstance(email, tabsComponent)

    def test_get_key(self):
        tabs = self.builder.components['tabs']
        self.assertEqual(tabs.key, 'tabs')

    def test_get_type(self):
        tabs = self.builder.components['tabs']
        self.assertEqual(tabs.type, 'tabs')

    def test_get_label(self):
        tabs = self.builder.components['tabs']
        self.assertEqual(tabs.label, 'Tabs')

    def test_get_tabs(self):
        builder_tabs_component = self.builder.components['tabs']
        tabs_component = self.form.components[builder_tabs_component.key]

        self.assertEqual(len(tabs_component.tabs), 2)

        for tab in tabs_component.tabs:
            if tab['tab']['key'] == 'tab1':
                self.assertEqual(tab['tab']['label'], 'Tab 1')
                # components in tab
                self.assertEqual(len(tab['components']), 1)
                textfieldTab1 = tab['components'][0]
                self.assertIsInstance(textfieldTab1, textfieldComponent)
                self.assertEqual(textfieldTab1.value, 'text in tab 1')
            if tab['tab']['key'] == 'tab2':
                self.assertEqual(tab['tab']['label'], 'Tab 2')
                # components in tab
                self.assertEqual(len(tab['components']), 1)
                numberTab2 = tab['components'][0]
                self.assertIsInstance(numberTab2, numberComponent)
                self.assertEqual(numberTab2.value, 2)
