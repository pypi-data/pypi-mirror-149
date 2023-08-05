
from radware.sdk.beans_common import *


class EnumBwmContTimePolicyDay(BaseBeanEnum):
    sunday = 1
    monday = 2
    tuesday = 3
    wednesday = 4
    thursday = 5
    friday = 6
    saturday = 7
    weekday = 8
    weekend = 9
    everyday = 10


class EnumBwmContTimePolicyState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumBwmContTimePolicyDelete(BaseBeanEnum):
    other = 1
    delete = 2


class BwmNewCfgContTimePolicyTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ContIndx = kwargs.get('ContIndx', None)
        self.Indx = kwargs.get('Indx', None)
        self.Day = EnumBwmContTimePolicyDay.enum(kwargs.get('Day', None))
        self.From = kwargs.get('From', None)
        self.To = kwargs.get('To', None)
        self.Pol = kwargs.get('Pol', None)
        self.State = EnumBwmContTimePolicyState.enum(kwargs.get('State', None))
        self.Delete = EnumBwmContTimePolicyDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.ContIndx, self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'ContIndx', 'Indx',

