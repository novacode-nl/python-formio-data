# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from test_component import ComponentTestCase


class ValidationErrorSimpleTestCase(ComponentTestCase):

    def test_required_components_in_builder(self):
        firstName = self.builder.input_components['firstName']
        self.assertTrue(firstName.required)

        lastName = self.builder.input_components['lastName']
        self.assertTrue(lastName.required)

        email = self.builder.input_components['email']
        self.assertFalse(email.required)

    def test_required_components_form_validation_errors(self):
        errors = self.form_empty.validation_errors()

        self.assertEqual(
            errors['firstName']['required'],
            'First Name is required'
        )
        self.assertEqual(
            errors['lastName']['required'],
            'Last Name is required'
        )
        self.assertEqual(
            errors['dataGrid'][0]['textField']['required'],
            'Text Field is required'
        )

    def test_required_components_form_validation_errors_i18n_nl(self):
        errors = self.form_empty_i18n_nl.validation_errors()

        self.assertEqual(
            errors['firstName']['required'],
            'Voornaam is verplicht'
        )
        self.assertEqual(
            errors['lastName']['required'],
            'Achternaam is verplicht'
        )
        self.assertEqual(
            errors['dataGrid'][0]['textField']['required'],
            'Tekstveld is verplicht'
        )

    def test_not_required_components_form(self):
        errors = self.form_empty_i18n_nl.validation_errors()
        self.assertNotIn('email', errors)
