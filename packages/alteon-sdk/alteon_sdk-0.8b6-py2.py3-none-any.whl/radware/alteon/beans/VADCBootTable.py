
from radware.sdk.beans_common import *


class EnumVADCBootAction(BaseBeanEnum):
    none = 1
    reset = 2


class VADCBootTable(DeviceBean):
    def __init__(self, **kwargs):
        self.VADCId = kwargs.get('VADCId', None)
        self.Action = EnumVADCBootAction.enum(kwargs.get('Action', None))

    def get_indexes(self):
        return self.VADCId,
    
    @classmethod
    def get_index_names(cls):
        return 'VADCId',

