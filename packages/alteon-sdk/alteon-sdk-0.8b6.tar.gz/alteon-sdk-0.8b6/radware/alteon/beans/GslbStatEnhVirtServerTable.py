
from radware.sdk.beans_common import *


class GslbStatEnhVirtServerTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Idx = kwargs.get('Idx', None)
        self.ServiceIdx = kwargs.get('ServiceIdx', None)
        self.RserverIdx = kwargs.get('RserverIdx', None)
        self.VirtPort = kwargs.get('VirtPort', None)
        self.IpAddress = kwargs.get('IpAddress', None)
        self.ResponseTime = kwargs.get('ResponseTime', None)
        self.MinSessAvail = kwargs.get('MinSessAvail', None)
        self.Dname = kwargs.get('Dname', None)
        self.RemSite = kwargs.get('RemSite', None)
        self.DnsDirect = kwargs.get('DnsDirect', None)
        self.Ipv6Address = kwargs.get('Ipv6Address', None)
        self.HttpRedirs = kwargs.get('HttpRedirs', None)

    def get_indexes(self):
        return self.Idx, self.ServiceIdx, self.RserverIdx,
    
    @classmethod
    def get_index_names(cls):
        return 'Idx', 'ServiceIdx', 'RserverIdx',

