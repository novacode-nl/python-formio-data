# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from test_common import CommonTestCase
from builder import Builder
from submission import Submission


class ComponentTestCase(CommonTestCase):

    def setUp(self):
        super(ComponentTestCase, self).setUp()
        self.builder = Builder(self.builder_json)
        self.submission = Submission(self.submission_json, self.builder)
