
from radware.sdk.beans_common import *


class SlbStatEnhServiceActionNonGroupTable(DeviceBean):
    def __init__(self, **kwargs):
        self.VirtServIndex = kwargs.get('VirtServIndex', None)
        self.VirtServiceIndex = kwargs.get('VirtServiceIndex', None)
        self.CurrSess = kwargs.get('CurrSess', None)
        self.TotSess = kwargs.get('TotSess', None)
        self.HighSess = kwargs.get('HighSess', None)
        self.TotOcts = kwargs.get('TotOcts', None)

    def get_indexes(self):
        return self.VirtServIndex, self.VirtServiceIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'VirtServIndex', 'VirtServiceIndex',

