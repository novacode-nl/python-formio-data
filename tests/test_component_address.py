# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from test_component import ComponentTestCase
from formiodata.components.address import addressComponent


class addressComponentTestCase(ComponentTestCase):

    def test_object(self):
        address = self.builder.input_components['deliveryAddress']
        self.assertIsInstance(address, addressComponent)

        # Not addressComponent
        email = self.builder.input_components['email']
        self.assertNotIsInstance(email, addressComponent)

    def test_get_form_empty_address(self):
        address = self.form_empty.input_components['deliveryAddress']
        self.assertEqual(address.type, 'address')
        self.assertEqual(address.label, 'Delivery Address')
        self.assertIsInstance(address.value, dict)
        self.assertEqual(address.value, {})

        # parts
        # TODO lat, lon (coordinates)
        self.assertIsNone(address.postal_code)
        self.assertIsNone(address.street_name)
        self.assertIsNone(address.street_number)
        self.assertIsNone(address.city)
        self.assertIsNone(address.country)

    def test_get_form_address(self):
        address = self.form.input_components['deliveryAddress']
        self.assertEqual(address.type, 'address')
        self.assertEqual(address.label, 'Delivery Address')
        self.assertIsNotNone(address.value)

        # parts
        # TODO lat, lon (coordinates)
        self.assertEqual(address.postal_code, '1017 CT')
        self.assertEqual(address.street_name, 'Rembrandtplein')
        self.assertEqual(address.street_number, '33')
        self.assertEqual(address.city, 'Amsterdam')
        self.assertEqual(address.country, 'Netherlands')
        self.assertEqual(address.country_code, 'NL')

    # i18n translations
    def test_get_label_i18n_nl(self):
        address = self.builder_i18n_nl.input_components['deliveryAddress']
        self.assertEqual(address.label, 'Afleveradres')

    def test_get_form_data_i18n_nl(self):
        self.assertEqual(self.form_i18n_nl.input.deliveryAddress.label, 'Afleveradres')
