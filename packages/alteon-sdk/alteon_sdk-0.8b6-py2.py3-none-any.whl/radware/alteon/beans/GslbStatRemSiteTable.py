
from radware.sdk.beans_common import *


class GslbStatRemSiteTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Idx = kwargs.get('Idx', None)
        self.OutUpdates = kwargs.get('OutUpdates', None)
        self.InUpdates = kwargs.get('InUpdates', None)
        self.OutUpdates2 = kwargs.get('OutUpdates2', None)
        self.InUpdates2 = kwargs.get('InUpdates2', None)
        self.InBadUpdates = kwargs.get('InBadUpdates', None)

    def get_indexes(self):
        return self.Idx,
    
    @classmethod
    def get_index_names(cls):
        return 'Idx',

