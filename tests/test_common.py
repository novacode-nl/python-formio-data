# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import json
import unittest
import sys

from tests.utils import readfile
from formiodata.builder import Builder
from formiodata.form import Form


class CommonTestCase(unittest.TestCase):

    def setUp(self):
        super(CommonTestCase, self).setUp()

        # test_example_builder.json
        # - shown: https://formio.github.io/formio.js/
        # - source: https://examples.form.io/example
        self.builder_json = readfile('data', 'test_example_builder.json')
        self.builder_resource = readfile('data', 'test_example_builder_with_resource.json')
        self.builder_with_resource = readfile('data', 'test_example_builder_with_resource.json')
        self.form_json = readfile('data', 'test_example_form.json')
        self.form_empty_json = readfile('data', 'test_example_form_empty.json')
        self.form_json_check_default = readfile('data', 'test_example_form_check_default.json')
        self.form_with_resource = readfile("data", "test_example_form_with_resource.json")
        self.builder_json_resource = readfile('data', 'test_resources_submission.json')

        # self.builder = Builder(self.builder_json)
        # self.form = Form(self.form_json, None, self.builder_json)
