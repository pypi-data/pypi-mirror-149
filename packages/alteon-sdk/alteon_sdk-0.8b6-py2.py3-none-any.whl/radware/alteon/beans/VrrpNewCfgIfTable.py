
from radware.sdk.beans_common import *


class EnumVrrpIfAuthType(BaseBeanEnum):
    none = 1
    simple_text_password = 2


class EnumVrrpIfDelete(BaseBeanEnum):
    other = 1
    delete = 2


class VrrpNewCfgIfTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.AuthType = EnumVrrpIfAuthType.enum(kwargs.get('AuthType', None))
        self.Passwd = kwargs.get('Passwd', None)
        self.Delete = EnumVrrpIfDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

