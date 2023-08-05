
from radware.sdk.beans_common import *


class CompPerBrowRuleListStatsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.BrowRuleListIndex = kwargs.get('BrowRuleListIndex', None)
        self.BrowRuleListId = kwargs.get('BrowRuleListId', None)
        self.BrowRuleListNumOfObj = kwargs.get('BrowRuleListNumOfObj', None)
        self.BrowRuleListSizeBefComp = kwargs.get('BrowRuleListSizeBefComp', None)
        self.BrowRuleListSizeAftComp = kwargs.get('BrowRuleListSizeAftComp', None)
        self.BrowRuleListCompRatio = kwargs.get('BrowRuleListCompRatio', None)

    def get_indexes(self):
        return self.BrowRuleListIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'BrowRuleListIndex',

