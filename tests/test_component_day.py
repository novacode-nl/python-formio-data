# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from collections import OrderedDict

from test_component import ComponentTestCase
from formiodata.components.day import dayComponent


class dayComponentTestCase(ComponentTestCase):

    def test_object(self):
        # dayComponent
        monthDayYear = self.builder.input_components['monthDayYear']
        self.assertIsInstance(monthDayYear, dayComponent)

        monthYear = self.builder.input_components['monthYear']
        self.assertIsInstance(monthYear, dayComponent)

        dayMonthYear = self.builder.input_components['dayMonthYear']
        self.assertIsInstance(dayMonthYear, dayComponent)

        dayMonth = self.builder.input_components['dayMonth']
        self.assertIsInstance(dayMonth, dayComponent)

        day = self.builder.input_components['day']
        self.assertIsInstance(day, dayComponent)

        month = self.builder.input_components['month']
        self.assertIsInstance(month, dayComponent)

        year = self.builder.input_components['year']
        self.assertIsInstance(year, dayComponent)

        # Not dayComponent
        email = self.builder.input_components['email']
        self.assertNotIsInstance(email, dayComponent)

    def test_get_form_empty_monthDayYear(self):
        monthDayYear = self.form_empty.input_components['monthDayYear']
        self.assertEqual(monthDayYear.type, 'day')
        self.assertEqual(monthDayYear.label, 'Month Day Year')
        self.assertIsInstance(monthDayYear.value, OrderedDict)
        self.assertEqual(monthDayYear.value, {'month': None, 'day': None, 'year': None})
        # parts
        self.assertIsNone(monthDayYear.day)
        self.assertIsNone(monthDayYear.month)
        self.assertIsNone(monthDayYear.year)

    def test_get_form_monthDayYear(self):
        monthDayYear = self.form.input_components['monthDayYear']
        self.assertEqual(monthDayYear.type, 'day')
        self.assertEqual(monthDayYear.label, 'Month Day Year')
        self.assertEqual(monthDayYear.value, {'month': 5, 'day': 16, 'year': 2021})
        # parts
        self.assertEqual(monthDayYear.day, 16)
        self.assertEqual(monthDayYear.month, 5)
        self.assertEqual(monthDayYear.month_name, 'May')
        self.assertEqual(monthDayYear.year, 2021)
        # extra test
        self.assertIsInstance(monthDayYear.value, OrderedDict)

    def test_get_form_monthYear(self):
        monthYear = self.form.input_components['monthYear']
        self.assertEqual(monthYear.type, 'day')
        self.assertEqual(monthYear.label, 'Month Year')
        self.assertEqual(monthYear.value, {'month': 5, 'month': 5, 'year': 2021})
        # parts
        self.assertIsNone(monthYear.day)
        self.assertEqual(monthYear.month, 5)
        self.assertEqual(monthYear.month_name, 'May')
        self.assertEqual(monthYear.year, 2021)

    def test_get_form_dayMonthYear(self):
        dayMonthYear = self.form.input_components['dayMonthYear']
        self.assertEqual(dayMonthYear.type, 'day')
        self.assertEqual(dayMonthYear.label, 'Day Month Year')
        self.assertEqual(dayMonthYear.value, {'day': 16, 'month': 5, 'year': 2021})
        # parts
        self.assertEqual(dayMonthYear.day, 16)
        self.assertEqual(dayMonthYear.month, 5)
        self.assertEqual(dayMonthYear.month_name, 'May')
        self.assertEqual(dayMonthYear.year, 2021)

    def test_get_form_dayMonth(self):
        dayMonth = self.form.input_components['dayMonth']
        self.assertEqual(dayMonth.type, 'day')
        self.assertEqual(dayMonth.label, 'Day Month')
        self.assertEqual(dayMonth.value, {'day': 16, 'month': 5})
        # parts
        self.assertEqual(dayMonth.day, 16)
        self.assertEqual(dayMonth.month, 5)
        self.assertEqual(dayMonth.month_name, 'May')
        self.assertIsNone(dayMonth.year)

    def test_get_form_day(self):
        day = self.form.input_components['day']
        self.assertEqual(day.type, 'day')
        self.assertEqual(day.label, 'Day')
        self.assertEqual(day.value, {'day': 16})
        # parts
        self.assertEqual(day.day, 16)
        self.assertIsNone(day.month)
        self.assertIsNone(day.year)

    def test_get_form_month(self):
        month = self.form.input_components['month']
        self.assertEqual(month.type, 'day')
        self.assertEqual(month.label, 'Month')
        self.assertEqual(month.value, {'month': 5})
        # parts
        self.assertIsNone(month.day)
        self.assertEqual(month.month, 5)
        self.assertEqual(month.month_name, 'May')
        self.assertIsNone(month.year)

    def test_get_form_year(self):
        year = self.form.input_components['year']
        self.assertEqual(year.type, 'day')
        self.assertEqual(year.label, 'Year')
        self.assertEqual(year.value, {'year': 2021})
        # parts
        self.assertIsNone(year.day)
        self.assertIsNone(year.month)
        self.assertEqual(year.year, 2021)

    # i18n translations
    def test_get_label_i18n_nl(self):
        # We won't test all here
        monthDayYear = self.builder_i18n_nl.input_components['monthDayYear']
        self.assertEqual(monthDayYear.label, 'Maand dag jaar')

        dayMonthYear = self.builder_i18n_nl.input_components['dayMonthYear']
        self.assertEqual(dayMonthYear.label, 'Dag maand jaar')

    def test_get_form_data_i18n_nl(self):
        self.assertEqual(self.form_i18n_nl.input.dayMonthYear.label, 'Dag maand jaar')

        monthDayYear = self.form_i18n_nl.input_components['monthDayYear']
        self.assertEqual(monthDayYear.month_name, 'Mei')

        dayMonthYear = self.form_i18n_nl.input_components['dayMonthYear']
        self.assertEqual(dayMonthYear.month_name, 'Mei')

        dayMonth = self.form_i18n_nl.input_components['dayMonth']
        self.assertEqual(dayMonth.month_name, 'Mei')

        monthYear = self.form_i18n_nl.input_components['monthYear']
        self.assertEqual(monthYear.month_name, 'Mei')

        month = self.form_i18n_nl.input_components['month']
        self.assertEqual(month.month_name, 'Mei')
