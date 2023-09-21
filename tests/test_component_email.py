# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from test_component import ComponentTestCase
from formiodata.components.email import emailComponent


class emailComponentTestCase(ComponentTestCase):

    def test_object(self):
        # EmailComponent
        email = self.builder.input_components['email']
        self.assertIsInstance(email, emailComponent)

        # Not EmailComponent
        firstName = self.builder.input_components['firstName']
        self.assertNotIsInstance(firstName, emailComponent)

    def test_get_key(self):
        email = self.builder.input_components['email']
        self.assertEqual(email.key, 'email')

    def test_get_type(self):
        email = self.builder.input_components['email']
        self.assertEqual(email.type, 'email')

    def test_get_label(self):
        email = self.builder.input_components['email']
        self.assertEqual(email.label, 'Email')

    def test_set_label(self):
        email = self.builder.input_components['email']
        self.assertEqual(email.label, 'Email')
        email.label = 'Foobar'
        self.assertEqual(email.label, 'Foobar')

    def test_get_form(self):
        email = self.form.input_components['email']
        self.assertEqual(email.label, 'Email')
        self.assertEqual(email.value, 'bob@novacode.nl')
        self.assertEqual(email.type, 'email')

    def test_get_form_data(self):
        email = self.form.input.email
        self.assertEqual(email.label, 'Email')
        self.assertEqual(email.value, 'bob@novacode.nl')
        self.assertEqual(email.type, 'email')
