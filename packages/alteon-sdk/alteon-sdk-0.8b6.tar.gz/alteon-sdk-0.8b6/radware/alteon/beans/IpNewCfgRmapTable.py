
from radware.sdk.beans_common import *


class EnumIpRmapState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumIpRmapMetricType(BaseBeanEnum):
    none = 1
    type1 = 2
    type2 = 3


class EnumIpRmapDelete(BaseBeanEnum):
    other = 1
    delete = 2


class IpNewCfgRmapTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Lp = kwargs.get('Lp', None)
        self.Metric = kwargs.get('Metric', None)
        self.Prec = kwargs.get('Prec', None)
        self.Weight = kwargs.get('Weight', None)
        self.State = EnumIpRmapState.enum(kwargs.get('State', None))
        self.Ap = kwargs.get('Ap', None)
        self.MetricType = EnumIpRmapMetricType.enum(kwargs.get('MetricType', None))
        self.Delete = EnumIpRmapDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

