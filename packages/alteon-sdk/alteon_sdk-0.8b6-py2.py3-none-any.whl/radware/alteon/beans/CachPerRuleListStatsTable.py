
from radware.sdk.beans_common import *


class CachPerRuleListStatsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.RuleListIndex = kwargs.get('RuleListIndex', None)
        self.RuleListId = kwargs.get('RuleListId', None)
        self.RuleListNumOfObjCac = kwargs.get('RuleListNumOfObjCac', None)
        self.RuleListNumOfBytesCac = kwargs.get('RuleListNumOfBytesCac', None)

    def get_indexes(self):
        return self.RuleListId,
    
    @classmethod
    def get_index_names(cls):
        return 'RuleListId',

