
from radware.sdk.beans_common import *


class EnumVADCOperAction(BaseBeanEnum):
    none = 1
    reassign = 2


class VADCOperTable(DeviceBean):
    def __init__(self, **kwargs):
        self.VADCId = kwargs.get('VADCId', None)
        self.Action = EnumVADCOperAction.enum(kwargs.get('Action', None))

    def get_indexes(self):
        return self.VADCId,
    
    @classmethod
    def get_index_names(cls):
        return 'VADCId',

