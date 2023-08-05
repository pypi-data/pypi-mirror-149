
from radware.sdk.beans_common import *


class EnumSnmphcInvert(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSnmphcDeleteHc(BaseBeanEnum):
    other = 1
    delete = 2


class EnumSnmphcUseWeight(BaseBeanEnum):
    enabled = 1
    disabled = 2


class SnmphcNewCfgTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Oid = kwargs.get('Oid', None)
        self.CommString = kwargs.get('CommString', None)
        self.RcvContent = kwargs.get('RcvContent', None)
        self.Invert = EnumSnmphcInvert.enum(kwargs.get('Invert', None))
        self.DeleteHc = EnumSnmphcDeleteHc.enum(kwargs.get('DeleteHc', None))
        self.UseWeight = EnumSnmphcUseWeight.enum(kwargs.get('UseWeight', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

