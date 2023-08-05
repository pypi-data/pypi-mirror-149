
from radware.sdk.beans_common import *


class EnumSlbAcclOptExcListAdminStatus(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclOptExcListDel(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewAcclCfgOptExcListTable(DeviceBean):
    def __init__(self, **kwargs):
        self.IdIndex = kwargs.get('IdIndex', None)
        self.Name = kwargs.get('Name', None)
        self.AdminStatus = EnumSlbAcclOptExcListAdminStatus.enum(kwargs.get('AdminStatus', None))
        self.Del = EnumSlbAcclOptExcListDel.enum(kwargs.get('Del', None))
        self.Copy = kwargs.get('Copy', None)

    def get_indexes(self):
        return self.IdIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'IdIndex',

