
from radware.sdk.beans_common import *


class EnumStgPortState(BaseBeanEnum):
    on = 1
    off = 2


class EnumStgPortLink(BaseBeanEnum):
    auto = 1
    p2p = 2
    shared = 3


class EnumStgPortEdge(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumStgBlockBPDU(BaseBeanEnum):
    enabled = 1
    disabled = 2


class StgNewCfgPortTable(DeviceBean):
    def __init__(self, **kwargs):
        self.StgIndex = kwargs.get('StgIndex', None)
        self.Index = kwargs.get('Index', None)
        self.State = EnumStgPortState.enum(kwargs.get('State', None))
        self.Priority = kwargs.get('Priority', None)
        self.PathCost = kwargs.get('PathCost', None)
        self.Link = EnumStgPortLink.enum(kwargs.get('Link', None))
        self.Edge = EnumStgPortEdge.enum(kwargs.get('Edge', None))
        self.BlockBPDU = EnumStgBlockBPDU.enum(kwargs.get('BlockBPDU', None))

    def get_indexes(self):
        return self.StgIndex, self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'StgIndex', 'Index',

