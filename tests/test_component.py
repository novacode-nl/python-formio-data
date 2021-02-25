# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.
import json

from test_common import CommonTestCase
from formiodata.builder import Builder
from formiodata.form import Form


class ComponentTestCase(CommonTestCase):

    def setUp(self):
        super(ComponentTestCase, self).setUp()
        self.builder = Builder(self.builder_json)
        self.form = Form(self.form_json, self.builder)

        self.builder_i18n_nl = Builder(self.builder_json, language='nl', i18n=self._i18n())
        self.form_i18n_nl = Form(self.form_json, self.builder_i18n_nl)

    def _i18n(self):
        return  {
            'nl': {
                'First Name': 'Voornaam',
                'Last Name': 'Achternaam',
                'Appointment Date / Time': 'Afspraak Tijdstip',
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
                'Upload Base64': 'Upload binair naar ASCII',
                'Upload Url': 'Upload naar locatie'
            }
        }

    def test_schema_dict(self):
        builder_json = json.loads(self.builder_json)
        form_json = json.loads(self.form_json)
        self.builder = Builder(builder_json)
        self.form = Form(form_json, self.builder)

        self.builder_i18n_nl = Builder(builder_json, language='nl', i18n=self._i18n())
        self.form_i18n_nl = Form(form_json, self.builder_i18n_nl)



