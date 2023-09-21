# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from .component import Component


class addressComponent(Component):

    _none_value = {}

    # XXX other providers not analysed and implemented yet.
    PROVIDER_GOOGLE = 'google'

    def _address_google(self, get_type, notation='long_name'):
        comps = self.value.get('address_components')
        if not comps:
            return None
        else:
            for comp in comps:
                if comp.get('types') and get_type in comp['types']:
                    return comp.get(notation)
            return None

    @property
    def provider(self):
        return self.raw.get('provider')

    @property
    def postal_code(self):
        if self.provider == self.PROVIDER_GOOGLE:
            return self._address_google('postal_code')
        else:
            return None

    @property
    def street_name(self):
        if self.provider == self.PROVIDER_GOOGLE:
            return self._address_google('route')
        else:
            return None

    @property
    def street_number(self):
        if self.provider == self.PROVIDER_GOOGLE:
            return self._address_google('street_number')
        else:
            return None

    @property
    def city(self):
        if self.provider == self.PROVIDER_GOOGLE:
            return self._address_google('locality')
        else:
            return None

    @property
    def country(self):
        if self.provider == self.PROVIDER_GOOGLE:
            return self._address_google('country')
        else:
            return None

    @property
    def country_code(self):
        if self.provider == self.PROVIDER_GOOGLE:
            return self._address_google('country', 'short_name')
        else:
            return None
