
from radware.sdk.beans_common import *


class EnumVadcVrrpOperBackup(BaseBeanEnum):
    ok = 1
    backup = 2


class AgVadcVrrpOperTable(DeviceBean):
    def __init__(self, **kwargs):
        self.vadcVrrpOperIdx = kwargs.get('vadcVrrpOperIdx', None)
        self.vadcVrrpOperBackup = EnumVadcVrrpOperBackup.enum(kwargs.get('vadcVrrpOperBackup', None))

    def get_indexes(self):
        return self.vadcVrrpOperIdx,
    
    @classmethod
    def get_index_names(cls):
        return 'vadcVrrpOperIdx',

