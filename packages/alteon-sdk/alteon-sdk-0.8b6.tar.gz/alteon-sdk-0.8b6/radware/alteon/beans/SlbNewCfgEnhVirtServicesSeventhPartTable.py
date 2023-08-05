
from radware.sdk.beans_common import *


class EnumSlbVirtServiceSessionMirror(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceSoftGrid(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceConnPooling(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceProxyIpMode(BaseBeanEnum):
    ingress = 0
    egress = 1
    address = 2
    nwclss = 3
    disable = 4


class EnumSlbVirtServiceProxyIpPersistency(BaseBeanEnum):
    disable = 0
    client = 1
    host = 2


class EnumSlbVirtServiceProxyIpNWclassPersistency(BaseBeanEnum):
    disable = 0
    client = 1


class EnumSlbVirtServiceClsRST(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceCluster(BaseBeanEnum):
    enabled = 1
    disabled = 2


class SlbNewCfgEnhVirtServicesSeventhPartTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ServSeventhPartIndex = kwargs.get('ServSeventhPartIndex', None)
        self.SeventhPartIndex = kwargs.get('SeventhPartIndex', None)
        self.RealGroup = kwargs.get('RealGroup', None)
        self.SessionMirror = EnumSlbVirtServiceSessionMirror.enum(kwargs.get('SessionMirror', None))
        self.SoftGrid = EnumSlbVirtServiceSoftGrid.enum(kwargs.get('SoftGrid', None))
        self.ConnPooling = EnumSlbVirtServiceConnPooling.enum(kwargs.get('ConnPooling', None))
        self.PersistentTimeOut = kwargs.get('PersistentTimeOut', None)
        self.ProxyIpMode = EnumSlbVirtServiceProxyIpMode.enum(kwargs.get('ProxyIpMode', None))
        self.ProxyIpAddr = kwargs.get('ProxyIpAddr', None)
        self.ProxyIpMask = kwargs.get('ProxyIpMask', None)
        self.ProxyIpv6Addr = kwargs.get('ProxyIpv6Addr', None)
        self.ProxyIpv6Prefix = kwargs.get('ProxyIpv6Prefix', None)
        self.ProxyIpPersistency = EnumSlbVirtServiceProxyIpPersistency.enum(kwargs.get('ProxyIpPersistency', None))
        self.ProxyIpNWclass = kwargs.get('ProxyIpNWclass', None)
        self.ProxyIpv6NWclass = kwargs.get('ProxyIpv6NWclass', None)
        self.ProxyIpNWclassPersistency = EnumSlbVirtServiceProxyIpNWclassPersistency.enum(kwargs.get('ProxyIpNWclassPersistency', None))
        self.HashLen = kwargs.get('HashLen', None)
        self.ClsRST = EnumSlbVirtServiceClsRST.enum(kwargs.get('ClsRST', None))
        self.HttpHdrName = kwargs.get('HttpHdrName', None)
        self.ServFastWa = kwargs.get('ServFastWa', None)
        self.AppwallWebappId = kwargs.get('AppwallWebappId', None)
        self.Http2 = kwargs.get('Http2', None)
        self.Cluster = EnumSlbVirtServiceCluster.enum(kwargs.get('Cluster', None))
        self.DataPort = kwargs.get('DataPort', None)

    def get_indexes(self):
        return self.ServSeventhPartIndex, self.SeventhPartIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'ServSeventhPartIndex', 'SeventhPartIndex',

