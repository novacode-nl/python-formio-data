# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import json
import unittest
import sys
sys.path.append('..')
from utils import readfile
from builder import Builder
from submission import Submission


class CommonTestCase(unittest.TestCase):

    def setUp(self):
        super(CommonTestCase, self).setUp()

        # test_example_builder.json
        # - shown: https://formio.github.io/formio.js/
        # - source: https://examples.form.io/example
        self.builder_json = readfile('tests/data', 'test_example_builder.json')
        self.submission_json = readfile('tests/data', 'test_example_submission.json')

        # self.builder = Builder(self.builder_json)
        # self.submission = Submission(self.submission_json, None, self.builder_json)
