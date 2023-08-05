
from radware.sdk.beans_common import *


class EnumSlbSslSSLInspectFlowCriteriaAction(BaseBeanEnum):
    inspect = 1
    bypass = 2


class EnumSlbSslSSLInspectFlowCriteriaContMatch(BaseBeanEnum):
    none = 1
    urlcategories = 2
    hostnamelist = 3


class EnumSlbSslSSLInspectFlowCriteriaDelete(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewSslCfgSSLInspectFlowCriteriaTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.RuleId = kwargs.get('RuleId', None)
        self.HttpsFilter = kwargs.get('HttpsFilter', None)
        self.HttpFilter = kwargs.get('HttpFilter', None)
        self.Action = EnumSlbSslSSLInspectFlowCriteriaAction.enum(kwargs.get('Action', None))
        self.ContMatch = EnumSlbSslSSLInspectFlowCriteriaContMatch.enum(kwargs.get('ContMatch', None))
        self.Delete = EnumSlbSslSSLInspectFlowCriteriaDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.Index, self.RuleId,
    
    @classmethod
    def get_index_names(cls):
        return 'Index', 'RuleId',

