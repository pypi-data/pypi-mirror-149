
from radware.sdk.beans_common import *


class EnumOspfv3IfNbrState(BaseBeanEnum):
    down = 1
    attempt = 2
    init = 3
    twoway = 4
    exStart = 5
    exchange = 6
    loading = 7
    full = 8


class Ospfv3IfNbrTable(DeviceBean):
    def __init__(self, **kwargs):
        self.VlanID = kwargs.get('VlanID', None)
        self.IpAddr = kwargs.get('IpAddr', None)
        self.Addr = kwargs.get('Addr', None)
        self.AreaID = kwargs.get('AreaID', None)
        self.IntfIndex = kwargs.get('IntfIndex', None)
        self.Option = kwargs.get('Option', None)
        self.Priority = kwargs.get('Priority', None)
        self.State = EnumOspfv3IfNbrState.enum(kwargs.get('State', None))
        self.No = kwargs.get('No', None)

    def get_indexes(self):
        return self.VlanID, self.IpAddr,
    
    @classmethod
    def get_index_names(cls):
        return 'VlanID', 'IpAddr',

