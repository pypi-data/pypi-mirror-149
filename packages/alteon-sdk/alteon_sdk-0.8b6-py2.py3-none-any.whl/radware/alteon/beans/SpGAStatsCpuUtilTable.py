
from radware.sdk.beans_common import *


class SpGAStatsCpuUtilTable(DeviceBean):
    def __init__(self, **kwargs):
        self.SpIndex = kwargs.get('SpIndex', None)
        self.UtilvADC = kwargs.get('UtilvADC', None)
        self.Util1Second = kwargs.get('Util1Second', None)
        self.Util4Seconds = kwargs.get('Util4Seconds', None)
        self.Util64Seconds = kwargs.get('Util64Seconds', None)

    def get_indexes(self):
        return self.SpIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'SpIndex',

