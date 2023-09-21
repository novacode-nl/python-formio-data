# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import json

from test_common import CommonTestCase
from formiodata.builder import Builder
from formiodata.components.editgrid import editgridComponent


class ComponentClassMappingTestCase(CommonTestCase):

    def setUp(self):
        super().setUp()

        schema_dict = json.loads(self.builder_json)
        for comp in schema_dict['components']:
            if comp['key'] == 'editGrid':
                comp['type'] = 'custom_editgrid'

        self.schema_json_component_class_mapping = json.dumps(schema_dict)

    def test_component_class_mapping_with_class(self):
        component_class_mapping = {'custom_editgrid': editgridComponent}
        builder = Builder(
            self.schema_json_component_class_mapping,
            component_class_mapping=component_class_mapping,
        )
        custom_editgrid = builder.components['editGrid']
        self.assertIsInstance(custom_editgrid, editgridComponent)
        self.assertEqual(custom_editgrid.type, 'custom_editgrid')

    def test_component_class_mapping_with_string(self):
        component_class_mapping = {'custom_editgrid': 'editgrid'}
        builder = Builder(
            self.schema_json_component_class_mapping,
            component_class_mapping=component_class_mapping,
        )
        custom_editgrid = builder.components['editGrid']
        self.assertIsInstance(custom_editgrid, editgridComponent)
        self.assertEqual(custom_editgrid.type, 'custom_editgrid')
