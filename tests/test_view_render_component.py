from formiodata.form import Form
from test_component import ComponentTestCase
from formiodata.components import emailComponent


class viewRenderEmailComponent(ComponentTestCase):

    def test_view_render(self):
        self.form_check_default = Form(self.form_json_check_default, self.builder)
        # EmailComponent
        email = self.form_check_default.components['email']
        self.assertEqual(email.html_component, '<p>yourmail@yourlife.io</p>')