
from radware.sdk.beans_common import *


class PortStatsPerSecTable(DeviceBean):
    def __init__(self, **kwargs):
        self.PortNumber = kwargs.get('PortNumber', None)
        self.InOctetsPerSec = kwargs.get('InOctetsPerSec', None)
        self.InPktsPerSec = kwargs.get('InPktsPerSec', None)
        self.InDiscardsPerSec = kwargs.get('InDiscardsPerSec', None)
        self.InErrorsPerSec = kwargs.get('InErrorsPerSec', None)
        self.OutOctetsPerSec = kwargs.get('OutOctetsPerSec', None)
        self.OutPktsPerSec = kwargs.get('OutPktsPerSec', None)
        self.OutDiscardsPerSec = kwargs.get('OutDiscardsPerSec', None)
        self.OutErrorsPerSec = kwargs.get('OutErrorsPerSec', None)

    def get_indexes(self):
        return self.PortNumber,
    
    @classmethod
    def get_index_names(cls):
        return 'PortNumber',

