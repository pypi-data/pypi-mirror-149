
from radware.sdk.beans_common import *


class CompPerBrowRuleStatsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.BrowRuleRuleListIndex = kwargs.get('BrowRuleRuleListIndex', None)
        self.BrowRuleIndex = kwargs.get('BrowRuleIndex', None)
        self.BrowRuleRuleListId = kwargs.get('BrowRuleRuleListId', None)
        self.BrowRuleNumOfObj = kwargs.get('BrowRuleNumOfObj', None)
        self.BrowRuleSizeBefComp = kwargs.get('BrowRuleSizeBefComp', None)
        self.BrowRuleSizeAftComp = kwargs.get('BrowRuleSizeAftComp', None)
        self.BrowRuleCompRatio = kwargs.get('BrowRuleCompRatio', None)

    def get_indexes(self):
        return self.BrowRuleRuleListIndex, self.BrowRuleIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'BrowRuleRuleListIndex', 'BrowRuleIndex',

