
from radware.sdk.beans_common import *


class PortMirrorStatsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.Ingress = kwargs.get('Ingress', None)
        self.Egress = kwargs.get('Egress', None)

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

