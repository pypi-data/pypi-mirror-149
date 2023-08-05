
from radware.sdk.beans_common import *


class EventCountersTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.StrName = kwargs.get('StrName', None)
        self.BaseVal = kwargs.get('BaseVal', None)
        self.HistVal15sec = kwargs.get('HistVal15sec', None)
        self.HistVal30sec = kwargs.get('HistVal30sec', None)
        self.HistVal45sec = kwargs.get('HistVal45sec', None)
        self.HistVal60sec = kwargs.get('HistVal60sec', None)
        self.HistVal75sec = kwargs.get('HistVal75sec', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

