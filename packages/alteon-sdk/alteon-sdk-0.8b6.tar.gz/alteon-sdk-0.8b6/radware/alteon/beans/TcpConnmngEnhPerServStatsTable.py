
from radware.sdk.beans_common import *


class TcpConnmngEnhPerServStatsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.VirtServIndex = kwargs.get('VirtServIndex', None)
        self.VirtServiceIndex = kwargs.get('VirtServiceIndex', None)
        self.VirtServPort = kwargs.get('VirtServPort', None)
        self.ServConn = kwargs.get('ServConn', None)
        self.ServConnReuse = kwargs.get('ServConnReuse', None)
        self.CliTrans = kwargs.get('CliTrans', None)
        self.MulRatio = kwargs.get('MulRatio', None)
        self.TotalServConn = kwargs.get('TotalServConn', None)
        self.TotalServConnReuse = kwargs.get('TotalServConnReuse', None)
        self.TotalCliTrans = kwargs.get('TotalCliTrans', None)
        self.TotalMulRatio = kwargs.get('TotalMulRatio', None)

    def get_indexes(self):
        return self.VirtServIndex, self.VirtServiceIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'VirtServIndex', 'VirtServiceIndex',

