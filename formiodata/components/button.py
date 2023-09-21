# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from .component import Component


class buttonComponent(Component):

    @property
    def is_form_component(self):
        return False

    def load_data(self, data):
        # just bypass this
        pass
