
from radware.sdk.beans_common import *


class HaServiceRealTable(DeviceBean):
    def __init__(self, **kwargs):
        self.GrpIndex = kwargs.get('GrpIndex', None)
        self.Index = kwargs.get('Index', None)

    def get_indexes(self):
        return self.GrpIndex, self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'GrpIndex', 'Index',

