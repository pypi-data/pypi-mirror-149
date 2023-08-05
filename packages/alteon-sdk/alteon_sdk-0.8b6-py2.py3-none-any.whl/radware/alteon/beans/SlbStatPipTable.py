
from radware.sdk.beans_common import *


class SlbStatPipTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Mask = kwargs.get('Mask', None)
        self.Used = kwargs.get('Used', None)
        self.Failure = kwargs.get('Failure', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

