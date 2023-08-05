
from radware.sdk.beans_common import *


class ErrorCountersSpTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.CntrIndex = kwargs.get('CntrIndex', None)
        self.StrName = kwargs.get('StrName', None)
        self.BaseVal = kwargs.get('BaseVal', None)

    def get_indexes(self):
        return self.Index, self.CntrIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'Index', 'CntrIndex',

