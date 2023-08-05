
from radware.sdk.beans_common import *


class HttpEnhPerServStatsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.VirtServIndex = kwargs.get('VirtServIndex', None)
        self.VirtServiceIndex = kwargs.get('VirtServiceIndex', None)
        self.VirtServPort = kwargs.get('VirtServPort', None)
        self.CliUseKeepAlive = kwargs.get('CliUseKeepAlive', None)
        self.Http10VsHttp11Ratio = kwargs.get('Http10VsHttp11Ratio', None)
        self.HttpToHTTPSRedir = kwargs.get('HttpToHTTPSRedir', None)
        self.AvgNumReqPerConn = kwargs.get('AvgNumReqPerConn', None)
        self.RespSmall1Kb = kwargs.get('RespSmall1Kb', None)
        self.Resp1KbTo10Kb = kwargs.get('Resp1KbTo10Kb', None)
        self.Resp11KbTo50Kb = kwargs.get('Resp11KbTo50Kb', None)
        self.Resp51KbTo100Kb = kwargs.get('Resp51KbTo100Kb', None)
        self.RespLarger100Kb = kwargs.get('RespLarger100Kb', None)
        self.ReqCliToAas = kwargs.get('ReqCliToAas', None)
        self.ReqAasToSer = kwargs.get('ReqAasToSer', None)
        self.RespSerToAas = kwargs.get('RespSerToAas', None)
        self.RespAasToCli = kwargs.get('RespAasToCli', None)
        self.TransRate = kwargs.get('TransRate', None)
        self.PerServStatsHttp20ConnectionCount = kwargs.get('PerServStatsHttp20ConnectionCount', None)
        self.PerServStatsHttp11ConnectionCount = kwargs.get('PerServStatsHttp11ConnectionCount', None)
        self.PerServStatsHttp10ConnectionCount = kwargs.get('PerServStatsHttp10ConnectionCount', None)
        self.PerServStatsHttp20ConnectionPeak = kwargs.get('PerServStatsHttp20ConnectionPeak', None)
        self.PerServStatsHttp11ConnectionPeak = kwargs.get('PerServStatsHttp11ConnectionPeak', None)
        self.PerServStatsHttp10ConnectionPeak = kwargs.get('PerServStatsHttp10ConnectionPeak', None)
        self.PerServStatsHttp20RequestCount = kwargs.get('PerServStatsHttp20RequestCount', None)
        self.PerServStatsHttp11RequestCount = kwargs.get('PerServStatsHttp11RequestCount', None)
        self.PerServStatsHttp10RequestCount = kwargs.get('PerServStatsHttp10RequestCount', None)
        self.PerServStatsBackendProxyConnections = kwargs.get('PerServStatsBackendProxyConnections', None)
        self.PerServStatsClientStreams = kwargs.get('PerServStatsClientStreams', None)
        self.PerServStatsPushStreams = kwargs.get('PerServStatsPushStreams', None)
        self.PerServStatsCanceledPushStreams = kwargs.get('PerServStatsCanceledPushStreams', None)
        self.PerServStatsConnectionDurationAvgStr = kwargs.get('PerServStatsConnectionDurationAvgStr', None)
        self.PerServStatsHeadersRequestCompRatio = kwargs.get('PerServStatsHeadersRequestCompRatio', None)
        self.PerServStatsHeadersResponseCompRatio = kwargs.get('PerServStatsHeadersResponseCompRatio', None)
        self.PerServStatsBigHeaders = kwargs.get('PerServStatsBigHeaders', None)
        self.PerServStatsAvgEvictionBytes = kwargs.get('PerServStatsAvgEvictionBytes', None)
        self.PerServStatsAvgHpackTableSize = kwargs.get('PerServStatsAvgHpackTableSize', None)
        self.PerServStatsPeakBackendProxyConnections = kwargs.get('PerServStatsPeakBackendProxyConnections', None)
        self.PerServStatsPeakClientStreams = kwargs.get('PerServStatsPeakClientStreams', None)
        self.PerServStatsPeakPushStreams = kwargs.get('PerServStatsPeakPushStreams', None)
        self.PerServStatsPeakCanceledPushStreams = kwargs.get('PerServStatsPeakCanceledPushStreams', None)
        self.PerServStatsPeakConnectionDurationAvgStr = kwargs.get('PerServStatsPeakConnectionDurationAvgStr', None)
        self.PerServStatsPeakHeadersRequestCompRatio = kwargs.get('PerServStatsPeakHeadersRequestCompRatio', None)
        self.PerServStatsPeakHeadersResponseCompRatio = kwargs.get('PerServStatsPeakHeadersResponseCompRatio', None)
        self.PerServStatsPeakBigHeaders = kwargs.get('PerServStatsPeakBigHeaders', None)
        self.PerServStatsPeakAvgEvictionBytes = kwargs.get('PerServStatsPeakAvgEvictionBytes', None)
        self.PerServStatsPeakAvgHpackTableSize = kwargs.get('PerServStatsPeakAvgHpackTableSize', None)

    def get_indexes(self):
        return self.VirtServIndex, self.VirtServiceIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'VirtServIndex', 'VirtServiceIndex',

