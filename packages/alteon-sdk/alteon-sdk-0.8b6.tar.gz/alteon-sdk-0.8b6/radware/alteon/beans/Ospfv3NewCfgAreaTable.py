
from radware.sdk.beans_common import *


class EnumOspfv3AreaType(BaseBeanEnum):
    transit = 1
    stub = 2
    nssa = 3


class EnumOspfv3AreaMType(BaseBeanEnum):
    v3 = 1
    compare_cost = 2
    non_compare = 3


class EnumOspfv3AreaSummary(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumOspfv3AreaTrRole(BaseBeanEnum):
    always = 1
    candidate = 2


class EnumOspfv3AreaState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumOspfv3AreaDelete(BaseBeanEnum):
    other = 1
    delete = 2


class Ospfv3NewCfgAreaTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Id = kwargs.get('Id', None)
        self.SpfInterval = kwargs.get('SpfInterval', None)
        self.Type = EnumOspfv3AreaType.enum(kwargs.get('Type', None))
        self.Metric = kwargs.get('Metric', None)
        self.MType = EnumOspfv3AreaMType.enum(kwargs.get('MType', None))
        self.Summary = EnumOspfv3AreaSummary.enum(kwargs.get('Summary', None))
        self.TrRole = EnumOspfv3AreaTrRole.enum(kwargs.get('TrRole', None))
        self.State = EnumOspfv3AreaState.enum(kwargs.get('State', None))
        self.Delete = EnumOspfv3AreaDelete.enum(kwargs.get('Delete', None))
        self.IDRW = kwargs.get('IDRW', None)

    def get_indexes(self):
        return self.Index, self.Id,
    
    @classmethod
    def get_index_names(cls):
        return 'Index', 'Id',

