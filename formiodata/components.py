# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

class Component:

    def __init__(self, raw):
        self.raw = raw
        self.submission = {}

    @property
    def key(self):
        return self.raw.get('key')

    @property
    def type(self):
        return self.raw.get('type')

    @property
    def label(self):
        return self.raw.get('label')

    @label.setter
    def label(self, value):
        if self.raw.get('label'):
            self.raw['label'] = value

    @property
    def value(self):
        return self.submission['value']

    @value.setter
    def value(self, value):
        self.submission['value'] = value


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
