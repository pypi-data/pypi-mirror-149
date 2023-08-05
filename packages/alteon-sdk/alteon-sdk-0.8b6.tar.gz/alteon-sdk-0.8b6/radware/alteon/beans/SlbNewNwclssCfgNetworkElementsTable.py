
from radware.sdk.beans_common import *


class EnumSlbNwclssNetworkElementsNetType(BaseBeanEnum):
    subnet = 1
    range = 2


class EnumSlbNwclssNetworkElementsMatchType(BaseBeanEnum):
    include = 1
    exclude = 2


class EnumSlbNwclssNetworkElementsDel(BaseBeanEnum):
    other = 1
    delete = 2


class EnumSlbNwclssNetworkTypeAddrOrRegn(BaseBeanEnum):
    address = 1
    region = 2


class SlbNewNwclssCfgNetworkElementsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.NcId = kwargs.get('NcId', None)
        self.Id = kwargs.get('Id', None)
        self.NetType = EnumSlbNwclssNetworkElementsNetType.enum(kwargs.get('NetType', None))
        self.Ip = kwargs.get('Ip', None)
        self.Mask = kwargs.get('Mask', None)
        self.FromIp = kwargs.get('FromIp', None)
        self.ToIp = kwargs.get('ToIp', None)
        self.Ipv6Addr = kwargs.get('Ipv6Addr', None)
        self.PrefixLen = kwargs.get('PrefixLen', None)
        self.FromIpv6Addr = kwargs.get('FromIpv6Addr', None)
        self.ToIpv6Addr = kwargs.get('ToIpv6Addr', None)
        self.MatchType = EnumSlbNwclssNetworkElementsMatchType.enum(kwargs.get('MatchType', None))
        self.Del = EnumSlbNwclssNetworkElementsDel.enum(kwargs.get('Del', None))
        self.RegCont = kwargs.get('RegCont', None)
        self.RegCountry = kwargs.get('RegCountry', None)
        self.RegState = kwargs.get('RegState', None)
        self.TypeAddrOrRegn = EnumSlbNwclssNetworkTypeAddrOrRegn.enum(kwargs.get('TypeAddrOrRegn', None))

    def get_indexes(self):
        return self.NcId, self.Id,
    
    @classmethod
    def get_index_names(cls):
        return 'NcId', 'Id',

