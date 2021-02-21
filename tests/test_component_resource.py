# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.
import json

from formiodata.builder import Builder
from formiodata.components import resourceComponent
from formiodata.form import Form
from tests.test_component import ComponentTestCase


class resourceComponentTestCase(ComponentTestCase):

    def external_recource(self, id):
        resources = json.loads(self.builder_json_resource)
        return resources[id]

    def setUp(self):
        super(resourceComponentTestCase, self).setUp()
        self.builder_res = Builder(self.builder_with_resource, resources=self.builder_json_resource)
        self.form_res = Form(self.form_with_resource, self.builder_res)

    def test_object(self):
        # resourceComponent
        res = self.builder_res.form_components['resourceObj']
        self.assertIsInstance(res, resourceComponent)

    def test_get_key(self):
        res = self.builder_res.form_components['resourceObj']
        self.assertEqual(res.key, 'resourceObj')

    def test_get_type(self):
        res = self.builder_res.form_components['resourceObj']
        self.assertEqual(res.type, 'resource')

    def test_values(self):
        res = self.builder_res.form_components['resourceObj']
        self.assertEqual(len(res.values), 4)

    def test_first_value(self):
        res = self.builder_res.form_components['resourceObj']
        self.assertEqual(res.values[1], {'label': 'ResB', 'value': {'$oid': '60034ec3942c74ca500b32b1'}} )

    def test_ext_resources(self):
        self.builder_res_ext = Builder(self.builder_with_resource, resources_ext=self.external_recource)
        self.form_res = Form(self.form_with_resource, self.builder_res_ext)
        res = self.builder_res_ext.form_components['resourceObj']
        self.assertIsInstance(res, resourceComponent)
        res = self.builder_res_ext.form_components['resourceObj']
        self.assertEqual(len(res.values), 4)
        self.assertEqual(res.values[1], {'label': 'ResB', 'value': {'$oid': '60034ec3942c74ca500b32b1'}} )
