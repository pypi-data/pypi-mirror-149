
from radware.sdk.beans_common import *


class CompPerUrlRuleListStatsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.UrlRuleListIndex = kwargs.get('UrlRuleListIndex', None)
        self.UrlRuleListId = kwargs.get('UrlRuleListId', None)
        self.UrlRuleListNumOfObj = kwargs.get('UrlRuleListNumOfObj', None)
        self.UrlRuleListSizeBefComp = kwargs.get('UrlRuleListSizeBefComp', None)
        self.UrlRuleListSizeAftComp = kwargs.get('UrlRuleListSizeAftComp', None)
        self.UrlRuleListCompRatio = kwargs.get('UrlRuleListCompRatio', None)

    def get_indexes(self):
        return self.UrlRuleListIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'UrlRuleListIndex',

