
from radware.sdk.beans_common import *


class EnumAgHcTcpPortNumDelete(BaseBeanEnum):
    other = 1
    delete = 2


class AgNewCfgHcTcpPortTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.Num = kwargs.get('Num', None)
        self.NumDelete = EnumAgHcTcpPortNumDelete.enum(kwargs.get('NumDelete', None))

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

