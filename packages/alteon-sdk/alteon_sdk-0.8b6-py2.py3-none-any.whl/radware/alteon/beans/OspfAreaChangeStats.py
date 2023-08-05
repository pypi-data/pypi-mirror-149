
from radware.sdk.beans_common import *


class OspfAreaChangeStats(DeviceBean):
    def __init__(self, **kwargs):
        self.IntfIndex = kwargs.get('IntfIndex', None)
        self.IntfHello = kwargs.get('IntfHello', None)
        self.IntfDown = kwargs.get('IntfDown', None)
        self.IntfLoop = kwargs.get('IntfLoop', None)
        self.IntfUnloop = kwargs.get('IntfUnloop', None)
        self.IntfWaitTimer = kwargs.get('IntfWaitTimer', None)
        self.IntfBackup = kwargs.get('IntfBackup', None)
        self.IntfNbrChange = kwargs.get('IntfNbrChange', None)

    def get_indexes(self):
        return self.IntfIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'IntfIndex',

