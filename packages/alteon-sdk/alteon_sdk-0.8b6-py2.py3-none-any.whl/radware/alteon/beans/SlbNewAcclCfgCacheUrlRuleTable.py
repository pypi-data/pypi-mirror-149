
from radware.sdk.beans_common import *


class EnumSlbAcclCacheUrlRuleDomainM(BaseBeanEnum):
    any = 1
    text = 2
    regex = 3


class EnumSlbAcclCacheUrlRuleURLm(BaseBeanEnum):
    any = 1
    text = 2
    regex = 3


class EnumSlbAcclCacheUrlRuleCache(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclCacheUrlRuleAdminStatus(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclCacheUrlRuleDelete(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewAcclCfgCacheUrlRuleTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ListIdIndex = kwargs.get('ListIdIndex', None)
        self.Index = kwargs.get('Index', None)
        self.Name = kwargs.get('Name', None)
        self.DomainM = EnumSlbAcclCacheUrlRuleDomainM.enum(kwargs.get('DomainM', None))
        self.Domain = kwargs.get('Domain', None)
        self.URLm = EnumSlbAcclCacheUrlRuleURLm.enum(kwargs.get('URLm', None))
        self.URL = kwargs.get('URL', None)
        self.Expire = kwargs.get('Expire', None)
        self.Cache = EnumSlbAcclCacheUrlRuleCache.enum(kwargs.get('Cache', None))
        self.AdminStatus = EnumSlbAcclCacheUrlRuleAdminStatus.enum(kwargs.get('AdminStatus', None))
        self.Delete = EnumSlbAcclCacheUrlRuleDelete.enum(kwargs.get('Delete', None))
        self.Copy = kwargs.get('Copy', None)

    def get_indexes(self):
        return self.ListIdIndex, self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'ListIdIndex', 'Index',

