# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import json
import unittest
import sys

from utils import readfile
from formiodata.builder import Builder
from formiodata.form import Form


class CommonTestCase(unittest.TestCase):

    def setUp(self):
        super(CommonTestCase, self).setUp()

        # test_example_builder.json
        # - shown: https://formio.github.io/formio.js/
        # - source: https://examples.form.io/example
        self.builder_json = readfile('data', 'test_example_builder.json')
        self.form_json = readfile('data', 'test_example_form.json')

        # self.builder = Builder(self.builder_json)
        # self.form = Form(self.form_json, None, self.builder_json)
