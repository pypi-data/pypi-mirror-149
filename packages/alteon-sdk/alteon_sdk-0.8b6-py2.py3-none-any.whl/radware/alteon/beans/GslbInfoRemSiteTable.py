
from radware.sdk.beans_common import *


class EnumGslbInfoRemSiteState(BaseBeanEnum):
    running = 2
    failed = 3
    disabled = 4


class GslbInfoRemSiteTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Idx = kwargs.get('Idx', None)
        self.PrimaryIp = kwargs.get('PrimaryIp', None)
        self.SecondaryIp = kwargs.get('SecondaryIp', None)
        self.Name = kwargs.get('Name', None)
        self.State = EnumGslbInfoRemSiteState.enum(kwargs.get('State', None))

    def get_indexes(self):
        return self.Idx,
    
    @classmethod
    def get_index_names(cls):
        return 'Idx',

