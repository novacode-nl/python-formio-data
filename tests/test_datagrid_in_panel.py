# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import unittest

from tests.utils import readfile

from formiodata.builder import Builder
from formiodata.form import Form


# Regression test for #17
class DatagridInPanelTestcase(unittest.TestCase):
    def setUp(self):
        super(DatagridInPanelTestcase, self).setUp()

        self.builder_json = readfile('data', 'test_datagrid_in_panel_builder.json')
        self.one_row_form_json = readfile('data', 'test_datagrid_in_panel_one_row_form.json')

    def test_default_state_in_builder_has_one_row(self):
        builder = Builder(self.builder_json)
        self.assertEqual({'panel', 'submit'}, set(builder.components.keys()))

        panel = builder.components['panel']
        self.assertEqual({'dataGrid'}, set(panel.components.keys()))

        datagrid = builder.components['panel'].components['dataGrid']
        self.assertEqual({'textField'}, set(datagrid.components.keys()))

        # datagrid will have no visible rows when initialized
        self.assertTrue(datagrid.initEmpty)
        self.assertEqual(len(datagrid.rows), 0)


    def test_form_with_one_row_has_the_one_row_created_by_submission(self):
        builder = Builder(self.builder_json)

        form = Form(self.one_row_form_json, builder)
        self.assertEqual({'panel', 'submit'}, set(form.components.keys()))

        panel = form.components['panel']
        self.assertEqual({'dataGrid'}, set(panel.components.keys()))

        datagrid = form.components['panel'].components['dataGrid']
        self.assertEqual({'textField'}, set(datagrid.components.keys()))
        self.assertEqual(len(datagrid.rows), 1)
