# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from tests.utils import readfile
from test_component import ComponentTestCase

from formiodata.form import Form


class ValidationErrorSimpleTestCase(ComponentTestCase):

    def setUp(self):
        super(ValidationErrorSimpleTestCase, self).setUp()
        self.form_validation_errors_json = readfile('data', 'test_example_form_validation_errors.json')
        self.form_validation_errors = Form(self.form_validation_errors_json, self.builder)
        self.form_validation_errors_i18n_nl = Form(self.form_validation_errors_json, self.builder_i18n_nl)

    def test_required_components_in_builder(self):
        firstName = self.builder.input_components['firstName']
        self.assertTrue(firstName.required)

        lastName = self.builder.input_components['lastName']
        self.assertTrue(lastName.required)

        email = self.builder.input_components['email']
        self.assertFalse(email.required)

    def test_required_components_form_validation_errors(self):
        errors = self.form_validation_errors.validation_errors()

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
        self.assertEqual(
            errors['dataGrid'][1],
            {}
        )
        self.assertEqual(
            errors['dataGrid'][2]['textField']['required'],
            'Text Field is required'
        )
        self.assertEqual(
            errors['dataGrid'][3],
            {}
        )

    def test_required_components_form_validation_errors_i18n_nl(self):
        errors = self.form_validation_errors_i18n_nl.validation_errors()

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
        self.assertEqual(
            errors['dataGrid'][1],
            {}
        )
        self.assertEqual(
            errors['dataGrid'][2]['textField']['required'],
            'Tekstveld is verplicht'
        )
        self.assertEqual(
            errors['dataGrid'][3],
            {}
        )

    def test_not_required_components_form(self):
        errors = self.form_validation_errors_i18n_nl.validation_errors()
        self.assertNotIn('email', errors)
