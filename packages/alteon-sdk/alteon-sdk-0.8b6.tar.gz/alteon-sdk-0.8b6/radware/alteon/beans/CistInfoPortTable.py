
from radware.sdk.beans_common import *


class EnumCistInfoPortState(BaseBeanEnum):
    disabled = 1
    discarding = 2
    learning = 4
    forwarding = 5


class EnumCistInfoPortRole(BaseBeanEnum):
    disabled = 1
    alternate = 2
    backup = 3
    root = 4
    designated = 5
    master = 6
    unknown = 7


class EnumCistInfoPortLinkType(BaseBeanEnum):
    p2p = 1
    shared = 2
    unknown = 3


class CistInfoPortTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Priority = kwargs.get('Priority', None)
        self.PathCost = kwargs.get('PathCost', None)
        self.State = EnumCistInfoPortState.enum(kwargs.get('State', None))
        self.Role = EnumCistInfoPortRole.enum(kwargs.get('Role', None))
        self.DesignatedBridge = kwargs.get('DesignatedBridge', None)
        self.DesignatedPort = kwargs.get('DesignatedPort', None)
        self.LinkType = EnumCistInfoPortLinkType.enum(kwargs.get('LinkType', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

