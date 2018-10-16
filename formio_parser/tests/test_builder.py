# -*- coding: utf-8 -*-
# Copyright 2018 Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from .test_common import CommonTestCase


class BuilderTestCase(CommonTestCase):

    def test_components(self):
        keys = ('firstName', 'email', 'lastName', 'phoneNumber', 'survey', 'signature', 'submit')

        for key, comp in self.builder.components.items():
            self.assertIn(key, keys)

        for key in keys:
            self.assertIn(key, self.builder.components)
