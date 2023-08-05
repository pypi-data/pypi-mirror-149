
from radware.sdk.beans_common import *


class EnumOspfVirtIntfState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumOspfVirtIntfDelete(BaseBeanEnum):
    other = 1
    delete = 2


class OspfNewCfgVirtIntfTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.AreaId = kwargs.get('AreaId', None)
        self.Nbr = kwargs.get('Nbr', None)
        self.Mdkey = kwargs.get('Mdkey', None)
        self.Hello = kwargs.get('Hello', None)
        self.Dead = kwargs.get('Dead', None)
        self.Transit = kwargs.get('Transit', None)
        self.Retrans = kwargs.get('Retrans', None)
        self.Key = kwargs.get('Key', None)
        self.State = EnumOspfVirtIntfState.enum(kwargs.get('State', None))
        self.Delete = EnumOspfVirtIntfDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

