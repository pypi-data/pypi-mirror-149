
from radware.sdk.beans_common import *


class GslbEnhNetworkRealsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.RealIndx = kwargs.get('RealIndx', None)

    def get_indexes(self):
        return self.Indx, self.RealIndx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx', 'RealIndx',

