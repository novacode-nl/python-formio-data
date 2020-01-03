# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from test_component import ComponentTestCase
from components import textfieldComponent


class TextfieldComponentTestCase(ComponentTestCase):

    def test_object(self):
        # TextfieldComponent
        firstName = self.builder.components['firstName']
        self.assertIsInstance(firstName, textfieldComponent)

        lastName = self.builder.components['lastName']
        self.assertIsInstance(lastName, textfieldComponent)

        # Not TextfieldComponent
        email = self.builder.components['email']
        self.assertNotIsInstance(email, textfieldComponent)
        submit = self.builder.components['submit']
        self.assertNotIsInstance(submit, textfieldComponent)

    def test_get_key(self):
        firstName = self.builder.components['firstName']
        self.assertEqual(firstName.key, 'firstName')

    def test_get_type(self):
        firstName = self.builder.components['firstName']
        self.assertEqual(firstName.type, 'textfield')

    def test_get_label(self):
        firstName = self.builder.components['firstName']
        self.assertEqual(firstName.label, 'First Name')

    def test_set_label(self):
        firstName = self.builder.components['firstName']
        self.assertEqual(firstName.label, 'First Name')
        firstName.label = 'Foobar'
        self.assertEqual(firstName.label, 'Foobar')

    def test_get_submission(self):
        firstName = self.submission.components['firstName']
        self.assertEqual(firstName.label, 'First Name')
        self.assertEqual(firstName.value, 'Bob')
        self.assertEqual(firstName.type, 'textfield')
        
    def test_get_submission_data(self):
        firstName = self.submission.data.firstName
        self.assertEqual(firstName.label, 'First Name')
        self.assertEqual(firstName.value, 'Bob')
        self.assertEqual(firstName.type, 'textfield')
