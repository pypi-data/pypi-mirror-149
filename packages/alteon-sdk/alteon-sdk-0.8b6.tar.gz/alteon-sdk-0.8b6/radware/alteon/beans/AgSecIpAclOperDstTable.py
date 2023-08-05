
from radware.sdk.beans_common import *


class AgSecIpAclOperDstTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.Addr = kwargs.get('Addr', None)
        self.Mask = kwargs.get('Mask', None)
        self.Timeout = kwargs.get('Timeout', None)

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

