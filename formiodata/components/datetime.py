# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from copy import copy
from datetime import datetime

from .component import Component


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
        # Backport of Python 3.7 datetime.fromisoformat
        if hasattr(datetime, 'fromisoformat'):
            # Python >= 3.7
            return datetime.fromisoformat(value)
        else:
            # Python < 3.7
            # replaces the fromisoformat, not available in Python < 3.7
            #
            # XXX following:
            # - Raises: '2021-02-25T00:00:00+01:00' does not match format '%Y-%m-%dT%H:%M%z'
            # - Due to %z not obtaing the colon in '+1:00' (tz offset)
            # - More info: https://stackoverflow.com/questions/54268458/datetime-strptime-issue-with-a-timezone-offset-with-colons
            # fmt_str =  r"%Y-%m-%dT%H:%M:%S%z"
            # return datetime.strptime(value, fmt_str)
            #
            # REQUIREMENT (TODO document, setup dependency or try/except raise exception)
            # - pip install dateutil
            # - https://dateutil.readthedocs.io/
            from dateutil.parser import parse
            return parse(value)

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
