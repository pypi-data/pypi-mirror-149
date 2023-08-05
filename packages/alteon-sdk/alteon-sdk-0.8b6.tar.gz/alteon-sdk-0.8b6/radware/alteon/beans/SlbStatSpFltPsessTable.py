
from radware.sdk.beans_common import *


class SlbStatSpFltPsessTable(DeviceBean):
    def __init__(self, **kwargs):
        self.SpIndex = kwargs.get('SpIndex', None)
        self.Cur = kwargs.get('Cur', None)
        self.High = kwargs.get('High', None)
        self.Total = kwargs.get('Total', None)

    def get_indexes(self):
        return self.SpIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'SpIndex',

