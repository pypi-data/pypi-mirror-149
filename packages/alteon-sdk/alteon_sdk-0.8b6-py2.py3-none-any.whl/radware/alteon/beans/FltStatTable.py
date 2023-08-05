
from radware.sdk.beans_common import *


class FltStatTable(DeviceBean):
    def __init__(self, **kwargs):
        self.FltIndex = kwargs.get('FltIndex', None)
        self.FltFirings = kwargs.get('FltFirings', None)

    def get_indexes(self):
        return self.FltIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'FltIndex',

