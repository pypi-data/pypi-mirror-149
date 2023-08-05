
from radware.sdk.beans_common import *


class EnumSlbSerAppShapeDelete(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewCfgEnhSerAppShapeTable(DeviceBean):
    def __init__(self, **kwargs):
        self.VirtServIndex = kwargs.get('VirtServIndex', None)
        self.VirtServiceIndex = kwargs.get('VirtServiceIndex', None)
        self.Priority = kwargs.get('Priority', None)
        self.Index = kwargs.get('Index', None)
        self.Delete = EnumSlbSerAppShapeDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.VirtServIndex, self.VirtServiceIndex, self.Priority,
    
    @classmethod
    def get_index_names(cls):
        return 'VirtServIndex', 'VirtServiceIndex', 'Priority',

