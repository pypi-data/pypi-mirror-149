
from radware.sdk.beans_common import *


class EnumSlbFQDNServerIpVers(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2


class EnumSlbFQDNServerState(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumSlbFQDNServerDelete(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewCfgFQDNServerTable(DeviceBean):
    def __init__(self, **kwargs):
        self.IdIndex = kwargs.get('IdIndex', None)
        self.FQDN = kwargs.get('FQDN', None)
        self.IpVers = EnumSlbFQDNServerIpVers.enum(kwargs.get('IpVers', None))
        self.TTL = kwargs.get('TTL', None)
        self.Group = kwargs.get('Group', None)
        self.Templ = kwargs.get('Templ', None)
        self.State = EnumSlbFQDNServerState.enum(kwargs.get('State', None))
        self.Delete = EnumSlbFQDNServerDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.IdIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'IdIndex',

