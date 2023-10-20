# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import json

from requests.exceptions import ConnectionError

from tests.utils import log_unittest
from tests.test_common import CommonTestCase

from formiodata.builder import Builder
from formiodata.form import Form


class ComponentTestCase(CommonTestCase):

    def setUp(self):
        super(ComponentTestCase, self).setUp()
        self.builder = Builder(self.builder_json)
        self.form = Form(self.form_json, self.builder)
        self.form_empty = Form(self.form_empty_json, self.builder)

        self.builder_i18n_nl = Builder(self.builder_json, language='nl', i18n=self._i18n())
        self.form_i18n_nl = Form(self.form_json, self.builder_i18n_nl)
        self.form_empty_i18n_nl = Form(self.form_empty_json, self.builder_i18n_nl)

    def _i18n(self):
        return {
            'nl': {
                'First Name': 'Voornaam',
                'Last Name': 'Achternaam',
                'Appointment Date / Time': 'Afspraak Tijdstip',
                'Delivery Address': 'Afleveradres',
                'Survey': 'Enquête',
                'excellent': 'uitstekend',
                'great': 'supergoed',
                'My Favourites': 'Mijn favorieten',
                'Favourite Season': 'Favoriete seizoen',
                'Autumn': 'Herfst',
                'Favourite Food': 'Lievelingseten',
                'Cardinal Direction': 'Kardinale richting',
                'North': 'Noord',
                'East': 'Oost',
                'South': 'Zuid',
                'West': 'West',
                'Select Boxes': 'Select aanvink opties',
                'Month Day Year': 'Maand dag jaar',
                'Day Month Year': 'Dag maand jaar',
                'May': 'Mei',
                'Text Field': 'Tekstveld',
                'Upload Base64': 'Upload binair naar ASCII',
                'Upload Url': 'Upload naar locatie',
                '{{field}} is required': '{{field}} is verplicht'
            }
        }

    def test_schema_dict(self):
        builder_json = json.loads(self.builder_json)
        form_json = json.loads(self.form_json)
        self.builder = Builder(builder_json)
        self.form = Form(form_json, self.builder)

        self.builder_i18n_nl = Builder(builder_json, language='nl', i18n=self._i18n())
        self.form_i18n_nl = Form(form_json, self.builder_i18n_nl)

    def assertUrlBase64(self, component, expected_base64, log_level='warning'):
        try:
            self.assertEqual(component.base64, expected_base64)
        except ConnectionError as e:
            msg = 'Internet access is required, %s...\n%s' % (e.__class__.__name__, e)
            log_unittest(self, msg, log_level)
