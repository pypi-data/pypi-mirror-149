
from radware.sdk.beans_common import *


class EnumOspfVisionAreaAuthType(BaseBeanEnum):
    none = 1
    password = 2
    md5 = 3


class EnumOspfVisionAreaType(BaseBeanEnum):
    transit = 1
    stub = 2
    nssa = 3


class EnumOspfVisionAreaState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumOspfVisionAreaDelete(BaseBeanEnum):
    other = 1
    delete = 2


class OspfNewCfgVisionAreaTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Id = kwargs.get('Id', None)
        self.SpfInterval = kwargs.get('SpfInterval', None)
        self.AuthType = EnumOspfVisionAreaAuthType.enum(kwargs.get('AuthType', None))
        self.Type = EnumOspfVisionAreaType.enum(kwargs.get('Type', None))
        self.Metric = kwargs.get('Metric', None)
        self.State = EnumOspfVisionAreaState.enum(kwargs.get('State', None))
        self.Delete = EnumOspfVisionAreaDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

