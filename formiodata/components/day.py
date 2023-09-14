# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

import calendar

from collections import OrderedDict

from .component import Component


class dayComponent(Component):

    @property
    def dayFirst(self):
        return self.raw.get('dayFirst')

    @property
    def value(self):
        return super().value

    @value.setter
    def value(self, value):
        """
        Notes:
        - value format: dd/dd/yyyy
        - Empty value: '00/00/0000'
        """
        val = OrderedDict()
        fields = self.raw['fields']

        # XXX Maybe future formio versions have more formatting possibilites.
        if self.dayFirst:
            if not fields['day'].get('hide'):
                day_val = value[0:2]
                if day_val != '00':
                    val['day'] = int(day_val)
                else:
                    val['day'] = None
            if not fields['month'].get('hide'):
                month_val = value[3:5]
                if month_val != '00':
                    val['month'] = int(month_val)
                else:
                    val['month'] = None
        else:
            if not fields['month'].get('hide'):
                month_val = value[0:2]
                if month_val != '00':
                    val['month'] = int(month_val)
                else:
                    val['month'] = None
            if not fields['day'].get('hide'):
                day_val = value[3:5]
                if day_val != '00':
                    val['day'] = int(day_val)
                else:
                    val['day'] = None

        if not fields['year'].get('hide'):
            if not fields['year'].get('hide'):
                year_val = value[6:10]
                if year_val != '0000':
                    val['year'] = int(year_val)
                else:
                    val['year'] = None

        super(self.__class__, self.__class__).value.fset(self, val)

    @property
    def day(self):
        fields = self.raw['fields']
        if not fields['day'].get('hide'):
            return self.value['day']
        else:
            return None

    @property
    def month(self):
        fields = self.raw['fields']
        if not fields['month'].get('hide'):
            return self.value['month']
        else:
            return None

    @property
    def month_name(self):
        fields = self.raw['fields']
        if self.value['month'] and not fields['month'].get('hide'):
            month_name = calendar.month_name[self.value['month']]
            if self.i18n.get(self.language):
                return self.i18n[self.language].get(month_name, month_name)
            else:
                return month_name
        else:
            return None

    @property
    def year(self):
        fields = self.raw['fields']
        if not fields['year'].get('hide'):
            return self.value['year']
        else:
            return None
