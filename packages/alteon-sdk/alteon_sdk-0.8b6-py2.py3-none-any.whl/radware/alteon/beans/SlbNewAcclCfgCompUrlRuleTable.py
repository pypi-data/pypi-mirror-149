
from radware.sdk.beans_common import *


class EnumSlbAcclCompUrlRuleDomainM(BaseBeanEnum):
    any = 1
    text = 2
    regex = 3


class EnumSlbAcclCompUrlRuleURLm(BaseBeanEnum):
    any = 1
    text = 2
    regex = 3


class EnumSlbAcclCompUrlRuleCompress(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclCompUrlRuleAdminStatus(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclCompUrlRuleDelete(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewAcclCfgCompUrlRuleTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ListIdIndex = kwargs.get('ListIdIndex', None)
        self.Index = kwargs.get('Index', None)
        self.Name = kwargs.get('Name', None)
        self.DomainM = EnumSlbAcclCompUrlRuleDomainM.enum(kwargs.get('DomainM', None))
        self.Domain = kwargs.get('Domain', None)
        self.URLm = EnumSlbAcclCompUrlRuleURLm.enum(kwargs.get('URLm', None))
        self.URL = kwargs.get('URL', None)
        self.Compress = EnumSlbAcclCompUrlRuleCompress.enum(kwargs.get('Compress', None))
        self.AdminStatus = EnumSlbAcclCompUrlRuleAdminStatus.enum(kwargs.get('AdminStatus', None))
        self.Delete = EnumSlbAcclCompUrlRuleDelete.enum(kwargs.get('Delete', None))
        self.Copy = kwargs.get('Copy', None)

    def get_indexes(self):
        return self.ListIdIndex, self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'ListIdIndex', 'Index',

