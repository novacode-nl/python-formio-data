# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from test_common import CommonTestCase
from formiodata.form import Form


class FormTestCase(CommonTestCase):

    def x_test_constructor_validation_ok(self):
        sub = Form(self.form_json, None, self.builder_json)
        self.assertIsInstance(sub, Form)

        sub = Form(self.form_json, self.builder)
        self.assertIsInstance(sub, Form)
        # self.assertIsInstance(self.form.store, FormStore)

    def x_test_constructor_validation_fails(self):
        with self.assertRaisesRegexp(Exception, "Provide either the argument: builder or builder_schema_json."):
            Form(self.form_json)

        with self.assertRaisesRegexp(Exception, "Constructor accepts either builder or builder_schema_json."):
            Form(self.form_json, self.builder, self.builder_schema_json)
