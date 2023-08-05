
from radware.sdk.beans_common import *


class HttpPerServStatsTable(DeviceBean):
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

    def get_indexes(self):
        return self.VirtServIndex, self.VirtServiceIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'VirtServIndex', 'VirtServiceIndex',

