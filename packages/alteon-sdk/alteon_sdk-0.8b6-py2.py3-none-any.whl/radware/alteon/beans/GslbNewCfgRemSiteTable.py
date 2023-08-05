
from radware.sdk.beans_common import *


class EnumGslbRemSiteState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumGslbRemSiteUpdate(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumGslbRemSiteDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumGslbRemSitePrimaryIPVer(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2


class EnumGslbRemSiteSecondaryIPVer(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2


class EnumGslbRemSitePeer(BaseBeanEnum):
    enabled = 1
    disabled = 2


class GslbNewCfgRemSiteTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.PrimaryIp = kwargs.get('PrimaryIp', None)
        self.SecondaryIp = kwargs.get('SecondaryIp', None)
        self.State = EnumGslbRemSiteState.enum(kwargs.get('State', None))
        self.Update = EnumGslbRemSiteUpdate.enum(kwargs.get('Update', None))
        self.Delete = EnumGslbRemSiteDelete.enum(kwargs.get('Delete', None))
        self.Name = kwargs.get('Name', None)
        self.PrimaryIPVer = EnumGslbRemSitePrimaryIPVer.enum(kwargs.get('PrimaryIPVer', None))
        self.PrimaryIp6 = kwargs.get('PrimaryIp6', None)
        self.SecondaryIPVer = EnumGslbRemSiteSecondaryIPVer.enum(kwargs.get('SecondaryIPVer', None))
        self.SecondaryIp6 = kwargs.get('SecondaryIp6', None)
        self.Peer = EnumGslbRemSitePeer.enum(kwargs.get('Peer', None))

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

