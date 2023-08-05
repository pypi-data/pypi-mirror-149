
from radware.sdk.beans_common import *


class EnumAgImageVxStatus(BaseBeanEnum):
    idle = 0
    active = 1


class AgImageVxTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Version = kwargs.get('Version', None)
        self.DownloadTime = kwargs.get('DownloadTime', None)
        self.Status = EnumAgImageVxStatus.enum(kwargs.get('Status', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

