# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from test_component import ComponentTestCase
from formiodata.components import surveyComponent


class SurveyComponentTestCase(ComponentTestCase):

    def test_object(self):
        # surveyComponent
        survey = self.builder.form_components['survey']
        self.assertIsInstance(survey, surveyComponent)

        # Not surveyComponent
        firstName = self.builder.form_components['firstName']
        self.assertNotIsInstance(firstName, surveyComponent)
        submit = self.builder.form_components['submit']
        self.assertNotIsInstance(submit, surveyComponent)

    def test_get_key(self):
        survey = self.builder.form_components['survey']
        self.assertEqual(survey.key, 'survey')

    def test_get_type(self):
        survey = self.builder.form_components['survey']
        self.assertEqual(survey.type, 'survey')

    def test_get_label(self):
        survey = self.builder.form_components['survey']
        self.assertEqual(survey.label, 'Survey')

    def test_set_label(self):
        survey = self.builder.form_components['survey']
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
        survey = self.form.data.survey
        self.assertEqual(survey.label, 'Survey')
        self.assertEqual(survey.value['overallExperience'], 'excellent')
        self.assertEqual(survey.value['howWasCustomerSupport'], 'great')
        self.assertEqual(survey.value['howWouldYouRateTheFormIoPlatform'], 'excellent')
        self.assertEqual(survey.type, 'survey')
