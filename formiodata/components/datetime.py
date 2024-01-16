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
        # TODO: to improve these transformations (mappings and loops)

        if not value:
            return value

        component = self.component_owner.input_components.get(self.key)

        # if not component.raw.get('enableTime'):
        if not self.enableTime:
            # OMG some parsing to deal with the ISO format (storage).
            try:
                dt = datetime.fromisoformat(value)
                dt_format = self.raw.get('format')
                py_format = copy(dt_format)
                for date_part, mapping in self._format_mappings().items():
                    done_date_part = False
                    for fm_formio, fm_py in mapping.items():
                        # fm_formio are (JS) uibDateParser codes, see comment
                        # in _format_mappings
                        if not done_date_part and fm_formio in dt_format:
                            py_format = py_format.replace(fm_formio, fm_py)
                            done_date_part = True
                super(self.__class__, self.__class__).value.fset(
                    self,
                    dt.strftime(py_format)
                )
            except ValueError:
                dt_format = self.raw.get('format')
                py_format = copy(dt_format)
                for date_part, mapping in self._format_mappings().items():
                    done_date_part = False
                    for fm_formio, fm_py in mapping.items():
                        # fm_formio are (JS) uibDateParser codes, see comment
                        # in _format_mappings
                        if not done_date_part and fm_formio in dt_format:
                            py_format = py_format.replace(fm_formio, fm_py)
                            done_date_part = True
                py_dt = datetime.strptime(value, py_format)
                val = datetime.fromisoformat(py_dt)
                super(self.__class__, self.__class__).value.fset(self, val)
            return
        else:
            dt = self._fromisoformat(value)
            py_dt_format = formio_dt_format = component.raw.get('format')
            mapping = self._format_mappings()

            # year
            done = False
            for formio, py in mapping['year'].items():
                if not done and formio in formio_dt_format:
                    py_dt_format = py_dt_format.replace(formio, py)
                    done = True

            # month
            done = False
            for formio, py in mapping['month'].items():
                if not done and formio in formio_dt_format:
                    py_dt_format = py_dt_format.replace(formio, py)
                    done = True

            # day
            done = False
            for formio, py in mapping['day'].items():
                if not done and formio in formio_dt_format:
                    py_dt_format = py_dt_format.replace(formio, py)
                    done = True

            # hour
            done = False
            for formio, py in mapping['hour'].items():
                if not done and formio in formio_dt_format:
                    py_dt_format = py_dt_format.replace(formio, py)
                    done = True

            # minute
            done = False
            for formio, py in mapping['minute'].items():
                if not done and formio in formio_dt_format:
                    py_dt_format = py_dt_format.replace(formio, py)
                    done = True

            # second
            done = False
            for formio, py in mapping['second'].items():
                if not done and formio in formio_dt_format:
                    py_dt_format = py_dt_format.replace(formio, py)
                    done = True

            # 12 hours AM/PM
            done = False
            for formio, py in mapping['am_pm'].items():
                if not done and formio in formio_dt_format:
                    py_dt_format = py_dt_format.replace(formio, py)
                    done = True

            val = dt.strftime(py_dt_format)
            super(self.__class__, self.__class__).value.fset(self, val)

    def to_datetime(self):
        if not self.raw_value:
            return None
        dt = self._fromisoformat(self.raw_value)
        return dt

    def to_date(self):
        if not self.raw_value:
            return None
        return self.to_datetime().date()
