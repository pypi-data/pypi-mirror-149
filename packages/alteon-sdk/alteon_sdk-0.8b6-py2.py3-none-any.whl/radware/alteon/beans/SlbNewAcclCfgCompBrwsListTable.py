
from radware.sdk.beans_common import *


class EnumSlbAcclCompBrwsListAdminStatus(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclCompBrwsListDel(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewAcclCfgCompBrwsListTable(DeviceBean):
    def __init__(self, **kwargs):
        self.IdIndex = kwargs.get('IdIndex', None)
        self.Name = kwargs.get('Name', None)
        self.AdminStatus = EnumSlbAcclCompBrwsListAdminStatus.enum(kwargs.get('AdminStatus', None))
        self.Del = EnumSlbAcclCompBrwsListDel.enum(kwargs.get('Del', None))
        self.Copy = kwargs.get('Copy', None)

    def get_indexes(self):
        return self.IdIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'IdIndex',

