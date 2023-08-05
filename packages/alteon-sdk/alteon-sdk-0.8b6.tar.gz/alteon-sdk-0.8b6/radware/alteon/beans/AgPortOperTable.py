
from radware.sdk.beans_common import *


class EnumPortOperState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumPortOperRmon(BaseBeanEnum):
    enabled = 1
    disabled = 2


class AgPortOperTable(DeviceBean):
    def __init__(self, **kwargs):
        self.portOperIdx = kwargs.get('portOperIdx', None)
        self.portOperState = EnumPortOperState.enum(kwargs.get('portOperState', None))
        self.portOperRmon = EnumPortOperRmon.enum(kwargs.get('portOperRmon', None))

    def get_indexes(self):
        return self.portOperIdx,
    
    @classmethod
    def get_index_names(cls):
        return 'portOperIdx',

