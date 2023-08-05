
from radware.sdk.beans_common import *


class EnumVADCInfoStatus(BaseBeanEnum):
    disabled = 0
    init = 1
    running = 2
    down = 3
    stopping = 4
    restarting = 5
    querying = 6


class EnumVADCInfoVRRPStatus(BaseBeanEnum):
    init = 1
    master = 2
    backup = 3
    holdoff = 4
    off = 5
    active = 6
    standby = 7
    activestar = 8
    none = 9


class VADCInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Id = kwargs.get('Id', None)
        self.Name = kwargs.get('Name', None)
        self.Status = EnumVADCInfoStatus.enum(kwargs.get('Status', None))
        self.VRRPStatus = EnumVADCInfoVRRPStatus.enum(kwargs.get('VRRPStatus', None))
        self.CU = kwargs.get('CU', None)
        self.Throughput = kwargs.get('Throughput', None)
        self.Limit = kwargs.get('Limit', None)
        self.SPcpu = kwargs.get('SPcpu', None)
        self.MPcpu = kwargs.get('MPcpu', None)
        self.CUMbit = kwargs.get('CUMbit', None)
        self.UpTime = kwargs.get('UpTime', None)
        self.ThrputUtil = kwargs.get('ThrputUtil', None)
        self.ElasticCoreAllocMPcpuSize = kwargs.get('ElasticCoreAllocMPcpuSize', None)

    def get_indexes(self):
        return self.Id,
    
    @classmethod
    def get_index_names(cls):
        return 'Id',

