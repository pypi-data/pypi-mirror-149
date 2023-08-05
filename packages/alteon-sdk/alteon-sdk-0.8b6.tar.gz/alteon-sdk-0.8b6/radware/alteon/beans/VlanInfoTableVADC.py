
from radware.sdk.beans_common import *


class VlanInfoTableVADC(DeviceBean):
    def __init__(self, **kwargs):
        self.Idx = kwargs.get('Idx', None)
        self.VADC = kwargs.get('VADC', None)

    def get_indexes(self):
        return self.Idx,
    
    @classmethod
    def get_index_names(cls):
        return 'Idx',

