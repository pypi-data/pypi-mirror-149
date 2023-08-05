
from radware.sdk.beans_common import *


class SslBeOffPerCiphServStatsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.VirtServIndex = kwargs.get('VirtServIndex', None)
        self.VirtServiceIndex = kwargs.get('VirtServiceIndex', None)
        self.VirtCiphIndex = kwargs.get('VirtCiphIndex', None)
        self.CiphName = kwargs.get('CiphName', None)
        self.NewhandShake = kwargs.get('NewhandShake', None)
        self.VirtServPort = kwargs.get('VirtServPort', None)
        self.NewhandShakeTotal = kwargs.get('NewhandShakeTotal', None)

    def get_indexes(self):
        return self.VirtServIndex, self.VirtServiceIndex, self.VirtCiphIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'VirtServIndex', 'VirtServiceIndex', 'VirtCiphIndex',

