
from radware.sdk.beans_common import *


class StgVlanNewCfgTable(DeviceBean):
    def __init__(self, **kwargs):
        self.VlanId = kwargs.get('VlanId', None)
        self.VlanName = kwargs.get('VlanName', None)

    def get_indexes(self):
        return self.VlanId,
    
    @classmethod
    def get_index_names(cls):
        return 'VlanId',

