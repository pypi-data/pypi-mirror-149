
from radware.sdk.beans_common import *


class EnumSlbPortClientState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbPortSerState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbPortFltState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbPortRTSState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbPortHotStandbyState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbPortInterSWState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbPortProxyState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbPortIdSlbState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbPortSymantecState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class SlbPortInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.ClientState = EnumSlbPortClientState.enum(kwargs.get('ClientState', None))
        self.SerState = EnumSlbPortSerState.enum(kwargs.get('SerState', None))
        self.FltState = EnumSlbPortFltState.enum(kwargs.get('FltState', None))
        self.RTSState = EnumSlbPortRTSState.enum(kwargs.get('RTSState', None))
        self.HotStandbyState = EnumSlbPortHotStandbyState.enum(kwargs.get('HotStandbyState', None))
        self.InterSWState = EnumSlbPortInterSWState.enum(kwargs.get('InterSWState', None))
        self.ProxyState = EnumSlbPortProxyState.enum(kwargs.get('ProxyState', None))
        self.IdSlbState = EnumSlbPortIdSlbState.enum(kwargs.get('IdSlbState', None))
        self.SymantecState = EnumSlbPortSymantecState.enum(kwargs.get('SymantecState', None))
        self.FitersAdded = kwargs.get('FitersAdded', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

