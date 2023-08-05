
from radware.sdk.beans_common import *


class EnumDot1dStpPortState(BaseBeanEnum):
    disabled = 1
    blocking = 2
    listening = 3
    learning = 4
    forwarding = 5
    broken = 6


class EnumDot1dStpPortEnable(BaseBeanEnum):
    enabled = 1
    disabled = 2


class Dot1dStpPortTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Port = kwargs.get('Port', None)
        self.Priority = kwargs.get('Priority', None)
        self.State = EnumDot1dStpPortState.enum(kwargs.get('State', None))
        self.Enable = EnumDot1dStpPortEnable.enum(kwargs.get('Enable', None))
        self.PathCost = kwargs.get('PathCost', None)
        self.DesignatedRoot = kwargs.get('DesignatedRoot', None)
        self.DesignatedCost = kwargs.get('DesignatedCost', None)
        self.DesignatedBridge = kwargs.get('DesignatedBridge', None)
        self.DesignatedPort = kwargs.get('DesignatedPort', None)
        self.ForwardTransitions = kwargs.get('ForwardTransitions', None)

    def get_indexes(self):
        return self.Port,
    
    @classmethod
    def get_index_names(cls):
        return 'Port',

