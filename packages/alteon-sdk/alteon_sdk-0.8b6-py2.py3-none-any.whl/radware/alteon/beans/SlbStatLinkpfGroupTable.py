
from radware.sdk.beans_common import *


class SlbStatLinkpfGroupTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.CurrUpBw = kwargs.get('CurrUpBw', None)
        self.CurrDnBw = kwargs.get('CurrDnBw', None)
        self.CurrTotBw = kwargs.get('CurrTotBw', None)
        self.CurrSess = kwargs.get('CurrSess', None)
        self.LastClearTmSt = kwargs.get('LastClearTmSt', None)
        self.TotUpBw = kwargs.get('TotUpBw', None)
        self.TotDnBw = kwargs.get('TotDnBw', None)
        self.TotBw = kwargs.get('TotBw', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

