# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from test_common import CommonTestCase
from formiodata.builder import Builder
from formiodata.form import Form


class ComponentTestCase(CommonTestCase):

    def setUp(self):
        super(ComponentTestCase, self).setUp()
        self.builder = Builder(self.builder_json)
        self.form = Form(self.form_json, self.builder)

        i18n = {
            'nl': {
                'First Name': 'Voornaam',
                'Last Name': 'Achternaam',
                'Survey': 'Enquête',
                'excellent': 'uitstekend',
                'great': 'supergoed',
                'My Favourites': 'Mijn favorieten',
                'Favourite Season': 'Favoriete seizoen',
                'Autumn': 'Herfst',
                'Favourite Food': 'Lievelingseten',
            }
        }
        self.builder_i18n_nl = Builder(self.builder_json, language='nl', i18n=i18n)
        self.form_i18n_nl = Form(self.form_json, self.builder_i18n_nl)
