# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

class Component:

    def __init__(self, raw):
        self.raw = raw


class textfieldComponent(Component):
    pass


class emailComponent(Component):
    pass


class phoneNumberComponent(Component):
    pass


class surveyComponent(Component):
    pass


class signatureComponent(Component):
    pass


class buttonComponent(Component):
    pass
