
from radware.sdk.beans_common import *


class EnumSlbBuddyDelete(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewCfgBuddyTable(DeviceBean):
    def __init__(self, **kwargs):
        self.RealSerIndex = kwargs.get('RealSerIndex', None)
        self.Index = kwargs.get('Index', None)
        self.RealIndex = kwargs.get('RealIndex', None)
        self.GroupIndex = kwargs.get('GroupIndex', None)
        self.Service = kwargs.get('Service', None)
        self.Delete = EnumSlbBuddyDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.RealSerIndex, self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'RealSerIndex', 'Index',

