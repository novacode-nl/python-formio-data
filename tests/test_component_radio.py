# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from test_component import ComponentTestCase
from formiodata.components import radioComponent


class radioComponentTestCase(ComponentTestCase):

    def test_object(self):
        cd = self.builder.form_components['cardinalDirection']
        self.assertIsInstance(cd, radioComponent)

        # Not radioComponent
        email = self.builder.form_components['email']
        self.assertNotIsInstance(email, radioComponent)

    def test_get_key(self):
        cd = self.builder.form_components['cardinalDirection']
        self.assertEqual(cd.key, 'cardinalDirection')

    def test_get_type(self):
        cd = self.builder.form_components['cardinalDirection']
        self.assertEqual(cd.type, 'radio')

    def test_get_label(self):
        cd = self.builder.form_components['cardinalDirection']
        self.assertEqual(cd.label, 'Cardinal Direction')

    def test_set_label(self):
        cd = self.builder.form_components['cardinalDirection']
        self.assertEqual(cd.label, 'Cardinal Direction')
        cd.label = 'Compass Direction'
        self.assertEqual(cd.label, 'Compass Direction')

    def test_get_form(self):
        cd = self.form.components['cardinalDirection']
        self.assertEqual(cd.label, 'Cardinal Direction')

        #self.assertEqual(cd.values_labels, 'south')
        self.assertEqual(cd.value, 'south')
        self.assertEqual(cd.value_label, 'South')
        self.assertEqual(cd.type, 'radio')
        
    def test_get_form_data(self):
        cd = self.form.data.cardinalDirection
        self.assertEqual(cd.label, 'Cardinal Direction')
        self.assertEqual(cd.value, 'south')
        self.assertEqual(cd.value_label, 'South')        
        self.assertEqual(cd.type, 'radio')

    # i18n translations
    def test_get_label_i18n_nl(self):
        cd = self.builder_i18n_nl.form_components['cardinalDirection']
        self.assertEqual(cd.label, 'Kardinale richting')

    def test_get_form_data_i18n_nl(self):
        self.assertEqual(self.form_i18n_nl.data.cardinalDirection.label, 'Kardinale richting')
        self.assertEqual(self.form_i18n_nl.data.cardinalDirection.value, 'south')
        self.assertEqual(self.form_i18n_nl.data.cardinalDirection.value_label, 'Zuid')
