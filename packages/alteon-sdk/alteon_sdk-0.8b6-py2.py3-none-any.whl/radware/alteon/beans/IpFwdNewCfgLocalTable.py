
from radware.sdk.beans_common import *


class EnumIpFwdLocalDelete(BaseBeanEnum):
    other = 1
    delete = 2


class IpFwdNewCfgLocalTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Subnet = kwargs.get('Subnet', None)
        self.Mask = kwargs.get('Mask', None)
        self.Delete = EnumIpFwdLocalDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

