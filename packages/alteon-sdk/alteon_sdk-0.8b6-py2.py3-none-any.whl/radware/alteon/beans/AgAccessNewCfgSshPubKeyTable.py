
from radware.sdk.beans_common import *


class EnumAgAccessSshPubKeyDelete(BaseBeanEnum):
    other = 1
    delete = 2


class AgAccessNewCfgSshPubKeyTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ID = kwargs.get('ID', None)
        self.Name = kwargs.get('Name', None)
        self.Delete = EnumAgAccessSshPubKeyDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.ID,
    
    @classmethod
    def get_index_names(cls):
        return 'ID',

