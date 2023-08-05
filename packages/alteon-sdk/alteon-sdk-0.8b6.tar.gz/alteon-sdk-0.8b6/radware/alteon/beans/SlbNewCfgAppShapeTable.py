
from radware.sdk.beans_common import *


class EnumSlbAppShapeState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAppShapeDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumSlbAppShapeDefault(BaseBeanEnum):
    other = 1
    default = 2


class SlbNewCfgAppShapeTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Name = kwargs.get('Name', None)
        self.State = EnumSlbAppShapeState.enum(kwargs.get('State', None))
        self.Delete = EnumSlbAppShapeDelete.enum(kwargs.get('Delete', None))
        self.Default = EnumSlbAppShapeDefault.enum(kwargs.get('Default', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

