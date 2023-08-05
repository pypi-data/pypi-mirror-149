
from radware.sdk.beans_common import *


class EnumIpRepWhiteListAction(BaseBeanEnum):
    other = 1
    delete = 2


class IpRepNewWhiteListTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.IP = kwargs.get('IP', None)
        self.Mask = kwargs.get('Mask', None)
        self.Action = EnumIpRepWhiteListAction.enum(kwargs.get('Action', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

