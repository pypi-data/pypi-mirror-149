
from radware.sdk.beans_common import *


class EnumSlbRealServerState(BaseBeanEnum):
    enabled = 2
    disabled = 3
    disabled_with_fastage = 4


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


class EnumSlbRealServerProxy(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbRealServerLdapwr(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbRealServerFastHealthCheck(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbRealServerSubdmac(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbRealServerOverflow(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbRealServerBkpPreempt(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbRealServerIpVer(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2


class EnumSlbRealServerMode(BaseBeanEnum):
    physical = 1
    logical = 2


class EnumSlbUpdateAllRealServers(BaseBeanEnum):
    none = 0
    mode = 1
    maxcon = 2
    weight = 3
    all = 4


class EnumSlbRealServerProxyIpMode(BaseBeanEnum):
    enable = 0
    address = 2
    nwclss = 3
    disable = 4


class EnumSlbRealServerProxyIpPersistency(BaseBeanEnum):
    disable = 0
    client = 1
    host = 2


class EnumSlbRealServerProxyIpNWclassPersistency(BaseBeanEnum):
    disable = 0
    client = 1


class SlbNewCfgRealServerTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.IpAddr = kwargs.get('IpAddr', None)
        self.Weight = kwargs.get('Weight', None)
        self.MaxConns = kwargs.get('MaxConns', None)
        self.TimeOut = kwargs.get('TimeOut', None)
        self.BackUp = kwargs.get('BackUp', None)
        self.PingInterval = kwargs.get('PingInterval', None)
        self.FailRetry = kwargs.get('FailRetry', None)
        self.SuccRetry = kwargs.get('SuccRetry', None)
        self.State = EnumSlbRealServerState.enum(kwargs.get('State', None))
        self.Delete = EnumSlbRealServerDelete.enum(kwargs.get('Delete', None))
        self.Type = EnumSlbRealServerType.enum(kwargs.get('Type', None))
        self.Name = kwargs.get('Name', None)
        self.UrlBmap = kwargs.get('UrlBmap', None)
        self.AddUrl = kwargs.get('AddUrl', None)
        self.RemUrl = kwargs.get('RemUrl', None)
        self.Cookie = EnumSlbRealServerCookie.enum(kwargs.get('Cookie', None))
        self.ExcludeStr = EnumSlbRealServerExcludeStr.enum(kwargs.get('ExcludeStr', None))
        self.Submac = EnumSlbRealServerSubmac.enum(kwargs.get('Submac', None))
        self.Proxy = EnumSlbRealServerProxy.enum(kwargs.get('Proxy', None))
        self.Ldapwr = EnumSlbRealServerLdapwr.enum(kwargs.get('Ldapwr', None))
        self.Oid = kwargs.get('Oid', None)
        self.CommString = kwargs.get('CommString', None)
        self.Idsvlan = kwargs.get('Idsvlan', None)
        self.Idsport = kwargs.get('Idsport', None)
        self.Avail = kwargs.get('Avail', None)
        self.FastHealthCheck = EnumSlbRealServerFastHealthCheck.enum(kwargs.get('FastHealthCheck', None))
        self.Subdmac = EnumSlbRealServerSubdmac.enum(kwargs.get('Subdmac', None))
        self.Overflow = EnumSlbRealServerOverflow.enum(kwargs.get('Overflow', None))
        self.BkpPreempt = EnumSlbRealServerBkpPreempt.enum(kwargs.get('BkpPreempt', None))
        self.IpVer = EnumSlbRealServerIpVer.enum(kwargs.get('IpVer', None))
        self.Ipv6Addr = kwargs.get('Ipv6Addr', None)
        self.NxtRportIdx = kwargs.get('NxtRportIdx', None)
        self.NxtBuddyIdx = kwargs.get('NxtBuddyIdx', None)
        self.Mode = EnumSlbRealServerMode.enum(kwargs.get('Mode', None))
        self.UpdateAllRealServers = EnumSlbUpdateAllRealServers.enum(kwargs.get('UpdateAllRealServers', None))
        self.ProxyIpMode = EnumSlbRealServerProxyIpMode.enum(kwargs.get('ProxyIpMode', None))
        self.ProxyIpAddr = kwargs.get('ProxyIpAddr', None)
        self.ProxyIpMask = kwargs.get('ProxyIpMask', None)
        self.ProxyIpv6Addr = kwargs.get('ProxyIpv6Addr', None)
        self.ProxyIpv6Prefix = kwargs.get('ProxyIpv6Prefix', None)
        self.ProxyIpPersistency = EnumSlbRealServerProxyIpPersistency.enum(kwargs.get('ProxyIpPersistency', None))
        self.ProxyIpNWclass = kwargs.get('ProxyIpNWclass', None)
        self.ProxyIpNWclassPersistency = EnumSlbRealServerProxyIpNWclassPersistency.enum(kwargs.get('ProxyIpNWclassPersistency', None))
        self.HealthID = kwargs.get('HealthID', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

