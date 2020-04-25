# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from test_common import CommonTestCase
from formiodata.submission import Submission


class SubmissionTestCase(CommonTestCase):

    def x_test_constructor_validation_ok(self):
        sub = Submission(self.submission_json, None, self.builder_json)
        self.assertIsInstance(sub, Submission)

        sub = Submission(self.submission_json, self.builder)
        self.assertIsInstance(sub, Submission)
        # self.assertIsInstance(self.submission.store, SubmissionStore)

    def x_test_constructor_validation_fails(self):
        with self.assertRaisesRegexp(Exception, "Provide either the argument: builder or builder_schema_json."):
            Submission(self.submission_json)

        with self.assertRaisesRegexp(Exception, "Constructor accepts either builder or builder_schema_json."):
            Submission(self.submission_json, self.builder, self.builder_schema_json)
