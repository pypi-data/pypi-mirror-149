
from radware.sdk.beans_common import *


class EnumSlbAcclCompBrwsRuleAgentM(BaseBeanEnum):
    any = 1
    text = 2
    regex = 3


class EnumSlbAcclCompBrwsRuleContentM(BaseBeanEnum):
    any = 1
    text = 2
    regex = 3


class EnumSlbAcclCompBrwsRuleCompress(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclCompBrwsRuleAdminStatus(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclCompBrwsRuleDelete(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewAcclCfgCompBrwsRuleTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ListIdIndex = kwargs.get('ListIdIndex', None)
        self.Index = kwargs.get('Index', None)
        self.Name = kwargs.get('Name', None)
        self.AgentM = EnumSlbAcclCompBrwsRuleAgentM.enum(kwargs.get('AgentM', None))
        self.Agent = kwargs.get('Agent', None)
        self.ContentM = EnumSlbAcclCompBrwsRuleContentM.enum(kwargs.get('ContentM', None))
        self.Content = kwargs.get('Content', None)
        self.Compress = EnumSlbAcclCompBrwsRuleCompress.enum(kwargs.get('Compress', None))
        self.AdminStatus = EnumSlbAcclCompBrwsRuleAdminStatus.enum(kwargs.get('AdminStatus', None))
        self.Delete = EnumSlbAcclCompBrwsRuleDelete.enum(kwargs.get('Delete', None))
        self.Copy = kwargs.get('Copy', None)

    def get_indexes(self):
        return self.ListIdIndex, self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'ListIdIndex', 'Index',

