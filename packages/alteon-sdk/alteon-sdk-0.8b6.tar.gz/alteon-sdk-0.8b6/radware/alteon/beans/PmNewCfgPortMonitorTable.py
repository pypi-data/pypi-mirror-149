
from radware.sdk.beans_common import *


class EnumPmPmirrDirection(BaseBeanEnum):
    in_ = 1
    out = 2
    both = 3


class EnumPmPmirrDelete(BaseBeanEnum):
    other = 1
    delete = 2


class PmNewCfgPortMonitorTable(DeviceBean):
    def __init__(self, **kwargs):
        self.PmirrMoniPortIndex = kwargs.get('PmirrMoniPortIndex', None)
        self.PmirrMirrPortIndex = kwargs.get('PmirrMirrPortIndex', None)
        self.PmirrDirection = EnumPmPmirrDirection.enum(kwargs.get('PmirrDirection', None))
        self.PmirrDelete = EnumPmPmirrDelete.enum(kwargs.get('PmirrDelete', None))
        self.AddVlan = kwargs.get('AddVlan', None)
        self.RemoveVlan = kwargs.get('RemoveVlan', None)
        self.PmirrPortVlansBmap = kwargs.get('PmirrPortVlansBmap', None)

    def get_indexes(self):
        return self.PmirrMoniPortIndex, self.PmirrMirrPortIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'PmirrMoniPortIndex', 'PmirrMirrPortIndex',

