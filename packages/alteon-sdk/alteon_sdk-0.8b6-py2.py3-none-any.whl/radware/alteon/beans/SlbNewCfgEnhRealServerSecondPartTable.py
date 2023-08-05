
from radware.sdk.beans_common import *


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


class SlbNewCfgEnhRealServerSecondPartTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.UrlBmap = kwargs.get('UrlBmap', None)
        self.Proxy = EnumSlbRealServerProxy.enum(kwargs.get('Proxy', None))
        self.Ldapwr = EnumSlbRealServerLdapwr.enum(kwargs.get('Ldapwr', None))
        self.Idsvlan = kwargs.get('Idsvlan', None)
        self.Avail = kwargs.get('Avail', None)
        self.FastHealthCheck = EnumSlbRealServerFastHealthCheck.enum(kwargs.get('FastHealthCheck', None))
        self.Subdmac = EnumSlbRealServerSubdmac.enum(kwargs.get('Subdmac', None))
        self.Overflow = EnumSlbRealServerOverflow.enum(kwargs.get('Overflow', None))
        self.BkpPreempt = EnumSlbRealServerBkpPreempt.enum(kwargs.get('BkpPreempt', None))
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

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

