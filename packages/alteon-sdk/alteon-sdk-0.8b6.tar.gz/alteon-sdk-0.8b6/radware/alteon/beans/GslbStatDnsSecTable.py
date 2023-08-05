
from radware.sdk.beans_common import *


class GslbStatDnsSecTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Idx = kwargs.get('Idx', None)
        self.TotalRequest = kwargs.get('TotalRequest', None)
        self.DnssecTotalRequest = kwargs.get('DnssecTotalRequest', None)
        self.DnssecRequestPercent = kwargs.get('DnssecRequestPercent', None)
        self.RequestPerSec = kwargs.get('RequestPerSec', None)
        self.DnssecRequestPerSec = kwargs.get('DnssecRequestPerSec', None)
        self.TcpRequest = kwargs.get('TcpRequest', None)
        self.UdpRequest = kwargs.get('UdpRequest', None)
        self.InvalidRequest = kwargs.get('InvalidRequest', None)
        self.NsecRecordAns = kwargs.get('NsecRecordAns', None)

    def get_indexes(self):
        return self.Idx,
    
    @classmethod
    def get_index_names(cls):
        return 'Idx',

