
from radware.sdk.beans_common import *


class StpInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.TimeSinceTopChange = kwargs.get('TimeSinceTopChange', None)
        self.TopChanges = kwargs.get('TopChanges', None)
        self.DesignatedRoot = kwargs.get('DesignatedRoot', None)
        self.RootCost = kwargs.get('RootCost', None)
        self.RootPort = kwargs.get('RootPort', None)
        self.MaxAge = kwargs.get('MaxAge', None)
        self.HelloTime = kwargs.get('HelloTime', None)
        self.ForwardDelay = kwargs.get('ForwardDelay', None)
        self.HoldTime = kwargs.get('HoldTime', None)
        self.TimeSinceTopChangeStr = kwargs.get('TimeSinceTopChangeStr', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

