
from radware.sdk.beans_common import *


class EnumSlbAcclCacheUrlListAdminStatus(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclCacheUrlListDel(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewAcclCfgCacheUrlListTable(DeviceBean):
    def __init__(self, **kwargs):
        self.IdIndex = kwargs.get('IdIndex', None)
        self.Name = kwargs.get('Name', None)
        self.AdminStatus = EnumSlbAcclCacheUrlListAdminStatus.enum(kwargs.get('AdminStatus', None))
        self.Del = EnumSlbAcclCacheUrlListDel.enum(kwargs.get('Del', None))
        self.Copy = kwargs.get('Copy', None)

    def get_indexes(self):
        return self.IdIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'IdIndex',

