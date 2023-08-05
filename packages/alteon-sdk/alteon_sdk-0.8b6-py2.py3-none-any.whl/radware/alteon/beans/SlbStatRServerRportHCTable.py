
from radware.sdk.beans_common import *


class EnumSlbStatRServerRportHCStatus(BaseBeanEnum):
    up = 1
    failed = 2
    blocked = 3
    overflow = 4
    disabled = 5


class SlbStatRServerRportHCTable(DeviceBean):
    def __init__(self, **kwargs):
        self.HCRealIndex = kwargs.get('HCRealIndex', None)
        self.HCServIndex = kwargs.get('HCServIndex', None)
        self.HCId = kwargs.get('HCId', None)
        self.HCType = kwargs.get('HCType', None)
        self.HCStatus = EnumSlbStatRServerRportHCStatus.enum(kwargs.get('HCStatus', None))
        self.HCUptime = kwargs.get('HCUptime', None)
        self.HCDowntime = kwargs.get('HCDowntime', None)
        self.HCLastValidTime = kwargs.get('HCLastValidTime', None)
        self.HCAvgRespTime = kwargs.get('HCAvgRespTime', None)
        self.HCPeakRespTime = kwargs.get('HCPeakRespTime', None)
        self.HCLastValidRespTime = kwargs.get('HCLastValidRespTime', None)
        self.HCFailureCount = kwargs.get('HCFailureCount', None)

    def get_indexes(self):
        return self.HCRealIndex, self.HCServIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'HCRealIndex', 'HCServIndex',

