
from radware.sdk.beans_common import *


class EnumVadcVlanIpv6LlaGen(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVadcVlanRouterAdv(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVadcVlanMFlag(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVadcVlanOFlag(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVadcVlanOpInfo(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVadcVlanApInfo(BaseBeanEnum):
    enabled = 2
    disabled = 3


class VadcVlanNewCfgTable(DeviceBean):
    def __init__(self, **kwargs):
        self.VlanId = kwargs.get('VlanId', None)
        self.BwmCont = kwargs.get('BwmCont', None)
        self.NonIp = kwargs.get('NonIp', None)
        self.Ipv6LlaGen = EnumVadcVlanIpv6LlaGen.enum(kwargs.get('Ipv6LlaGen', None))
        self.RouterAdv = EnumVadcVlanRouterAdv.enum(kwargs.get('RouterAdv', None))
        self.ReTransInt = kwargs.get('ReTransInt', None)
        self.MinIntBwAdv = kwargs.get('MinIntBwAdv', None)
        self.MaxIntBwAdv = kwargs.get('MaxIntBwAdv', None)
        self.Mtu = kwargs.get('Mtu', None)
        self.CurHopLimit = kwargs.get('CurHopLimit', None)
        self.MFlag = EnumVadcVlanMFlag.enum(kwargs.get('MFlag', None))
        self.OFlag = EnumVadcVlanOFlag.enum(kwargs.get('OFlag', None))
        self.RTime = kwargs.get('RTime', None)
        self.RlTime = kwargs.get('RlTime', None)
        self.PlTime = kwargs.get('PlTime', None)
        self.VlTime = kwargs.get('VlTime', None)
        self.OpInfo = EnumVadcVlanOpInfo.enum(kwargs.get('OpInfo', None))
        self.ApInfo = EnumVadcVlanApInfo.enum(kwargs.get('ApInfo', None))
        self.Ipv6Lla = kwargs.get('Ipv6Lla', None)

    def get_indexes(self):
        return self.VlanId,
    
    @classmethod
    def get_index_names(cls):
        return 'VlanId',

