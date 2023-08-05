
from radware.sdk.beans_common import *


class EnumStgState(BaseBeanEnum):
    on = 1
    off = 2


class EnumStgDefaultCfg(BaseBeanEnum):
    default_config = 1


class EnumStgUntagPvst(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumStgVlanListType(BaseBeanEnum):
    default = 1
    listall = 2


class StgNewCfgTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.State = EnumStgState.enum(kwargs.get('State', None))
        self.DefaultCfg = EnumStgDefaultCfg.enum(kwargs.get('DefaultCfg', None))
        self.AddVlan = kwargs.get('AddVlan', None)
        self.RemoveVlan = kwargs.get('RemoveVlan', None)
        self.Priority = kwargs.get('Priority', None)
        self.BrgHelloTime = kwargs.get('BrgHelloTime', None)
        self.BrgForwardDelay = kwargs.get('BrgForwardDelay', None)
        self.BrgMaxAge = kwargs.get('BrgMaxAge', None)
        self.AgingTime = kwargs.get('AgingTime', None)
        self.VlanBmap = kwargs.get('VlanBmap', None)
        self.UntagPvst = EnumStgUntagPvst.enum(kwargs.get('UntagPvst', None))
        self.VlanListType = EnumStgVlanListType.enum(kwargs.get('VlanListType', None))
        self.VlanBmap3 = kwargs.get('VlanBmap3', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

