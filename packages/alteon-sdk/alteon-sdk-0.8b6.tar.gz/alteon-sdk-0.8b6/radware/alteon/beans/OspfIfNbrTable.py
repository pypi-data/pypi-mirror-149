
from radware.sdk.beans_common import *


class EnumOspfIfNbrState(BaseBeanEnum):
    down = 1
    attempt = 2
    init = 3
    twoway = 4
    exStart = 5
    exchange = 6
    loading = 7
    full = 8


class OspfIfNbrTable(DeviceBean):
    def __init__(self, **kwargs):
        self.IntfIndex = kwargs.get('IntfIndex', None)
        self.IpAddr = kwargs.get('IpAddr', None)
        self.Priority = kwargs.get('Priority', None)
        self.State = EnumOspfIfNbrState.enum(kwargs.get('State', None))
        self.DesignatedRtr = kwargs.get('DesignatedRtr', None)
        self.BackupDesignatedRtr = kwargs.get('BackupDesignatedRtr', None)
        self.IpAddress = kwargs.get('IpAddress', None)

    def get_indexes(self):
        return self.IntfIndex, self.IpAddr,
    
    @classmethod
    def get_index_names(cls):
        return 'IntfIndex', 'IpAddr',

