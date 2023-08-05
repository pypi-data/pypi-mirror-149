
from radware.sdk.beans_common import *


class EnumGslbInfoVirtServerRegion(BaseBeanEnum):
    unknown = 0
    northamerica = 1
    southamerica = 2
    europe = 3
    caribbean = 4
    pacificrim = 5
    subsahara = 6
    japan = 7
    caribbeansubsahara = 8
    africa = 9


class GslbInfoEnhVirtServerTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Idx = kwargs.get('Idx', None)
        self.ServiceIdx = kwargs.get('ServiceIdx', None)
        self.RserverIdx = kwargs.get('RserverIdx', None)
        self.Dname = kwargs.get('Dname', None)
        self.VirtPort = kwargs.get('VirtPort', None)
        self.IpAddress = kwargs.get('IpAddress', None)
        self.Response = kwargs.get('Response', None)
        self.SessAvail = kwargs.get('SessAvail', None)
        self.SessCur = kwargs.get('SessCur', None)
        self.SessMax = kwargs.get('SessMax', None)
        self.SessUtil = kwargs.get('SessUtil', None)
        self.CpuUtil = kwargs.get('CpuUtil', None)
        self.RemSite = kwargs.get('RemSite', None)
        self.Weight = kwargs.get('Weight', None)
        self.Avail = kwargs.get('Avail', None)
        self.Region = EnumGslbInfoVirtServerRegion.enum(kwargs.get('Region', None))

    def get_indexes(self):
        return self.Idx, self.ServiceIdx, self.RserverIdx,
    
    @classmethod
    def get_index_names(cls):
        return 'Idx', 'ServiceIdx', 'RserverIdx',

