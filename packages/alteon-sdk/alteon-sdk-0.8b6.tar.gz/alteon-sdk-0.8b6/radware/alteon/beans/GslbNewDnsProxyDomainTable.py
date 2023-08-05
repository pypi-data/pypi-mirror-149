
from radware.sdk.beans_common import *


class EnumGslbDnsProxyDomainDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumGslbDnsProxyDomainState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class GslbNewDnsProxyDomainTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Id = kwargs.get('Id', None)
        self.Name = kwargs.get('Name', None)
        self.Group = kwargs.get('Group', None)
        self.Delete = EnumGslbDnsProxyDomainDelete.enum(kwargs.get('Delete', None))
        self.State = EnumGslbDnsProxyDomainState.enum(kwargs.get('State', None))

    def get_indexes(self):
        return self.Id,
    
    @classmethod
    def get_index_names(cls):
        return 'Id',

