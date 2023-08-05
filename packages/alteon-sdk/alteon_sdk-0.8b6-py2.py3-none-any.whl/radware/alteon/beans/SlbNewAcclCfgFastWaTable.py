
from radware.sdk.beans_common import *


class EnumSlbAcclFastWaAdminStatus(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclFastWaDelete(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewAcclCfgFastWaTable(DeviceBean):
    def __init__(self, **kwargs):
        self.NameIdIndex = kwargs.get('NameIdIndex', None)
        self.AdminStatus = EnumSlbAcclFastWaAdminStatus.enum(kwargs.get('AdminStatus', None))
        self.Delete = EnumSlbAcclFastWaDelete.enum(kwargs.get('Delete', None))
        self.Name = kwargs.get('Name', None)
        self.Copy = kwargs.get('Copy', None)

    def get_indexes(self):
        return self.NameIdIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'NameIdIndex',

