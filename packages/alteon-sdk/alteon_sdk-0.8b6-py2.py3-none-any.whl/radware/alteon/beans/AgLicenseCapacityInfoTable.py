
from radware.sdk.beans_common import *


class AgLicenseCapacityInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.licenseCapacityInfoIdx = kwargs.get('licenseCapacityInfoIdx', None)
        self.licenseCapacitySize = kwargs.get('licenseCapacitySize', None)
        self.licenseCapacityAllocated = kwargs.get('licenseCapacityAllocated', None)
        self.licenseCapacityPeakUsage = kwargs.get('licenseCapacityPeakUsage', None)
        self.licenseCapacityCurrUsage = kwargs.get('licenseCapacityCurrUsage', None)
        self.licenseCapacityPeakTimeStamp = kwargs.get('licenseCapacityPeakTimeStamp', None)

    def get_indexes(self):
        return self.licenseCapacityInfoIdx,
    
    @classmethod
    def get_index_names(cls):
        return 'licenseCapacityInfoIdx',

