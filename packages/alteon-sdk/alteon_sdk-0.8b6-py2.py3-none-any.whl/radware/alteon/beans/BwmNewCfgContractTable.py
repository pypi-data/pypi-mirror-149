
from radware.sdk.beans_common import *


class EnumBwmContractState(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumBwmContractDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumBwmContractUseTos(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumBwmContractHistory(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumBwmContractShaping(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumBwmContractResizeTcp(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumBwmContractIpLimit(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumBwmContractIpType(BaseBeanEnum):
    sip = 1
    dip = 2


class EnumBwmContractMonitorMode(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumBwmContractRowType(BaseBeanEnum):
    regular = 1
    reserved = 2


class EnumBwmContractOperMode(BaseBeanEnum):
    ratelimiting = 1
    shaping = 2
    monitor = 3


class BwmNewCfgContractTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.Name = kwargs.get('Name', None)
        self.State = EnumBwmContractState.enum(kwargs.get('State', None))
        self.Policy = kwargs.get('Policy', None)
        self.Delete = EnumBwmContractDelete.enum(kwargs.get('Delete', None))
        self.Prec = kwargs.get('Prec', None)
        self.UseTos = EnumBwmContractUseTos.enum(kwargs.get('UseTos', None))
        self.History = EnumBwmContractHistory.enum(kwargs.get('History', None))
        self.Shaping = EnumBwmContractShaping.enum(kwargs.get('Shaping', None))
        self.ResizeTcp = EnumBwmContractResizeTcp.enum(kwargs.get('ResizeTcp', None))
        self.IpLimit = EnumBwmContractIpLimit.enum(kwargs.get('IpLimit', None))
        self.IpType = EnumBwmContractIpType.enum(kwargs.get('IpType', None))
        self.MonitorMode = EnumBwmContractMonitorMode.enum(kwargs.get('MonitorMode', None))
        self.Group = kwargs.get('Group', None)
        self.MaxSess = kwargs.get('MaxSess', None)
        self.RowType = EnumBwmContractRowType.enum(kwargs.get('RowType', None))
        self.OperMode = EnumBwmContractOperMode.enum(kwargs.get('OperMode', None))
        self.AlarmsPerSec = kwargs.get('AlarmsPerSec', None)
        self.PrefixLength = kwargs.get('PrefixLength', None)

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

