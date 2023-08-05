
from radware.sdk.beans_common import *


class EnumOspfAreaAuthType(BaseBeanEnum):
    none = 1
    password = 2
    md5 = 3


class EnumOspfAreaType(BaseBeanEnum):
    transit = 1
    stub = 2
    nssa = 3


class EnumOspfAreaState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumOspfAreaDelete(BaseBeanEnum):
    other = 1
    delete = 2


class OspfNewCfgAreaTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Id = kwargs.get('Id', None)
        self.SpfInterval = kwargs.get('SpfInterval', None)
        self.AuthType = EnumOspfAreaAuthType.enum(kwargs.get('AuthType', None))
        self.Type = EnumOspfAreaType.enum(kwargs.get('Type', None))
        self.Metric = kwargs.get('Metric', None)
        self.State = EnumOspfAreaState.enum(kwargs.get('State', None))
        self.Delete = EnumOspfAreaDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.Index, self.Id,
    
    @classmethod
    def get_index_names(cls):
        return 'Index', 'Id',

