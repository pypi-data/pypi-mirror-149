
from radware.sdk.beans_common import *


class GslbEnhNetworkVirtsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Indx = kwargs.get('Indx', None)

    def get_indexes(self):
        return self.Index, self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Index', 'Indx',

