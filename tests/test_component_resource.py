# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from formiodata.builder import Builder
from formiodata.components.resource import resourceComponent
from formiodata.form import Form
from tests.test_component import ComponentTestCase


class resourceComponentTestCase(ComponentTestCase):

    def setUp(self):
        super(resourceComponentTestCase, self).setUp()
        self.builder_res = Builder(self.builder_with_resource, resources=self.builder_json_resource)
        self.form_res = Form(self.form_with_resource, self.builder_res)

    def test_object(self):
        # TextfieldComponent
        res = self.builder_res.input_components['resourceObj']
        self.assertIsInstance(res, resourceComponent)

    def test_get_key(self):
        res = self.builder_res.input_components['resourceObj']
        self.assertEqual(res.key, 'resourceObj')

    def test_get_type(self):
        res = self.builder_res.input_components['resourceObj']
        self.assertEqual(res.type, 'resource')

    def test_values(self):
        res = self.builder_res.input_components['resourceObj']
        self.assertEqual(len(res.values), 4)

    def test_first_value(self):
        res = self.builder_res.input_components['resourceObj']
        self.assertEqual(res.values[1], {'label': 'ResB', 'value': '60034ec3942c74ca500b32b1'})
