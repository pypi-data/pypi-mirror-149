
from radware.sdk.beans_common import *


class StgStatsPortTable(DeviceBean):
    def __init__(self, **kwargs):
        self.StpIndex = kwargs.get('StpIndex', None)
        self.Index = kwargs.get('Index', None)
        self.RcvCfgBpdus = kwargs.get('RcvCfgBpdus', None)
        self.RcvTcnBpdus = kwargs.get('RcvTcnBpdus', None)
        self.XmtCfgBpdus = kwargs.get('XmtCfgBpdus', None)
        self.XmtTcnBpdus = kwargs.get('XmtTcnBpdus', None)
        self.RcvMrstBpdus = kwargs.get('RcvMrstBpdus', None)
        self.XmtMrstBpdus = kwargs.get('XmtMrstBpdus', None)

    def get_indexes(self):
        return self.StpIndex, self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'StpIndex', 'Index',

