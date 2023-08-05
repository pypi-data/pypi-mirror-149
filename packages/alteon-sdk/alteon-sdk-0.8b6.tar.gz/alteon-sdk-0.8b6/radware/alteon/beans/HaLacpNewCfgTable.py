
from radware.sdk.beans_common import *


class EnumHaLacpLacpRemove(BaseBeanEnum):
    other = 1
    delete = 2


class HaLacpNewCfgTable(DeviceBean):
    def __init__(self, **kwargs):
        self.AdminKey = kwargs.get('AdminKey', None)
        self.LacpUpCriteria = kwargs.get('LacpUpCriteria', None)
        self.LacpRemove = EnumHaLacpLacpRemove.enum(kwargs.get('LacpRemove', None))

    def get_indexes(self):
        return self.AdminKey,
    
    @classmethod
    def get_index_names(cls):
        return 'AdminKey',

