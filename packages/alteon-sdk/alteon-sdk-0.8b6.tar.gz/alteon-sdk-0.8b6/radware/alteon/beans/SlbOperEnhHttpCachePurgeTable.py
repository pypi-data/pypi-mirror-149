
from radware.sdk.beans_common import *


class SlbOperEnhHttpCachePurgeTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ServerIndex = kwargs.get('ServerIndex', None)
        self.ServiceIndex = kwargs.get('ServiceIndex', None)
        self.URL = kwargs.get('URL', None)

    def get_indexes(self):
        return self.ServerIndex, self.ServiceIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'ServerIndex', 'ServiceIndex',

