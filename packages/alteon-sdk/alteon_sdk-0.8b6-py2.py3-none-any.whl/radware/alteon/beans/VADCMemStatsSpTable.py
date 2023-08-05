
from radware.sdk.beans_common import *


class VADCMemStatsSpTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Name = kwargs.get('Name', None)
        self.CurrentMemory = kwargs.get('CurrentMemory', None)
        self.HiWaterMark = kwargs.get('HiWaterMark', None)
        self.Maximum = kwargs.get('Maximum', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

