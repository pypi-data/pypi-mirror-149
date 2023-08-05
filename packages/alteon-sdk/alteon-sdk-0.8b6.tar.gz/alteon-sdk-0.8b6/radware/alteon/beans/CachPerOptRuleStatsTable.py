
from radware.sdk.beans_common import *


class CachPerOptRuleStatsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.OptRuleListIndex = kwargs.get('OptRuleListIndex', None)
        self.OptRuleIndex = kwargs.get('OptRuleIndex', None)
        self.OptRuleListId = kwargs.get('OptRuleListId', None)
        self.OptRuleNumOfHits = kwargs.get('OptRuleNumOfHits', None)

    def get_indexes(self):
        return self.OptRuleListIndex, self.OptRuleIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'OptRuleListIndex', 'OptRuleIndex',

