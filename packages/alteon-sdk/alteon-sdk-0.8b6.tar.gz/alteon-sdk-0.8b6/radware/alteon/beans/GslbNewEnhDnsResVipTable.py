
from radware.sdk.beans_common import *


class EnumGslbDnsResVipIPVer(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2


class EnumGslbDnsResVipStatus(BaseBeanEnum):
    enable = 1
    disable = 2


class EnumGslbDnsResVipDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumGslbDnsResVipRtsrcmac(BaseBeanEnum):
    enable = 1
    disable = 2


class GslbNewEnhDnsResVipTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index1 = kwargs.get('Index1', None)
        self.Index2 = kwargs.get('Index2', None)
        self.Name = kwargs.get('Name', None)
        self.IPVer = EnumGslbDnsResVipIPVer.enum(kwargs.get('IPVer', None))
        self.V4 = kwargs.get('V4', None)
        self.V6 = kwargs.get('V6', None)
        self.Status = EnumGslbDnsResVipStatus.enum(kwargs.get('Status', None))
        self.Delete = EnumGslbDnsResVipDelete.enum(kwargs.get('Delete', None))
        self.Rtsrcmac = EnumGslbDnsResVipRtsrcmac.enum(kwargs.get('Rtsrcmac', None))

    def get_indexes(self):
        return self.Index1, self.Index2,
    
    @classmethod
    def get_index_names(cls):
        return 'Index1', 'Index2',

