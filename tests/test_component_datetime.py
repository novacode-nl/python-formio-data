# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from datetime import datetime, date

from test_component import ComponentTestCase
from formiodata.components.datetime import datetimeComponent


class datetimeComponentTestCase(ComponentTestCase):

    def test_object(self):
        # datetimeComponent
        birthdate = self.builder.input_components['birthdate']
        self.assertIsInstance(birthdate, datetimeComponent)

        appointmentDateTime = self.builder.input_components['appointmentDateTime']
        self.assertIsInstance(appointmentDateTime, datetimeComponent)

        # Not datetimeComponent
        email = self.builder.input_components['email']
        self.assertNotIsInstance(email, datetimeComponent)

    def test_get_key(self):
        birthdate = self.builder.input_components['birthdate']
        self.assertEqual(birthdate.key, 'birthdate')

        appointmentDateTime = self.builder.input_components['appointmentDateTime']
        self.assertEqual(appointmentDateTime.key, 'appointmentDateTime')

    def test_get_type(self):
        birthdate = self.builder.input_components['birthdate']
        self.assertEqual(birthdate.type, 'datetime')

        appointmentDateTime = self.builder.input_components['appointmentDateTime']
        self.assertEqual(appointmentDateTime.type, 'datetime')

    def test_get_label(self):
        birthdate = self.builder.input_components['birthdate']
        self.assertEqual(birthdate.label, 'Birthdate')

        appointmentDateTime = self.builder.input_components['appointmentDateTime']
        self.assertEqual(appointmentDateTime.label, 'Appointment Date / Time')

    def test_set_label(self):
        birthdate = self.builder.input_components['birthdate']
        self.assertEqual(birthdate.label, 'Birthdate')
        birthdate.label = 'Born On'
        self.assertEqual(birthdate.label, 'Born On')

        appointmentDateTime = self.builder.input_components['appointmentDateTime']
        self.assertEqual(appointmentDateTime.label, 'Appointment Date / Time')
        appointmentDateTime.label = 'Appointment On'
        self.assertEqual(appointmentDateTime.label, 'Appointment On')

    def test_get_form(self):
        birthdate = self.form.input_components['birthdate']
        self.assertEqual(birthdate.label, 'Birthdate')
        self.assertEqual(birthdate.value, '1999-12-31')
        self.assertEqual(birthdate.type, 'datetime')

        appointmentDateTime = self.form.input_components['appointmentDateTime']
        self.assertEqual(appointmentDateTime.label, 'Appointment Date / Time')
        self.assertEqual(appointmentDateTime.value, '2021-02-26 12:30 PM')
        self.assertEqual(appointmentDateTime.type, 'datetime')

    def test_get_form_data(self):
        birthdate = self.form.input.birthdate
        self.assertEqual(birthdate.label, 'Birthdate')
        self.assertEqual(birthdate.value, '1999-12-31')
        self.assertEqual(birthdate.type, 'datetime')

        appointmentDateTime = self.form.input.appointmentDateTime
        self.assertEqual(appointmentDateTime.label, 'Appointment Date / Time')
        self.assertEqual(appointmentDateTime.value, '2021-02-26 12:30 PM')
        self.assertEqual(appointmentDateTime.type, 'datetime')

    def test_to_datetime(self):
        birthdate = self.form.input.birthdate
        self.assertIsInstance(birthdate.to_datetime(), datetime)
        self.assertIsInstance(birthdate.to_datetime().date(), date)

        appointmentDateTime = self.form.input.appointmentDateTime
        self.assertIsInstance(appointmentDateTime.to_datetime(), datetime)

    # i18n translations
    def test_get_label_i18n_nl(self):
        appointmentDateTime = self.builder_i18n_nl.input_components['appointmentDateTime']
        self.assertEqual(appointmentDateTime.label, 'Afspraak Tijdstip')

    def test_get_form_data_i18n_nl(self):
        self.assertEqual(self.form_i18n_nl.input.appointmentDateTime.label, 'Afspraak Tijdstip')
