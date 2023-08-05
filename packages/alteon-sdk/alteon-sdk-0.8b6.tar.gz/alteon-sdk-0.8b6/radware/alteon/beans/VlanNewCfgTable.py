
from radware.sdk.beans_common import *


class EnumVlanState(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVlanDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumVlanJumbo(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVlanLearn(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVlanShared(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVlanIpv6LlaGen(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVlanRouterAdv(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVlanMFlag(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVlanOFlag(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVlanOpInfo(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVlanApInfo(BaseBeanEnum):
    enabled = 2
    disabled = 3


class VlanNewCfgTable(DeviceBean):
    def __init__(self, **kwargs):
        self.VlanId = kwargs.get('VlanId', None)
        self.VlanName = kwargs.get('VlanName', None)
        self.Ports = kwargs.get('Ports', None)
        self.State = EnumVlanState.enum(kwargs.get('State', None))
        self.AddPort = kwargs.get('AddPort', None)
        self.RemovePort = kwargs.get('RemovePort', None)
        self.Delete = EnumVlanDelete.enum(kwargs.get('Delete', None))
        self.BwmContract = kwargs.get('BwmContract', None)
        self.Stg = kwargs.get('Stg', None)
        self.Jumbo = EnumVlanJumbo.enum(kwargs.get('Jumbo', None))
        self.Learn = EnumVlanLearn.enum(kwargs.get('Learn', None))
        self.Shared = EnumVlanShared.enum(kwargs.get('Shared', None))
        self.Ipv6LlaGen = EnumVlanIpv6LlaGen.enum(kwargs.get('Ipv6LlaGen', None))
        self.RouterAdv = EnumVlanRouterAdv.enum(kwargs.get('RouterAdv', None))
        self.ReTransInt = kwargs.get('ReTransInt', None)
        self.MinIntBwAdv = kwargs.get('MinIntBwAdv', None)
        self.MaxIntBwAdv = kwargs.get('MaxIntBwAdv', None)
        self.Mtu = kwargs.get('Mtu', None)
        self.CurHopLimit = kwargs.get('CurHopLimit', None)
        self.MFlag = EnumVlanMFlag.enum(kwargs.get('MFlag', None))
        self.OFlag = EnumVlanOFlag.enum(kwargs.get('OFlag', None))
        self.RTime = kwargs.get('RTime', None)
        self.RlTime = kwargs.get('RlTime', None)
        self.PlTime = kwargs.get('PlTime', None)
        self.VlTime = kwargs.get('VlTime', None)
        self.OpInfo = EnumVlanOpInfo.enum(kwargs.get('OpInfo', None))
        self.ApInfo = EnumVlanApInfo.enum(kwargs.get('ApInfo', None))
        self.Ipv6Lla = kwargs.get('Ipv6Lla', None)

    def get_indexes(self):
        return self.VlanId,
    
    @classmethod
    def get_index_names(cls):
        return 'VlanId',

