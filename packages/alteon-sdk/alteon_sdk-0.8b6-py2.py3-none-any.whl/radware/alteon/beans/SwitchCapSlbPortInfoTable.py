
from radware.sdk.beans_common import *


class EnumSwitchCapSlbPortClientState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSwitchCapSlbPortSerState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSwitchCapSlbPortRTSState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class SwitchCapSlbPortInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.ClientState = EnumSwitchCapSlbPortClientState.enum(kwargs.get('ClientState', None))
        self.SerState = EnumSwitchCapSlbPortSerState.enum(kwargs.get('SerState', None))
        self.FltState = kwargs.get('FltState', None)
        self.RTSState = EnumSwitchCapSlbPortRTSState.enum(kwargs.get('RTSState', None))

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

