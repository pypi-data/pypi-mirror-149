
from radware.sdk.beans_common import *

#APM module is obsolete
class SlbEnhVirtServicesWithApmTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ServerWithApmIndex = kwargs.get('ServerWithApmIndex', None)
        self.WithApmIndex = kwargs.get('WithApmIndex', None)

    def get_indexes(self):
        return self.ServerWithApmIndex, self.WithApmIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'ServerWithApmIndex', 'WithApmIndex',

