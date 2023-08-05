
from radware.sdk.beans_common import *


class CachPerRuleStatsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.RuleRuleListIndex = kwargs.get('RuleRuleListIndex', None)
        self.RuleIndex = kwargs.get('RuleIndex', None)
        self.RuleRuleListId = kwargs.get('RuleRuleListId', None)
        self.RuleNumOfObjCac = kwargs.get('RuleNumOfObjCac', None)
        self.RuleNumOfBytesCac = kwargs.get('RuleNumOfBytesCac', None)

    def get_indexes(self):
        return self.RuleRuleListIndex, self.RuleIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'RuleRuleListIndex', 'RuleIndex',

