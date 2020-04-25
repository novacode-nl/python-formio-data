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


# Basic

class textfieldComponent(Component):
    pass


class textareaComponent(Component):
    pass


class numberComponent(Component):
    pass


class passwordComponent(Component):
    pass


class checkboxComponent(Component):
    pass


class selectboxesComponent(Component):
    pass


class selectComponent(Component):
    pass


class radioComponent(Component):
    pass


class buttonComponent(Component):
    pass


# Advanced

class emailComponent(Component):
    pass


class urlComponent(Component):
    pass


class phoneNumberComponent(Component):
    pass


# TODO: tags, address


class datetimeComponent(Component):
    pass


class dateComponent(Component):
    pass


class timeComponent(Component):
    pass


class currencyComponent(Component):
    pass


class surveyComponent(Component):
    pass


class signatureComponent(Component):
    pass


# Layout components

class htmlelementComponent(Component):
    pass


class contentComponent(Component):
    pass


class columnsComponent(Component):
    pass


class fieldsetComponent(Component):
    pass


class panelComponent(Component):
    pass


class tableComponent(Component):
    pass
