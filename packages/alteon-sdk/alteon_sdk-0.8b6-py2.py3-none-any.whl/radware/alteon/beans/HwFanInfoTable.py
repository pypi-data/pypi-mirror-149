
from radware.sdk.beans_common import *


class EnumHwFanInfoStatus(BaseBeanEnum):
    notRelevant = 0
    ok = 1
    failed = 2
    unplugged = 3
    empty = 4


class EnumHwFanInfoIsCritical(BaseBeanEnum):
    no = 0
    yes = 1
    notRelevant = 2


class HwFanInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Status = EnumHwFanInfoStatus.enum(kwargs.get('Status', None))
        self.TotalCount = kwargs.get('TotalCount', None)
        self.CountFailed = kwargs.get('CountFailed', None)
        self.IsCritical = EnumHwFanInfoIsCritical.enum(kwargs.get('IsCritical', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

