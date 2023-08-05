
from radware.sdk.beans_common import *


class CachPerServStatTable(DeviceBean):
    def __init__(self, **kwargs):
        self.StatPerServVirtServIndex = kwargs.get('StatPerServVirtServIndex', None)
        self.StatPerServVirtServiceIndex = kwargs.get('StatPerServVirtServiceIndex', None)
        self.StatPerServVirtServPort = kwargs.get('StatPerServVirtServPort', None)
        self.StatPerServCachePolId = kwargs.get('StatPerServCachePolId', None)
        self.StatPerServTotObj = kwargs.get('StatPerServTotObj', None)
        self.StatPerServHitPerc = kwargs.get('StatPerServHitPerc', None)
        self.StatPerServServRate = kwargs.get('StatPerServServRate', None)
        self.StatPerServNewCachedObj = kwargs.get('StatPerServNewCachedObj', None)
        self.StatPerServPeakNewCachedObj = kwargs.get('StatPerServPeakNewCachedObj', None)
        self.StatPerServRateNewCachedObj = kwargs.get('StatPerServRateNewCachedObj', None)
        self.StatPerServNewCachedBytes = kwargs.get('StatPerServNewCachedBytes', None)
        self.StatPerServRateNewCachedBytes = kwargs.get('StatPerServRateNewCachedBytes', None)
        self.StatPerServObjSmaller10K = kwargs.get('StatPerServObjSmaller10K', None)
        self.StatPerServObj11KTO50K = kwargs.get('StatPerServObj11KTO50K', None)
        self.StatPerServObj51KTO100K = kwargs.get('StatPerServObj51KTO100K', None)
        self.StatPerServObj101KTO1M = kwargs.get('StatPerServObj101KTO1M', None)
        self.StatPerServObjLarger1M = kwargs.get('StatPerServObjLarger1M', None)

    def get_indexes(self):
        return self.StatPerServVirtServIndex, self.StatPerServVirtServiceIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'StatPerServVirtServIndex', 'StatPerServVirtServiceIndex',

