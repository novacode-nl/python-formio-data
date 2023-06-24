# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import logging
import os

def readfile(dir_path, filename):
    cwd = os.path.dirname(os.path.realpath(__file__))
    path = '%s/%s/%s' % (cwd, dir_path, filename)
    with open(path, "r") as fp:
        return fp.read()

def log_unittest(unittest_obj, msg, log_level='info'):
    log = '%s %s' % (log_level.upper(), unittest_obj.id())
    if unittest_obj.shortDescription():
        log += ' -- %s' % unittest_obj.shortDescription()
    log += ' - %s' % msg
    getattr(logging, log_level)(log)


class ConditionalVisibilityTestHelpers:
    def setUp(self):
        super(ConditionalVisibilityTestHelpers, self).setUp()
        try:
            from json_logic import jsonLogic
            self._have_json_logic = True
        except ImportError:
            self._have_json_logic = False

    def assertVisible(self, component):
        self.assertTrue(component.conditionally_visible)

    def assertNotVisible(self, component):
        if component.raw['conditional'].get('json') and not self._have_json_logic:
            # Without json_logic, all components with json conditionals
            # are considered always visible
            self.assertTrue(component.conditionally_visible)
        else:
            self.assertFalse(component.conditionally_visible)
