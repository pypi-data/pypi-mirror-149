
from radware.sdk.beans_common import *


class EnumSlbRealServerInfoHealthLayer(BaseBeanEnum):
    layer1 = 1
    layer3 = 3
    layer4 = 4


class EnumSlbRealServerInfoOverflow(BaseBeanEnum):
    overflow = 1
    no_overflow = 2


class EnumSlbRealServerInfoState(BaseBeanEnum):
    running = 2
    failed = 3
    disabled = 4


class SlbEnhRealServerInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.IpAddr = kwargs.get('IpAddr', None)
        self.MacAddr = kwargs.get('MacAddr', None)
        self.SwitchPort = kwargs.get('SwitchPort', None)
        self.HealthLayer = EnumSlbRealServerInfoHealthLayer.enum(kwargs.get('HealthLayer', None))
        self.Overflow = EnumSlbRealServerInfoOverflow.enum(kwargs.get('Overflow', None))
        self.State = EnumSlbRealServerInfoState.enum(kwargs.get('State', None))
        self.Vlan = kwargs.get('Vlan', None)
        self.Health = kwargs.get('Health', None)
        self.UpTime = kwargs.get('UpTime', None)
        self.DownTime = kwargs.get('DownTime', None)
        self.LastFailureTime = kwargs.get('LastFailureTime', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

