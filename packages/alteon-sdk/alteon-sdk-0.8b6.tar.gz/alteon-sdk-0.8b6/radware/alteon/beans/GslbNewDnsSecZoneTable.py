
from radware.sdk.beans_common import *


class EnumGslbDnsSecZoneStatus(BaseBeanEnum):
    enable = 1
    disable = 2


class EnumGslbDnsSecZoneParentIPVer(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2


class EnumGslbDnsSecZoneDelete(BaseBeanEnum):
    other = 1
    delete = 2


class GslbNewDnsSecZoneTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ID = kwargs.get('ID', None)
        self.Name = kwargs.get('Name', None)
        self.KSK1 = kwargs.get('KSK1', None)
        self.KSK2 = kwargs.get('KSK2', None)
        self.KSK3 = kwargs.get('KSK3', None)
        self.ZSK1 = kwargs.get('ZSK1', None)
        self.ZSK2 = kwargs.get('ZSK2', None)
        self.ZSK3 = kwargs.get('ZSK3', None)
        self.Status = EnumGslbDnsSecZoneStatus.enum(kwargs.get('Status', None))
        self.ParentIPVer = EnumGslbDnsSecZoneParentIPVer.enum(kwargs.get('ParentIPVer', None))
        self.ParentIPv4 = kwargs.get('ParentIPv4', None)
        self.ParentIPv6 = kwargs.get('ParentIPv6', None)
        self.Delete = EnumGslbDnsSecZoneDelete.enum(kwargs.get('Delete', None))
        self.ParentHost = kwargs.get('ParentHost', None)

    def get_indexes(self):
        return self.ID,
    
    @classmethod
    def get_index_names(cls):
        return 'ID',

