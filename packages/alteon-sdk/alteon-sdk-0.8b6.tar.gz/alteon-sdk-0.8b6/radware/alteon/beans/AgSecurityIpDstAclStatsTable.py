
from radware.sdk.beans_common import *


class AgSecurityIpDstAclStatsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.Address = kwargs.get('Address', None)
        self.BlockedPacket = kwargs.get('BlockedPacket', None)

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

