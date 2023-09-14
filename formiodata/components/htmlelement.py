# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from .component import Component


class htmlelementComponent(Component):

    @property
    def html(self):
        html = '<%s>%s</%s>' % (self.raw['tag'], self.raw['content'], self.raw['tag'])
        return html
