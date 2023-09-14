from formiodata.form import Form
from test_component import ComponentTestCase


class valueDefaultEmailComponent(ComponentTestCase):

    def test_default_value(self):
        self.form_check_default = Form(self.form_json_check_default, self.builder)
        # EmailComponent
        email = self.form_check_default.input_components['email']
        self.assertEqual(email.value, 'yourmail@yourlife.io')
