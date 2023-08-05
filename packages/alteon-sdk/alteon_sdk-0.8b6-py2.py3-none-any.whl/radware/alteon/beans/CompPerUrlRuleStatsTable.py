
from radware.sdk.beans_common import *


class CompPerUrlRuleStatsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.UrlRuleRuleListIndex = kwargs.get('UrlRuleRuleListIndex', None)
        self.UrlRuleIndex = kwargs.get('UrlRuleIndex', None)
        self.UrlRuleRuleListId = kwargs.get('UrlRuleRuleListId', None)
        self.UrlRuleNumOfObj = kwargs.get('UrlRuleNumOfObj', None)
        self.UrlRuleSizeBefComp = kwargs.get('UrlRuleSizeBefComp', None)
        self.UrlRuleSizeAftComp = kwargs.get('UrlRuleSizeAftComp', None)
        self.UrlRuleCompRatio = kwargs.get('UrlRuleCompRatio', None)

    def get_indexes(self):
        return self.UrlRuleRuleListIndex, self.UrlRuleIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'UrlRuleRuleListIndex', 'UrlRuleIndex',

