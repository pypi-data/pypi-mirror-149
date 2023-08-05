
from radware.sdk.beans_common import *


class EnumHaServicePref(BaseBeanEnum):
    active = 1
    standby = 2


class EnumHaServiceFailBackMode(BaseBeanEnum):
    onfailure = 1
    always = 2


class EnumHaServiceDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumHaServiceState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class HaServiceNewCfgTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Pref = EnumHaServicePref.enum(kwargs.get('Pref', None))
        self.FailBackMode = EnumHaServiceFailBackMode.enum(kwargs.get('FailBackMode', None))
        self.AddIf = kwargs.get('AddIf', None)
        self.RemIf = kwargs.get('RemIf', None)
        self.AddFip = kwargs.get('AddFip', None)
        self.RemFip = kwargs.get('RemFip', None)
        self.AddVip = kwargs.get('AddVip', None)
        self.RemVip = kwargs.get('RemVip', None)
        self.Adver = kwargs.get('Adver', None)
        self.Delete = EnumHaServiceDelete.enum(kwargs.get('Delete', None))
        self.State = EnumHaServiceState.enum(kwargs.get('State', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

