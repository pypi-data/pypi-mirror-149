
from radware.sdk.beans_common import *


class EnumBgpPeerState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumBgpPeerDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumBgpPeerDefaultAction(BaseBeanEnum):
    none = 1
    import_ = 2
    originate = 3
    redistribute = 4


class EnumBgpPeerOspfState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumBgpPeerFixedState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumBgpPeerStaticState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumBgpPeerVipState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumBgpPeerRipState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumBgpPeerDenyState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumBgpPeerBfdState(BaseBeanEnum):
    on = 1
    off = 2

class EnumbgpNewCfgPeerIpVer(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2

class EnumBgpPeerGracefulState(BaseBeanEnum):
    enabled = 1
    disabled = 2

class EnumBgpPeerCommAdv(BaseBeanEnum):
    enabled = 1
    disabled = 2

class EnumBgpPeerPasswordStatus(BaseBeanEnum):
    enabled = 1
    disabled = 2

class BgpNewCfgPeerTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.RemoteAddr = kwargs.get('RemoteAddr', None)
        self.RemoteAs = kwargs.get('RemoteAs', None)
        self.Ttl = kwargs.get('Ttl', None)
        self.State = EnumBgpPeerState.enum(kwargs.get('State', None))
        self.Delete = EnumBgpPeerDelete.enum(kwargs.get('Delete', None))
        self.Metric = kwargs.get('Metric', None)
        self.DefaultAction = EnumBgpPeerDefaultAction.enum(kwargs.get('DefaultAction', None))
        self.OspfState = EnumBgpPeerOspfState.enum(kwargs.get('OspfState', None))
        self.FixedState = EnumBgpPeerFixedState.enum(kwargs.get('FixedState', None))
        self.StaticState = EnumBgpPeerStaticState.enum(kwargs.get('StaticState', None))
        self.VipState = EnumBgpPeerVipState.enum(kwargs.get('VipState', None))
        self.InRmapList = kwargs.get('InRmapList', None)
        self.OutRmapList = kwargs.get('OutRmapList', None)
        self.AddInRmap = kwargs.get('AddInRmap', None)
        self.AddOutRmap = kwargs.get('AddOutRmap', None)
        self.RemoveInRmap = kwargs.get('RemoveInRmap', None)
        self.RemoveOutRmap = kwargs.get('RemoveOutRmap', None)
        self.HoldTime = kwargs.get('HoldTime', None)
        self.KeepAlive = kwargs.get('KeepAlive', None)
        self.MinTime = kwargs.get('MinTime', None)
        self.ConRetry = kwargs.get('ConRetry', None)
        self.MinAS = kwargs.get('MinAS', None)
        self.RipState = EnumBgpPeerRipState.enum(kwargs.get('RipState', None))
        self.DenyState = EnumBgpPeerDenyState.enum(kwargs.get('DenyState', None))
        self.NextHop = kwargs.get('NextHop', None)
        self.BfdState = EnumBgpPeerBfdState.enum(kwargs.get('BfdState', None))
        self.IpVer = EnumbgpNewCfgPeerIpVer.enum(kwargs.get('IpVer', None))
        self.RemoteAddr6 = kwargs.get('RemoteAddr6', None)
        self.GracefulState = EnumBgpPeerGracefulState.enum(kwargs.get('GracefulState', None))
        self.StdCommAdv = EnumBgpPeerCommAdv.enum(kwargs.get('StdCommAdv', None))
        self.LarCommAdv = EnumBgpPeerCommAdv.enum(kwargs.get('LarCommAdv', None))
        self.ExtCommAdv = EnumBgpPeerCommAdv.enum(kwargs.get('ExtCommAdv', None))
        self.SecureHops = kwargs.get('SecureHops', None)
        self.Password = kwargs.get('Password', None)
        self.PasswordStatus = EnumBgpPeerPasswordStatus.enum(kwargs.get('PasswordStatus', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

