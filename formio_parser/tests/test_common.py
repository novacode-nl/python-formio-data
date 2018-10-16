# -*- coding: utf-8 -*-
# Copyright 2018 Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import json
import unittest

from utils import readfile
from builder import Builder
from form import Form


class CommonTestCase(unittest.TestCase):

    def setUp(self):
        super(CommonTestCase, self).setUp()

        # test_example_builder.json
        # - shown: https://formio.github.io/formio.js/
        # - source: https://examples.form.io/example
        self.builder_json_str = readfile('tests/data', 'test_example_builder.json')
        self.form_json_str = readfile('tests/data', 'test_example_form.json')

        self.builder = Builder(self.builder_json_str)
        # self.form = Form(self.form_json, None, self.builder_json_str)
