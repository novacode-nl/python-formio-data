from formiodata.form import Form
from test_component import ComponentTestCase


class viewRenderEmailComponent(ComponentTestCase):

    def test_view_render(self):
        self.form_check_default = Form(self.form_json_check_default, self.builder)
        self.form_check_default.render_components()
        # EmailComponent
        email = self.form_check_default.input_components['email']
        self.assertEqual(email.html_component, '<p>yourmail@yourlife.io</p>')
