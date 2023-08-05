
from radware.sdk.beans_common import *


class CompStatPerServTable(DeviceBean):
    def __init__(self, **kwargs):
        self.VirtServIndex = kwargs.get('VirtServIndex', None)
        self.VirtServiceIndex = kwargs.get('VirtServiceIndex', None)
        self.VirtServPort = kwargs.get('VirtServPort', None)
        self.CompPolId = kwargs.get('CompPolId', None)
        self.UnComprTputKb = kwargs.get('UnComprTputKb', None)
        self.ComprTputKb = kwargs.get('ComprTputKb', None)
        self.AvgSizeBefComp = kwargs.get('AvgSizeBefComp', None)
        self.AvgSizeAftComp = kwargs.get('AvgSizeAftComp', None)
        self.AvgCompRatio = kwargs.get('AvgCompRatio', None)
        self.ThrputCompRatio = kwargs.get('ThrputCompRatio', None)
        self.BytesSaved = kwargs.get('BytesSaved', None)
        self.BytesSavedPeak = kwargs.get('BytesSavedPeak', None)
        self.BytesSavedTot = kwargs.get('BytesSavedTot', None)

    def get_indexes(self):
        return self.VirtServIndex, self.VirtServiceIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'VirtServIndex', 'VirtServiceIndex',

