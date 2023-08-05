
from radware.sdk.beans_common import *


class EnumSlbNwclssNetworkClassesIpVer(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2


class EnumSlbNwclssNetworkClassesDel(BaseBeanEnum):
    other = 1
    delete = 2


class EnumSlbNwclssNetworkClassesType(BaseBeanEnum):
    address = 1
    region = 2


class SlbNewNwclssCfgNetworkClassesTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Id = kwargs.get('Id', None)
        self.Name = kwargs.get('Name', None)
        self.IpVer = EnumSlbNwclssNetworkClassesIpVer.enum(kwargs.get('IpVer', None))
        self.Del = EnumSlbNwclssNetworkClassesDel.enum(kwargs.get('Del', None))
        self.Copy = kwargs.get('Copy', None)
        self.Type = EnumSlbNwclssNetworkClassesType.enum(kwargs.get('Type', None))

    def get_indexes(self):
        return self.Id,
    
    @classmethod
    def get_index_names(cls):
        return 'Id',

