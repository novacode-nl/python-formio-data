# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import json
import unittest

from tests.utils import readfile
from formiodata.builder import Builder
from formiodata.form import Form
from formiodata.components import textfieldComponent, passwordComponent


class ConditionalVisibilityJsonLogicTestCase(unittest.TestCase):
    def setUp(self):
        super(ConditionalVisibilityJsonLogicTestCase, self).setUp()

        self.builder_json = readfile('data', 'test_conditional_visibility_json_logic_builder.json')
        self.hide_secret_form_json = readfile('data', 'test_conditional_visibility_json_logic_hide_secret.json')
        self.show_secret_form_json = readfile('data', 'test_conditional_visibility_json_logic_show_secret.json')


    def test_conditionally_shown_form_elements_have_default_state_in_builder(self):
        builder = Builder(self.builder_json)

        self.assertTrue(builder.input_components['username'].conditionally_visible)
        self.assertTrue(builder.input_components['password'].conditionally_visible)
        self.assertFalse(builder.input_components['secret'].conditionally_visible)


    def test_conditionally_shown_form_elements_toggle_on_condition_being_met(self):
        builder = Builder(self.builder_json)

        hide_secret_form = Form(self.hide_secret_form_json, builder)
        self.assertTrue(hide_secret_form.input_components['username'].conditionally_visible)
        self.assertTrue(hide_secret_form.input_components['password'].conditionally_visible)
        self.assertFalse(hide_secret_form.input_components['secret'].conditionally_visible)

        show_secret_form = Form(self.show_secret_form_json, builder)
        self.assertTrue(show_secret_form.input_components['username'].conditionally_visible)
        self.assertTrue(show_secret_form.input_components['password'].conditionally_visible)
        self.assertTrue(show_secret_form.input_components['secret'].conditionally_visible)


    def test_conditionally_shown_form_elements_do_not_render_when_hidden(self):
        builder = Builder(self.builder_json)

        hide_secret_form = Form(self.hide_secret_form_json, builder)
        hide_secret_form.render_components()
        self.assertEqual('<p>wrong</p>', hide_secret_form.input_components['username'].html_component)
        self.assertEqual('<p>incorrect</p>', hide_secret_form.input_components['password'].html_component)
        self.assertEqual('', hide_secret_form.input_components['secret'].html_component)

        show_secret_form = Form(self.show_secret_form_json, builder)
        show_secret_form.render_components()
        self.assertEqual('<p>user</p>', show_secret_form.input_components['username'].html_component)
        self.assertEqual('<p>secret</p>', show_secret_form.input_components['password'].html_component)
        self.assertEqual('<p>Secret message</p>', show_secret_form.input_components['secret'].html_component)
