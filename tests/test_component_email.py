# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from test_component import ComponentTestCase
from components import emailComponent


class EmailComponentTestCase(ComponentTestCase):

    def test_object(self):
        # EmailComponent
        email = self.builder.components['email']
        self.assertIsInstance(email, emailComponent)

        # Not EmailComponent
        firstName = self.builder.components['firstName']
        self.assertNotIsInstance(firstName, emailComponent)
        submit = self.builder.components['submit']
        self.assertNotIsInstance(submit, emailComponent)

    def test_get_key(self):
       email = self.builder.components['email']
       self.assertEqual(email.key, 'email')

    def test_get_type(self):
        email = self.builder.components['email']
        self.assertEqual(email.type, 'email')

    def test_get_label(self):
        email = self.builder.components['email']
        self.assertEqual(email.label, 'Email')

    def test_set_label(self):
        email = self.builder.components['email']
        self.assertEqual(email.label, 'Email')
        email.label = 'Foobar'
        self.assertEqual(email.label, 'Foobar')

    def test_get_submission(self):
        email = self.submission.components['email']
        self.assertEqual(email.label, 'Email')
        self.assertEqual(email.value, 'bob@novacode.nl')
        self.assertEqual(email.type, 'email')

    def test_get_submission_data(self):
        email = self.submission.data.email
        self.assertEqual(email.label, 'Email')
        self.assertEqual(email.value, 'bob@novacode.nl')
        self.assertEqual(email.type, 'email')
