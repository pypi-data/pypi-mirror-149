
from radware.sdk.beans_common import *


class EnumBwmContractGroupDelete(BaseBeanEnum):
    other = 1
    delete = 2


class BwmNewCfgContractGroupTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.Contracts = kwargs.get('Contracts', None)
        self.AddCont = kwargs.get('AddCont', None)
        self.RemCont = kwargs.get('RemCont', None)
        self.Delete = EnumBwmContractGroupDelete.enum(kwargs.get('Delete', None))
        self.Name = kwargs.get('Name', None)

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

