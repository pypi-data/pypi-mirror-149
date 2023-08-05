
from radware.sdk.beans_common import *


class EnumSlbFiltAppShapeDelete(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewCfgFiltAppShapeTable(DeviceBean):
    def __init__(self, **kwargs):
        self.FiltIndex = kwargs.get('FiltIndex', None)
        self.Priority = kwargs.get('Priority', None)
        self.Index = kwargs.get('Index', None)
        self.Delete = EnumSlbFiltAppShapeDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.FiltIndex, self.Priority,
    
    @classmethod
    def get_index_names(cls):
        return 'FiltIndex', 'Priority',

