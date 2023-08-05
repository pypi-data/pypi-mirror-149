
from radware.sdk.beans_common import *


class EnumSlbPortSlbState(BaseBeanEnum):
    none = 1
    client = 2
    server = 3
    client_server = 4


class EnumSlbPortSlbHotStandby(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbPortSlbInterSwitch(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbPortSlbPipState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbPortSlbRtsState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbPortDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumSlbPortSlbIdslbState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbPortSlbFilter(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbPortSlbServState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbPortSlbClntState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbPortSlbL3Filter(BaseBeanEnum):
    enabled = 1
    disabled = 2


class SlbNewCfgPortTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.SlbState = EnumSlbPortSlbState.enum(kwargs.get('SlbState', None))
        self.SlbHotStandby = EnumSlbPortSlbHotStandby.enum(kwargs.get('SlbHotStandby', None))
        self.SlbInterSwitch = EnumSlbPortSlbInterSwitch.enum(kwargs.get('SlbInterSwitch', None))
        self.SlbPipState = EnumSlbPortSlbPipState.enum(kwargs.get('SlbPipState', None))
        self.SlbRtsState = EnumSlbPortSlbRtsState.enum(kwargs.get('SlbRtsState', None))
        self.Delete = EnumSlbPortDelete.enum(kwargs.get('Delete', None))
        self.SlbIdslbState = EnumSlbPortSlbIdslbState.enum(kwargs.get('SlbIdslbState', None))
        self.SlbFilter = EnumSlbPortSlbFilter.enum(kwargs.get('SlbFilter', None))
        self.SlbAddFilter = kwargs.get('SlbAddFilter', None)
        self.SlbRemFilter = kwargs.get('SlbRemFilter', None)
        self.SlbServState = EnumSlbPortSlbServState.enum(kwargs.get('SlbServState', None))
        self.SlbClntState = EnumSlbPortSlbClntState.enum(kwargs.get('SlbClntState', None))
        self.SlbL3Filter = EnumSlbPortSlbL3Filter.enum(kwargs.get('SlbL3Filter', None))
        self.SlbFilterBmap = kwargs.get('SlbFilterBmap', None)
        self.InterSwitchVlan = kwargs.get('InterSwitchVlan', None)
        self.VlanBmap = kwargs.get('VlanBmap', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

