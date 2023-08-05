
from radware.sdk.beans_common import *


class OspfIntfChangeStats(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Hello = kwargs.get('Hello', None)
        self.Down = kwargs.get('Down', None)
        self.Loop = kwargs.get('Loop', None)
        self.Unloop = kwargs.get('Unloop', None)
        self.WaitTimer = kwargs.get('WaitTimer', None)
        self.Backup = kwargs.get('Backup', None)
        self.NbrChange = kwargs.get('NbrChange', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

