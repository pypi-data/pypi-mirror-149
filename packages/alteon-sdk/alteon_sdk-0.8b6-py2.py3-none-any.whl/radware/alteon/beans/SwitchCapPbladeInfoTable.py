
from radware.sdk.beans_common import *


class SwitchCapPbladeInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.PbladeId = kwargs.get('PbladeId', None)
        self.RamMax = kwargs.get('RamMax', None)
        self.RamCur = kwargs.get('RamCur', None)

    def get_indexes(self):
        return self.PbladeId,
    
    @classmethod
    def get_index_names(cls):
        return 'PbladeId',

