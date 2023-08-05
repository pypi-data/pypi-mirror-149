
from radware.sdk.beans_common import *


class EnumSlbRealServPortDelete(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewCfgRealServPortTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.PortIndex = kwargs.get('PortIndex', None)
        self.RealPort = kwargs.get('RealPort', None)
        self.Delete = EnumSlbRealServPortDelete.enum(kwargs.get('Delete', None))
        self.RealPortFreeIdx = kwargs.get('RealPortFreeIdx', None)

    def get_indexes(self):
        return self.Index, self.PortIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'Index', 'PortIndex',

