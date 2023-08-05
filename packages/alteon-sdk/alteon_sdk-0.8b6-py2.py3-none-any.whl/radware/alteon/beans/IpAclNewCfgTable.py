
from radware.sdk.beans_common import *


class EnumIpAclAction(BaseBeanEnum):
    other = 1
    delete = 2


class IpAclNewCfgTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.Ip = kwargs.get('Ip', None)
        self.Action = EnumIpAclAction.enum(kwargs.get('Action', None))
        self.Mask = kwargs.get('Mask', None)

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

