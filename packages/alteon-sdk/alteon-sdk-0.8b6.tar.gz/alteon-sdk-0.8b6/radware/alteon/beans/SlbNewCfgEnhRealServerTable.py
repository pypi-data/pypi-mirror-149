
from radware.sdk.beans_common import *


class EnumSlbRealServerState(BaseBeanEnum):
    enabled = 2
    disabled = 3
    disabled_with_fastage = 4
    shutdown_connection = 5
    shutdown_persistent_sessions = 6


class EnumSlbRealServerDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumSlbRealServerType(BaseBeanEnum):
    local_server = 1
    remote_server = 2


class EnumSlbRealServerCookie(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbRealServerExcludeStr(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbRealServerSubmac(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbRealServerIpVer(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2


class EnumSlbRealServerLLBType(BaseBeanEnum):
    local = 0
    remote = 1
    wanlink = 2


class EnumSlbRealServerSecType(BaseBeanEnum):
    none = 1
    virtual = 2
    layer = 3
    passive = 4
    l3sw = 5


class EnumSlbRealServerSecDeviceFlag(BaseBeanEnum):
    none = 1
    security = 2


class SlbNewCfgEnhRealServerTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.IpAddr = kwargs.get('IpAddr', None)
        self.Weight = kwargs.get('Weight', None)
        self.MaxConns = kwargs.get('MaxConns', None)
        self.TimeOut = kwargs.get('TimeOut', None)
        self.PingInterval = kwargs.get('PingInterval', None)
        self.FailRetry = kwargs.get('FailRetry', None)
        self.SuccRetry = kwargs.get('SuccRetry', None)
        self.State = EnumSlbRealServerState.enum(kwargs.get('State', None))
        self.Delete = EnumSlbRealServerDelete.enum(kwargs.get('Delete', None))
        self.Type = EnumSlbRealServerType.enum(kwargs.get('Type', None))
        self.Name = kwargs.get('Name', None)
        self.AddUrl = kwargs.get('AddUrl', None)
        self.RemUrl = kwargs.get('RemUrl', None)
        self.Cookie = EnumSlbRealServerCookie.enum(kwargs.get('Cookie', None))
        self.ExcludeStr = EnumSlbRealServerExcludeStr.enum(kwargs.get('ExcludeStr', None))
        self.Submac = EnumSlbRealServerSubmac.enum(kwargs.get('Submac', None))
        self.Idsport = kwargs.get('Idsport', None)
        self.IpVer = EnumSlbRealServerIpVer.enum(kwargs.get('IpVer', None))
        self.Ipv6Addr = kwargs.get('Ipv6Addr', None)
        self.NxtRportIdx = kwargs.get('NxtRportIdx', None)
        self.NxtBuddyIdx = kwargs.get('NxtBuddyIdx', None)
        self.LLBType = EnumSlbRealServerLLBType.enum(kwargs.get('LLBType', None))
        self.Copy = kwargs.get('Copy', None)
        self.PortsIngress = kwargs.get('PortsIngress', None)
        self.PortsEgress = kwargs.get('PortsEgress', None)
        self.AddPortsIngress = kwargs.get('AddPortsIngress', None)
        self.RemPortsIngress = kwargs.get('RemPortsIngress', None)
        self.AddPortsEgress = kwargs.get('AddPortsEgress', None)
        self.RemPortsEgress = kwargs.get('RemPortsEgress', None)
        self.VlanIngress = kwargs.get('VlanIngress', None)
        self.VlanEgress = kwargs.get('VlanEgress', None)
        self.EgressIf = kwargs.get('EgressIf', None)
        self.SecType = EnumSlbRealServerSecType.enum(kwargs.get('SecType', None))
        self.IngressIf = kwargs.get('IngressIf', None)
        self.SecDeviceFlag = EnumSlbRealServerSecDeviceFlag.enum(kwargs.get('SecDeviceFlag', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

