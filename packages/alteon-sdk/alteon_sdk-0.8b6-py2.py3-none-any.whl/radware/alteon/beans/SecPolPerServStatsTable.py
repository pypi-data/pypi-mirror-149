
from radware.sdk.beans_common import *


class SecPolPerServStatsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.VirtServIndex = kwargs.get('VirtServIndex', None)
        self.VirtServiceIndex = kwargs.get('VirtServiceIndex', None)
        self.VirtServPort = kwargs.get('VirtServPort', None)
        self.SecPolId = kwargs.get('SecPolId', None)
        self.BwCurVal = kwargs.get('BwCurVal', None)
        self.BwLastPeriodAvg = kwargs.get('BwLastPeriodAvg', None)
        self.BwCurPeriodAvg = kwargs.get('BwCurPeriodAvg', None)
        self.BwPeak = kwargs.get('BwPeak', None)
        self.BwPeakTimestamp = kwargs.get('BwPeakTimestamp', None)
        self.PPSCurVal = kwargs.get('PPSCurVal', None)
        self.PPSLastPeriodAvg = kwargs.get('PPSLastPeriodAvg', None)
        self.PPSCurPeriodAvg = kwargs.get('PPSCurPeriodAvg', None)
        self.PPSPeak = kwargs.get('PPSPeak', None)
        self.PPSPeakTimestamp = kwargs.get('PPSPeakTimestamp', None)
        self.CPSCurVal = kwargs.get('CPSCurVal', None)
        self.CPSLastPeriodAvg = kwargs.get('CPSLastPeriodAvg', None)
        self.CPSCurPeriodAvg = kwargs.get('CPSCurPeriodAvg', None)
        self.CPSPeak = kwargs.get('CPSPeak', None)
        self.CPSPeakTimestamp = kwargs.get('CPSPeakTimestamp', None)
        self.CECCurVal = kwargs.get('CECCurVal', None)
        self.CECLastPeriodAvg = kwargs.get('CECLastPeriodAvg', None)
        self.CECCurPeriodAvg = kwargs.get('CECCurPeriodAvg', None)
        self.CECPeak = kwargs.get('CECPeak', None)
        self.CECPeakTimestamp = kwargs.get('CECPeakTimestamp', None)
        self.LatencyCurVal = kwargs.get('LatencyCurVal', None)
        self.LatencyLastPeriodAvg = kwargs.get('LatencyLastPeriodAvg', None)
        self.LatencyCurPeriodAvg = kwargs.get('LatencyCurPeriodAvg', None)
        self.LatencyPeak = kwargs.get('LatencyPeak', None)
        self.LatencyPeakTimestamp = kwargs.get('LatencyPeakTimestamp', None)

    def get_indexes(self):
        return self.VirtServIndex, self.VirtServiceIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'VirtServIndex', 'VirtServiceIndex',

