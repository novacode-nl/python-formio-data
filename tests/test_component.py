# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from test_common import CommonTestCase
from formiodata.builder import Builder
from formiodata.form import Form


class ComponentTestCase(CommonTestCase):

    def setUp(self):
        super(ComponentTestCase, self).setUp()
        self.builder = Builder(self.builder_json)
        self.form = Form(self.form_json, self.builder)
