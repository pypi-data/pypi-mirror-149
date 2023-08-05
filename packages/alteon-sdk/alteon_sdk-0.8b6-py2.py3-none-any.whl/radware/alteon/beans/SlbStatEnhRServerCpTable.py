
from radware.sdk.beans_common import *


class SlbStatEnhRServerCpTable(DeviceBean):
    def __init__(self, **kwargs):
        self.IndexCp = kwargs.get('IndexCp', None)
        self.CurrSessionsCp = kwargs.get('CurrSessionsCp', None)
        self.TotalSessionsCp = kwargs.get('TotalSessionsCp', None)
        self.FailuresCp = kwargs.get('FailuresCp', None)
        self.HighestSessionsCp = kwargs.get('HighestSessionsCp', None)
        self.HCOctetsLow32Cp = kwargs.get('HCOctetsLow32Cp', None)
        self.HCOctetsHigh32Cp = kwargs.get('HCOctetsHigh32Cp', None)
        self.HCOctetsCp = kwargs.get('HCOctetsCp', None)

    def get_indexes(self):
        return self.IndexCp,
    
    @classmethod
    def get_index_names(cls):
        return 'IndexCp',

