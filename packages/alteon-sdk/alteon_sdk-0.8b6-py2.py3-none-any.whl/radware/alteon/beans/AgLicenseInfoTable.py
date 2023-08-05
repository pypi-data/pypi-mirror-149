
from radware.sdk.beans_common import *


class EnumLicenseType(BaseBeanEnum):
    permanent = 1
    temporary = 2
    removed = 3
    expired = 4
    subscription = 5


class AgLicenseInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.licenseInfoIdx = kwargs.get('licenseInfoIdx', None)
        self.softwareKey = kwargs.get('softwareKey', None)
        self.licenseType = EnumLicenseType.enum(kwargs.get('licenseType', None))
        self.remainingDays = kwargs.get('remainingDays', None)
        self.remainingDaysLeft = kwargs.get('remainingDaysLeft', None)
        self.licenseSize = kwargs.get('licenseSize', None)
        self.licenseAllocated = kwargs.get('licenseAllocated', None)
        self.timeBasedLicenseStatus = kwargs.get('timeBasedLicenseStatus', None)

    def get_indexes(self):
        return self.licenseInfoIdx,
    
    @classmethod
    def get_index_names(cls):
        return 'licenseInfoIdx',

