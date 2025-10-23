# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from test_component import ComponentTestCase
from tests.utils import readfile
from formiodata.builder import Builder
from formiodata.form import Form
from formiodata.components.select import selectComponent


class selectOneDataSrcUrlComponentTestCase(ComponentTestCase):

    def setUp(self):
        super(selectOneDataSrcUrlComponentTestCase, self).setUp()

        self.builder_json = readfile('data', 'test_data_src_url_builder.json')
        self.builder = Builder(self.builder_json)
        self.form_no_value_json = readfile('data', 'test_data_src_url_form_no_value.json')
        self.form_no_value = Form(self.form_no_value_json, self.builder)

    def test_object(self):
        # selectComponent
        country = self.builder.input_components['country']
        self.assertIsInstance(country, selectComponent)

    def test_key(self):
        country = self.builder.input_components['country']
        self.assertEqual(country.key, 'country')

    def test_type(self):
        country = self.builder.input_components['country']
        self.assertEqual(country.type, 'select')

    def test_data_rc(self):
        country = self.builder.input_components['country']
        self.assertEqual(country.dataSrc, 'url')

    def test_label(self):
        country = self.builder.input_components['country']
        self.assertEqual(country.label, 'Country')

    def test_form(self):
        country = self.form_no_value.input_components['country']
        self.assertEqual(country.type, 'select')
        self.assertEqual(country.label, 'Country')
        self.assertEqual(country.value, {})
        self.assertEqual(country.raw_value, '')
        self.assertEqual(country.value_label, None)

    def test_form_data(self):
        country = self.form_no_value.input.country
        self.assertEqual(country.type, 'select')
        self.assertEqual(country.label, 'Country')
        self.assertEqual(country.value, {})
        self.assertEqual(country.raw_value, '')
        self.assertEqual(country.value_label, None)
