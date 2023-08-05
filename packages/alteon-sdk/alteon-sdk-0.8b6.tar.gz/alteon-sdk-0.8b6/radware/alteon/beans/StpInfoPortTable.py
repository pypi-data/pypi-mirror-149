
from radware.sdk.beans_common import *


class EnumStpInfoPortState(BaseBeanEnum):
    disabled = 1
    blocking = 2
    listening = 3
    learning = 4
    forwarding = 5
    broken = 6
    discarding = 7


class EnumStpInfoPortRole(BaseBeanEnum):
    disabled = 1
    alternate = 2
    backup = 3
    root = 4
    designated = 5
    master = 6
    unknown = 7


class EnumStpInfoPortLinkType(BaseBeanEnum):
    p2p = 1
    shared = 2
    unknown = 3


class EnumStpInfoPortEdge(BaseBeanEnum):
    enabled = 1
    disabled = 2


class StpInfoPortTable(DeviceBean):
    def __init__(self, **kwargs):
        self.StpIndex = kwargs.get('StpIndex', None)
        self.Index = kwargs.get('Index', None)
        self.State = EnumStpInfoPortState.enum(kwargs.get('State', None))
        self.DesignatedRoot = kwargs.get('DesignatedRoot', None)
        self.DesignatedCost = kwargs.get('DesignatedCost', None)
        self.DesignatedBridge = kwargs.get('DesignatedBridge', None)
        self.DesignatedPort = kwargs.get('DesignatedPort', None)
        self.ForwardTransitions = kwargs.get('ForwardTransitions', None)
        self.PathCost = kwargs.get('PathCost', None)
        self.Role = EnumStpInfoPortRole.enum(kwargs.get('Role', None))
        self.LinkType = EnumStpInfoPortLinkType.enum(kwargs.get('LinkType', None))
        self.Edge = EnumStpInfoPortEdge.enum(kwargs.get('Edge', None))

    def get_indexes(self):
        return self.StpIndex, self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'StpIndex', 'Index',

