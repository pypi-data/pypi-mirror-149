
from radware.sdk.beans_common import *


class EnumOspfIntfState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumOspfIntfDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumOspfIntfBfd(BaseBeanEnum):
    on = 1
    off = 2


class OspfNewCfgIntfTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Id = kwargs.get('Id', None)
        self.Mdkey = kwargs.get('Mdkey', None)
        self.AreaId = kwargs.get('AreaId', None)
        self.Priority = kwargs.get('Priority', None)
        self.Cost = kwargs.get('Cost', None)
        self.Hello = kwargs.get('Hello', None)
        self.Dead = kwargs.get('Dead', None)
        self.Transit = kwargs.get('Transit', None)
        self.Retrans = kwargs.get('Retrans', None)
        self.Key = kwargs.get('Key', None)
        self.State = EnumOspfIntfState.enum(kwargs.get('State', None))
        self.Delete = EnumOspfIntfDelete.enum(kwargs.get('Delete', None))
        self.Bfd = EnumOspfIntfBfd.enum(kwargs.get('Bfd', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

