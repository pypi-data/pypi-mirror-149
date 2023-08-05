
from radware.sdk.beans_common import *


class SlbStatSapAslrTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Sampling = kwargs.get('Sampling', None)
        self.Failure = kwargs.get('Failure', None)
        self.DeviceUpdates = kwargs.get('DeviceUpdates', None)
        self.DeviceFailure = kwargs.get('DeviceFailure', None)
        self.LastAct = kwargs.get('LastAct', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

