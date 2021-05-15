# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import json
import unittest

from tests.utils import readfile
from formiodata.builder import Builder
from formiodata.form import Form
from formiodata.components import textfieldComponent, passwordComponent


class ConditionalVisbilitySimpleTestCase(unittest.TestCase):
    def setUp(self):
        super(ConditionalVisbilitySimpleTestCase, self).setUp()

        self.builder_json = readfile('data', 'test_conditional_visibility_simple_builder.json')
        self.hide_password_form_json = readfile('data', 'test_conditional_visibility_simple_hide_password.json')
        self.show_textfield_form_json = readfile('data', 'test_conditional_visibility_simple_show_textfield.json')


    def test_conditionally_shown_form_elements_have_default_state_in_builder(self):
        builder = Builder(self.builder_json)

        self.assertTrue(builder.input_components['textField'].is_visible)
        self.assertFalse(builder.input_components['maybeTextField'].is_visible)
        self.assertTrue(builder.input_components['maybePassword'].is_visible)


    def test_conditionally_shown_form_elements_toggle_on_condition_being_met(self):
        builder = Builder(self.builder_json)

        hide_password_form = Form(self.hide_password_form_json, builder)
        self.assertTrue(hide_password_form.input_components['textField'].is_visible)
        self.assertFalse(hide_password_form.input_components['maybeTextField'].is_visible)
        self.assertFalse(hide_password_form.input_components['maybePassword'].is_visible)

        show_textfield_form = Form(self.show_textfield_form_json, builder)
        self.assertTrue(show_textfield_form.input_components['textField'].is_visible)
        self.assertTrue(show_textfield_form.input_components['maybeTextField'].is_visible)
        self.assertTrue(show_textfield_form.input_components['maybePassword'].is_visible)


    def test_conditionally_shown_form_elements_do_not_render_when_hidden(self):
        builder = Builder(self.builder_json)

        hide_password_form = Form(self.hide_password_form_json, builder)
        hide_password_form.render_components()
        self.assertEqual('<p>hide!</p>', hide_password_form.input_components['textField'].html_component)
        self.assertEqual('', hide_password_form.input_components['maybeTextField'].html_component)
        self.assertEqual('', hide_password_form.input_components['maybePassword'].html_component)

        show_textfield_form = Form(self.show_textfield_form_json, builder)
        show_textfield_form.render_components()
        self.assertEqual('<p>show!</p>', show_textfield_form.input_components['textField'].html_component)
        self.assertEqual('<p>maybe yes</p>', show_textfield_form.input_components['maybeTextField'].html_component)
        self.assertEqual('<p>hunter2</p>', show_textfield_form.input_components['maybePassword'].html_component)
