
from radware.sdk.beans_common import *


class EnumFdbState(BaseBeanEnum):
    unknown = 1
    ignore = 2
    forward = 3
    flood = 4
    ffd = 5
    trunk = 6
    vir = 7
    vsr = 8
    vpr = 9
    other = 10


class FdbTable(DeviceBean):
    def __init__(self, **kwargs):
        self.MacAddr = kwargs.get('MacAddr', None)
        self.Vlan = kwargs.get('Vlan', None)
        self.SrcPort = kwargs.get('SrcPort', None)
        self.State = EnumFdbState.enum(kwargs.get('State', None))
        self.Age = kwargs.get('Age', None)
        self.RefPorts = kwargs.get('RefPorts', None)
        self.RefSps = kwargs.get('RefSps', None)
        self.LearnedPort = kwargs.get('LearnedPort', None)
        self.SrcTrunk = kwargs.get('SrcTrunk', None)

    def get_indexes(self):
        return self.MacAddr,
    
    @classmethod
    def get_index_names(cls):
        return 'MacAddr',

