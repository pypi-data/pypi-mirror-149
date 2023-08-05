
from radware.sdk.beans_common import *


class SlbStatAuxSessTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.CurConn = kwargs.get('CurConn', None)
        self.MaxConn = kwargs.get('MaxConn', None)
        self.AllocFails = kwargs.get('AllocFails', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

