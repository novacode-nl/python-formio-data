# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from .grid_base import baseGridComponent


class editgridComponent(baseGridComponent):

    @property
    def initEmpty(self):
        return not self.raw.get('openWhenEmpty')
