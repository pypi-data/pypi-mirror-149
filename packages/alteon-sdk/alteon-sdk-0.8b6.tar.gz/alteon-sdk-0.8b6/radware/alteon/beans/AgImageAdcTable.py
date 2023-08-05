
from radware.sdk.beans_common import *


class EnumAgImageAdcStatus(BaseBeanEnum):
    idle = 0
    active = 1
    assigned = 2
    incompatible = 3


class EnumAgImageAdcDefault(BaseBeanEnum):
    yes = 1
    no = 2


class EnumAgImageAdcFvStatus(BaseBeanEnum):
    compressed = 1
    extracted = 2
    na = 3


class AgImageAdcTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Version = kwargs.get('Version', None)
        self.DownloadTime = kwargs.get('DownloadTime', None)
        self.AssignedVadcs = kwargs.get('AssignedVadcs', None)
        self.Status = EnumAgImageAdcStatus.enum(kwargs.get('Status', None))
        self.Add = kwargs.get('Add', None)
        self.Remove = kwargs.get('Remove', None)
        self.Bmap = kwargs.get('Bmap', None)
        self.Default = EnumAgImageAdcDefault.enum(kwargs.get('Default', None))
        self.FvStatus = EnumAgImageAdcFvStatus.enum(kwargs.get('FvStatus', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

