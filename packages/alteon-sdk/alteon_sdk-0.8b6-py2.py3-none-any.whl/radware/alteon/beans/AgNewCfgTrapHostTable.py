
from radware.sdk.beans_common import *


class AgNewCfgTrapHostTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.IpAddr = kwargs.get('IpAddr', None)
        self.CommString = kwargs.get('CommString', None)

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

