
from radware.sdk.beans_common import *


class Dot1dTpPortTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Port = kwargs.get('Port', None)
        self.MaxInfo = kwargs.get('MaxInfo', None)
        self.InFrames = kwargs.get('InFrames', None)
        self.OutFrames = kwargs.get('OutFrames', None)
        self.InDiscards = kwargs.get('InDiscards', None)

    def get_indexes(self):
        return self.Port,
    
    @classmethod
    def get_index_names(cls):
        return 'Port',

