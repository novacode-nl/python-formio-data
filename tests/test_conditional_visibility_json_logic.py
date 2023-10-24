# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import unittest

from tests.utils import readfile, ConditionalVisibilityTestHelpers
from formiodata.builder import Builder
from formiodata.form import Form


class ConditionalVisibilityJsonLogicTestCase(ConditionalVisibilityTestHelpers, unittest.TestCase):
    def setUp(self):
        super(ConditionalVisibilityJsonLogicTestCase, self).setUp()

        self.builder_json = readfile('data', 'test_conditional_visibility_json_logic_builder.json')
        self.hide_secret_form_json = readfile('data', 'test_conditional_visibility_json_logic_hide_secret.json')
        self.show_secret_form_json = readfile('data', 'test_conditional_visibility_json_logic_show_secret.json')

    def test_conditionally_shown_components_have_default_state_in_builder(self):
        builder = Builder(self.builder_json)

        self.assertVisible(builder.input_components['username'])
        self.assertVisible(builder.input_components['password'])
        self.assertNotVisible(builder.input_components['secret'])

    def test_conditionally_shown_components_toggle_on_condition_being_met(self):
        builder = Builder(self.builder_json)

        hide_secret_form = Form(self.hide_secret_form_json, builder)
        self.assertVisible(hide_secret_form.input_components['username'])
        self.assertVisible(hide_secret_form.input_components['password'])
        self.assertNotVisible(hide_secret_form.input_components['secret'])

        show_secret_form = Form(self.show_secret_form_json, builder)
        self.assertVisible(show_secret_form.input_components['username'])
        self.assertVisible(show_secret_form.input_components['password'])
        self.assertVisible(show_secret_form.input_components['secret'])

    def test_conditionally_shown_components_do_not_render_when_hidden(self):
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
