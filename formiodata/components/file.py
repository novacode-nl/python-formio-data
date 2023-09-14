# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from .component import Component

from formiodata.utils import base64_encode_url


class fileComponent(Component):

    def __init__(self, raw, builder, **kwargs):
        super().__init__(raw, builder, **kwargs)

    @property
    def storage(self):
        return self.raw.get('storage')

    @property
    def url(self):
        return self.raw.get('url')

    @property
    def base64(self):
        if self.storage == 'url':
            res = ''
            for val in self.form.get('value'):
                url = val.get('url')
                res += base64_encode_url(url)
            return res
        elif self.storage == 'base64':
            return super().value

    # @value.setter
    # def value(self, value):
    #     """ Inherit property setter the right way, URLs:
    #     - https://gist.github.com/Susensio/979259559e2bebcd0273f1a95d7c1e79
    #     - https://stackoverflow.com/questions/35290540/understanding-property-decorator-and-inheritance
    #     """
    #     super(self.__class__, self.__class__).value.fset(self, value)
