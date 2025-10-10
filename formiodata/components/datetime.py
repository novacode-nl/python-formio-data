# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import logging

from copy import copy
from datetime import datetime

from .component import Component
from ..utils import datetime_fromisoformat

logger = logging.getLogger(__name__)


class datetimeComponent(Component):

    @property
    def enableTime(self):
        return self.raw.get('enableTime')

    def _format_mappings(self):
        """
        Dictionary of mappings between Formio Datetime component
        (key) to Python format (value).

        Formio uses the (JS uibDateParser) format codes referenced in:
        https://github.com/angular-ui/bootstrap/tree/master/src/dateparser/docs#uibdateparsers-format-codes
        """
        return {
            'year': {'yyyy': '%Y', 'yy': '%y', 'y': '%y'},
            'month': {'MMMM': '%B', 'MMM': '%b', 'MM': '%m', 'M': '%-m'},
            'day': {'dd': '%d', 'd': '%-d'},
            'hour': {'HH': '%H', 'H': '%-H', 'hh': '%I', 'h': '%-I'},
            'minute': {'mm': '%M', 'm': '%-M'},
            'second': {'ss': '%S', 's': '%-S'},
            'am_pm': {'a': '%p'}
        }

    def _fromisoformat(self, value):
        return datetime_fromisoformat(value)

    @property
    def value(self):
        return super().value

    @value.setter
    def value(self, value):
        """ Inherit property setter the right way, URLs:
        - https://gist.github.com/Susensio/979259559e2bebcd0273f1a95d7c1e79
        - https://stackoverflow.com/questions/35290540/understanding-property-decorator-and-inheritance
        """
        if not value:
            return value
        else:
            return super(self.__class__, self.__class__).value.fset(self, value)

    def to_datetime(self):
        if not self.raw_value:
            return None
        dt = self._fromisoformat(self.raw_value)
        return dt

    def to_date(self):
        if not self.raw_value:
            return None
        return self.to_datetime().date()
