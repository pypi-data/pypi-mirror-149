
from radware.sdk.beans_common import *


class IpRepNewCountriesTable(DeviceBean):
    def __init__(self, **kwargs):
        self.CfgCountriesIndex = kwargs.get('CfgCountriesIndex', None)
        self.CfgCountriesCountry = kwargs.get('CfgCountriesCountry', None)

    def get_indexes(self):
        return self.CfgCountriesIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'CfgCountriesIndex',

