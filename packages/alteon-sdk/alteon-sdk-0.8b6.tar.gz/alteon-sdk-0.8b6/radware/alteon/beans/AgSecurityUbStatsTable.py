
from radware.sdk.beans_common import *


class AgSecurityUbStatsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.Port = kwargs.get('Port', None)
        self.BlockedPacket = kwargs.get('BlockedPacket', None)
        self.PacketRate = kwargs.get('PacketRate', None)

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

