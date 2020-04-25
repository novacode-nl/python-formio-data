# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from test_common import CommonTestCase
from formiodata.builder import Builder


class BuilderTestCase(CommonTestCase):

    def _builder(self):
        return Builder(self.builder_json)

    def test_builder(self):
        Builder(self.builder_json)

    def test_components(self):
        builder = self._builder()
        keys = ('firstName', 'email', 'lastName', 'phoneNumber', 'survey', 'signature', 'submit')
        for k in keys:
            self.assertIn(k, builder.form_components.keys())
