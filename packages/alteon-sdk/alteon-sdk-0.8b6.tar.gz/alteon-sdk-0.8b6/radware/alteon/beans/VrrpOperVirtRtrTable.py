
from radware.sdk.beans_common import *


class EnumVrrpOperVirtRtrBackup(BaseBeanEnum):
    ok = 1
    backup = 2


class VrrpOperVirtRtrTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Backup = EnumVrrpOperVirtRtrBackup.enum(kwargs.get('Backup', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

