
from radware.sdk.beans_common import *


class EnumGslbNetworkState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumGslbNetworkDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumGslbNetworkVer(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2


class EnumGslbNetworkClientAddrSrc(BaseBeanEnum):
    ldns = 1
    ecs = 2


class EnumGslbNetworkServType(BaseBeanEnum):
    group = 0
    server = 1


class EnumGslbNetworkSrcAddrType(BaseBeanEnum):
    address = 1
    network = 2


class GslbNewCfgEnhNetworkTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.State = EnumGslbNetworkState.enum(kwargs.get('State', None))
        self.SourceIp = kwargs.get('SourceIp', None)
        self.NetMask = kwargs.get('NetMask', None)
        self.Delete = EnumGslbNetworkDelete.enum(kwargs.get('Delete', None))
        self.AddVirtServer = kwargs.get('AddVirtServer', None)
        self.RemoveVirtServer = kwargs.get('RemoveVirtServer', None)
        self.AddRemRealServer = kwargs.get('AddRemRealServer', None)
        self.RemoveRemRealServer = kwargs.get('RemoveRemRealServer', None)
        self.SourceIpV6 = kwargs.get('SourceIpV6', None)
        self.Ver = EnumGslbNetworkVer.enum(kwargs.get('Ver', None))
        self.Sprefix = kwargs.get('Sprefix', None)
        self.AddRealServerAlphaNum = kwargs.get('AddRealServerAlphaNum', None)
        self.RemRealServerAlphaNum = kwargs.get('RemRealServerAlphaNum', None)
        self.AddEnhVirtServer = kwargs.get('AddEnhVirtServer', None)
        self.RemoveEnhVirtServer = kwargs.get('RemoveEnhVirtServer', None)
        self.ClassId = kwargs.get('ClassId', None)
        self.ClientAddrSrc = EnumGslbNetworkClientAddrSrc.enum(kwargs.get('ClientAddrSrc', None))
        self.ServType = EnumGslbNetworkServType.enum(kwargs.get('ServType', None))
        self.ServIp = kwargs.get('ServIp', None)
        self.SrcAddrType = EnumGslbNetworkSrcAddrType.enum(kwargs.get('SrcAddrType', None))
        self.WanGrp = kwargs.get('WanGrp', None)

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

