
from radware.sdk.beans_common import *


class EnumSlbSmartNatType(BaseBeanEnum):
    nonat = 0
    static = 1
    dynamic = 2


class EnumSlbSmartNatIpVer(BaseBeanEnum):
    ipv4 = 0
    ipv6 = 1


class EnumSlbSmartNatMode(BaseBeanEnum):
    address = 0
    nwclass = 1
    none = 2


class EnumSlbSmartNatDnatMode(BaseBeanEnum):
    address = 0
    nwclass = 1
    none = 2


class EnumSlbSmartNatDel(BaseBeanEnum):
    other = 1
    delete = 2


class EnumSlbSmartNatDnatPersist(BaseBeanEnum):
    none = 1
    host = 2
    client = 3


class SlbNewCfgSmartNatTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Name = kwargs.get('Name', None)
        self.Type = EnumSlbSmartNatType.enum(kwargs.get('Type', None))
        self.IpVer = EnumSlbSmartNatIpVer.enum(kwargs.get('IpVer', None))
        self.Mode = EnumSlbSmartNatMode.enum(kwargs.get('Mode', None))
        self.LocalIpV4 = kwargs.get('LocalIpV4', None)
        self.LocalIpV4Mask = kwargs.get('LocalIpV4Mask', None)
        self.LocalIpV6 = kwargs.get('LocalIpV6', None)
        self.LocalIpV6Mask = kwargs.get('LocalIpV6Mask', None)
        self.LocalNwclss = kwargs.get('LocalNwclss', None)
        self.DnatMode = EnumSlbSmartNatDnatMode.enum(kwargs.get('DnatMode', None))
        self.DnatIpV4 = kwargs.get('DnatIpV4', None)
        self.DnatIpV4Mask = kwargs.get('DnatIpV4Mask', None)
        self.DnatIpV6 = kwargs.get('DnatIpV6', None)
        self.DnatIpV6Mask = kwargs.get('DnatIpV6Mask', None)
        self.DnatNwclss = kwargs.get('DnatNwclss', None)
        self.WanLink = kwargs.get('WanLink', None)
        self.Del = EnumSlbSmartNatDel.enum(kwargs.get('Del', None))
        self.DnatPersist = EnumSlbSmartNatDnatPersist.enum(kwargs.get('DnatPersist', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

