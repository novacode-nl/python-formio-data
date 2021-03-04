# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import json
import unittest

from tests.utils import readfile
from formiodata.builder import Builder
from formiodata.form import Form


class nestingDatagridTestCase(unittest.TestCase):

    def setUp(self):
        super(nestingDatagridTestCase, self).setUp()
        self.builder_json = readfile('data', 'test_nesting_datagrid_builder.json')
        self.form_json = readfile('data', 'test_nesting_datagrid_form.json')
        self.builder = Builder(self.builder_json)
        self.form = Form(self.form_json, self.builder)

    def test_datagrid(self):
        # TODO implement component assertions (type, value, datagrid.rows)
        renderer = self.form.renderer
        panel = renderer.components[0]
        firstname = panel.children[0].children[0]
        lastname = panel.children[0].children[1]
        
        datagrid = panel.children[0].children[2]

        rows = []
        for row in datagrid.rows:
            rows.append([slot.value for slot in row])
