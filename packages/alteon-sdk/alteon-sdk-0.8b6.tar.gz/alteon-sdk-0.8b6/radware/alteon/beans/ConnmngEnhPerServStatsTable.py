
from radware.sdk.beans_common import *


class ConnmngEnhPerServStatsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.VirtServIndex = kwargs.get('VirtServIndex', None)
        self.VirtServiceIndex = kwargs.get('VirtServiceIndex', None)
        self.VirtServPort = kwargs.get('VirtServPort', None)
        self.ServConn = kwargs.get('ServConn', None)
        self.CliReq = kwargs.get('CliReq', None)
        self.MulRatio = kwargs.get('MulRatio', None)

    def get_indexes(self):
        return self.VirtServIndex, self.VirtServiceIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'VirtServIndex', 'VirtServiceIndex',

