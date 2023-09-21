# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from test_component import ComponentTestCase
from formiodata.components.file import fileComponent


class fileComponentStorageUrlTestCase(ComponentTestCase):

    def setUp(self):
        super(fileComponentStorageUrlTestCase, self).setUp()

        self.image_url = 'https://avatars1.githubusercontent.com/u/31220867?s=50'
        self.image_value_base64 = 'data:image/png;base64,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'

    def test_object(self):
        uploadUrl = self.builder.input_components['uploadUrl']
        self.assertIsInstance(uploadUrl, fileComponent)

        # Not fileComponent
        email = self.builder.input_components['email']
        self.assertNotIsInstance(email, fileComponent)

    def test_get_key(self):
        uploadUrl = self.builder.input_components['uploadUrl']
        self.assertEqual(uploadUrl.key, 'uploadUrl')

    def test_get_type(self):
        uploadUrl = self.builder.input_components['uploadUrl']
        self.assertEqual(uploadUrl.type, 'file')

    def test_get_label(self):
        uploadUrl = self.builder.input_components['uploadUrl']
        self.assertEqual(uploadUrl.label, 'Upload Url')

    def test_set_label(self):
        uploadUrl = self.builder.input_components['uploadUrl']
        self.assertEqual(uploadUrl.label, 'Upload Url')
        uploadUrl.label = 'RAW Image'
        self.assertEqual(uploadUrl.label, 'RAW Image')

    def test_get_form(self):
        uploadUrl = self.form.components['uploadUrl']
        self.assertEqual(uploadUrl.label, 'Upload Url')
        self.assertEqual(uploadUrl.type, 'file')
        self.assertEqual(uploadUrl.storage, 'url')
        self.assertUrlBase64(uploadUrl, self.image_value_base64)

        
    def test_get_form_data(self):
        uploadUrl = self.form.input.uploadUrl
        self.assertEqual(uploadUrl.label, 'Upload Url')
        self.assertEqual(uploadUrl.type, 'file')
        self.assertEqual(uploadUrl.storage, 'url')
        self.assertUrlBase64(uploadUrl, self.image_value_base64)

    # i18n translations
    def test_get_label_i18n_nl(self):
        uploadUrl = self.builder_i18n_nl.input_components['uploadUrl']
        self.assertEqual(uploadUrl.label, 'Upload naar locatie')

    def test_get_form_data_i18n_nl(self):
        self.assertEqual(self.form_i18n_nl.input.uploadUrl.label, 'Upload naar locatie')
