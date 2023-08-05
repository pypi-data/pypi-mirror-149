
from radware.sdk.beans_common import *


class Ip6GwStatsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.GwIndex = kwargs.get('GwIndex', None)
        self.Echoreq = kwargs.get('Echoreq', None)
        self.Echoresp = kwargs.get('Echoresp', None)
        self.Fails = kwargs.get('Fails', None)
        self.Master = kwargs.get('Master', None)
        self.IfIndex = kwargs.get('IfIndex', None)
        self.Retry = kwargs.get('Retry', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

