
from radware.sdk.beans_common import *


class EnumMstCistPortLinkType(BaseBeanEnum):
    auto = 1
    p2p = 2
    shared = 3


class EnumMstCistPortEdge(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumMstCistPortStpState(BaseBeanEnum):
    on = 1
    off = 2


class MstCistNewCfgPortTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Priority = kwargs.get('Priority', None)
        self.PathCost = kwargs.get('PathCost', None)
        self.LinkType = EnumMstCistPortLinkType.enum(kwargs.get('LinkType', None))
        self.Edge = EnumMstCistPortEdge.enum(kwargs.get('Edge', None))
        self.StpState = EnumMstCistPortStpState.enum(kwargs.get('StpState', None))
        self.HelloTime = kwargs.get('HelloTime', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

