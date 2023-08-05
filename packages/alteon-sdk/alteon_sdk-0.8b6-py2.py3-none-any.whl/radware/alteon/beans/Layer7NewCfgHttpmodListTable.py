
from radware.sdk.beans_common import *


class EnumLayer7HttpmodListAdminStatus(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumLayer7HttpmodListDelete(BaseBeanEnum):
    other = 1
    delete = 2


class Layer7NewCfgHttpmodListTable(DeviceBean):
    def __init__(self, **kwargs):
        self.NameIdIndex = kwargs.get('NameIdIndex', None)
        self.Name = kwargs.get('Name', None)
        self.AdminStatus = EnumLayer7HttpmodListAdminStatus.enum(kwargs.get('AdminStatus', None))
        self.Copy = kwargs.get('Copy', None)
        self.Delete = EnumLayer7HttpmodListDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.NameIdIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'NameIdIndex',

