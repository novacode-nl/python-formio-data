# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from test_component import ComponentTestCase
from formiodata.components.number import numberComponent


class numberComponentTestCase(ComponentTestCase):

    def test_object(self):
        howManySeats = self.builder.input_components['howManySeats']
        self.assertIsInstance(howManySeats, numberComponent)

        # Not numberComponent
        firstName = self.builder.input_components['firstName']
        self.assertNotIsInstance(firstName, numberComponent)

    def test_get_key(self):
        howManySeats = self.builder.input_components['howManySeats']
        self.assertEqual(howManySeats.key, 'howManySeats')

    def test_get_type(self):
        howManySeats = self.builder.input_components['howManySeats']
        self.assertEqual(howManySeats.type, 'number')

    def test_get_label(self):
        howManySeats = self.builder.input_components['howManySeats']
        self.assertEqual(howManySeats.label, 'How Many Seats?')

    def test_set_label(self):
        howManySeats = self.builder.input_components['howManySeats']
        self.assertEqual(howManySeats.label, 'How Many Seats?')
        howManySeats.label = 'Foobar?'
        self.assertEqual(howManySeats.label, 'Foobar?')

    def test_get_form(self):
        howManySeats = self.form.input_components['howManySeats']
        self.assertEqual(howManySeats.label, 'How Many Seats?')
        self.assertEqual(howManySeats.value, 4)
        self.assertEqual(howManySeats.type, 'number')

    def test_get_form_data(self):
        howManySeats = self.form.input.howManySeats
        self.assertEqual(howManySeats.label, 'How Many Seats?')
        self.assertEqual(howManySeats.value, 4)
        self.assertEqual(howManySeats.type, 'number')
