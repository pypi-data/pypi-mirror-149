
from radware.sdk.beans_common import *


class AgSecurityPgrpStatsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.Name = kwargs.get('Name', None)
        self.Hits = kwargs.get('Hits', None)

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

