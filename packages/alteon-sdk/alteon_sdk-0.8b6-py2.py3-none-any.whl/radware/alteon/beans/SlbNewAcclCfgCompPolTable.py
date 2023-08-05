
from radware.sdk.beans_common import *


class EnumSlbAcclCompPolAlgrthm(BaseBeanEnum):
    gzip = 1
    deflate = 2


class EnumSlbAcclCompPolPreDefBrwsRuleList(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclCompPolCompsrv(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclCompPolAdminStatus(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclCompPolDelete(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewAcclCfgCompPolTable(DeviceBean):
    def __init__(self, **kwargs):
        self.NameIdIndex = kwargs.get('NameIdIndex', None)
        self.Name = kwargs.get('Name', None)
        self.Algrthm = EnumSlbAcclCompPolAlgrthm.enum(kwargs.get('Algrthm', None))
        self.Complv1 = kwargs.get('Complv1', None)
        self.MinSize = kwargs.get('MinSize', None)
        self.MaxSize = kwargs.get('MaxSize', None)
        self.URLList = kwargs.get('URLList', None)
        self.BrwsList = kwargs.get('BrwsList', None)
        self.PreDefBrwsRuleList = EnumSlbAcclCompPolPreDefBrwsRuleList.enum(kwargs.get('PreDefBrwsRuleList', None))
        self.Compsrv = EnumSlbAcclCompPolCompsrv.enum(kwargs.get('Compsrv', None))
        self.AdminStatus = EnumSlbAcclCompPolAdminStatus.enum(kwargs.get('AdminStatus', None))
        self.Delete = EnumSlbAcclCompPolDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.NameIdIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'NameIdIndex',

