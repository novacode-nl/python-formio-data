# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import logging
import time
import unittest

from tests.utils import readfile
from formiodata.builder import Builder


class PerformanceNestedTestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='\n%(message)s', level=logging.INFO)

    def setUp(self):
        super(PerformanceNestedTestCase, self).setUp()
        self.builder_json = readfile('data', 'test_nested_components_builder.json')
        self.form_json = readfile('data', 'test_nested_components_form.json')

    def load_builders_range(self, range_num, load_path_objects):
        start = time.time()
        builders = {}
        for n in range(range_num):
            builders[n] = Builder(self.builder_json, load_path_objects=load_path_objects)
        end = time.time()
        msg_lines = [
            '----------------------------------------',
            'Load Builders range: %s' % range_num,
            'Duration: %s' % str(end - start),
            '----------------------------------------'
        ]
        self.logger.info('\n'.join(msg_lines))
        # self.logger.info(end - start)

    def test_Builder_component_with_path_objects(self):
        """ Builder: component path objects """

        msg_lines = [
            '========================================',
            'Load Builder WITH path objects',
            '========================================',
        ]
        self.logger.info('\n'.join(msg_lines))
        self.load_builders_range(10, load_path_objects=True)
        self.load_builders_range(100, load_path_objects=True)
        self.load_builders_range(1000, load_path_objects=True)

    def test_Builder_component_no_path_objects(self):
        """ Builder: component NO path objects """

        msg_lines = [
            '========================================',
            'Load Builder NO path objects',
            '========================================',
        ]
        self.logger.info('\n'.join(msg_lines))
        self.load_builders_range(10, load_path_objects=False)
        self.load_builders_range(100, load_path_objects=False)
        self.load_builders_range(1000, load_path_objects=False)
