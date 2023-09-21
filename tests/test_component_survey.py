# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from test_component import ComponentTestCase
from formiodata.components.survey import surveyComponent


class surveyComponentTestCase(ComponentTestCase):

    def test_object(self):
        # surveyComponent
        survey = self.builder.input_components['survey']
        self.assertIsInstance(survey, surveyComponent)

        # Not surveyComponent
        firstName = self.builder.input_components['firstName']
        self.assertNotIsInstance(firstName, surveyComponent)

    def test_get_key(self):
        survey = self.builder.input_components['survey']
        self.assertEqual(survey.key, 'survey')

    def test_get_type(self):
        survey = self.builder.input_components['survey']
        self.assertEqual(survey.type, 'survey')

    def test_get_label(self):
        survey = self.builder.input_components['survey']
        self.assertEqual(survey.label, 'Survey')

    def test_set_label(self):
        survey = self.builder.input_components['survey']
        self.assertEqual(survey.label, 'Survey')
        survey.label = 'Foobar'
        self.assertEqual(survey.label, 'Foobar')

    def test_get_form(self):
        survey = self.form.components['survey']
        self.assertEqual(survey.label, 'Survey')
        self.assertEqual(survey.value['overallExperience'], 'excellent')
        self.assertEqual(survey.value['howWasCustomerSupport'], 'great')
        self.assertEqual(survey.value['howWouldYouRateTheFormIoPlatform'], 'excellent')
        self.assertEqual(survey.type, 'survey')

    def test_get_form_data(self):
        survey = self.form.input.survey
        self.assertEqual(survey.label, 'Survey')
        self.assertEqual(survey.value['overallExperience'], 'excellent')
        self.assertEqual(survey.value['howWasCustomerSupport'], 'great')
        self.assertEqual(survey.value['howWouldYouRateTheFormIoPlatform'], 'excellent')
        self.assertEqual(survey.type, 'survey')

    # i18n translations
    def test_get_label_i18n_nl(self):
        survey = self.builder_i18n_nl.input_components['survey']
        self.assertEqual(survey.label, 'Enquête')

    def test_get_form_data_i18n_nl(self):
        survey = self.form_i18n_nl.input.survey
        self.assertEqual(survey.label, 'Enquête')
        # TODO Labels for questions and values
        # self.assertEqual(survey.value['overallExperience'], 'uitstekend')
        # self.assertEqual(survey.value['howWasCustomerSupport'], 'super goed')
        # self.assertEqual(survey.value['howWouldYouRateTheFormIoPlatform'], 'uitstekend')
