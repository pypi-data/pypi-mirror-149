
from radware.sdk.beans_common import *


class CachPerOptListStatsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.OptListIndex = kwargs.get('OptListIndex', None)
        self.OptListId = kwargs.get('OptListId', None)
        self.OptListNumOfHits = kwargs.get('OptListNumOfHits', None)

    def get_indexes(self):
        return self.OptListId,
    
    @classmethod
    def get_index_names(cls):
        return 'OptListId',

