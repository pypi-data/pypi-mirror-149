
from radware.sdk.beans_common import *


class VatdStatsCpuUtilTable(DeviceBean):
    def __init__(self, **kwargs):
        self.VatdIndex = kwargs.get('VatdIndex', None)
        self.Util1Second = kwargs.get('Util1Second', None)
        self.Util64Seconds = kwargs.get('Util64Seconds', None)

    def get_indexes(self):
        return self.VatdIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'VatdIndex',

