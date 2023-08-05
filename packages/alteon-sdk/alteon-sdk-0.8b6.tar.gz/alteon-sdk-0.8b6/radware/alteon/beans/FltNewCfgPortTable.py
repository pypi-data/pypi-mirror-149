
from radware.sdk.beans_common import *


class EnumFltPortState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class FltNewCfgPortTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.State = EnumFltPortState.enum(kwargs.get('State', None))
        self.FiltBmap = kwargs.get('FiltBmap', None)
        self.AddFiltRule = kwargs.get('AddFiltRule', None)
        self.RemFiltRule = kwargs.get('RemFiltRule', None)

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

