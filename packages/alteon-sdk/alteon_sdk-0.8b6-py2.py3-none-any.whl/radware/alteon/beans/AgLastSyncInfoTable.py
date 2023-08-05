
from radware.sdk.beans_common import *


class EnumLastSyncType(BaseBeanEnum):
    none = 1
    manual = 2
    auto = 3


class EnumLastSyncStatus(BaseBeanEnum):
    idle = 1
    in_progress = 2
    success = 3
    failure = 4


class EnumLastSuccessfulSyncType(BaseBeanEnum):
    none = 1
    manual = 2
    auto = 3


class AgLastSyncInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.lastSyncInfoIdx = kwargs.get('lastSyncInfoIdx', None)
        self.lastSyncPeerIp = kwargs.get('lastSyncPeerIp', None)
        self.lastSyncType = EnumLastSyncType.enum(kwargs.get('lastSyncType', None))
        self.lastSyncStatus = EnumLastSyncStatus.enum(kwargs.get('lastSyncStatus', None))
        self.lastSyncTime = kwargs.get('lastSyncTime', None)
        self.lastSyncFailReason = kwargs.get('lastSyncFailReason', None)
        self.lastSuccessfulSyncType = EnumLastSuccessfulSyncType.enum(kwargs.get('lastSuccessfulSyncType', None))
        self.lastSuccessfulSyncTime = kwargs.get('lastSuccessfulSyncTime', None)

    def get_indexes(self):
        return self.lastSyncInfoIdx,
    
    @classmethod
    def get_index_names(cls):
        return 'lastSyncInfoIdx',

