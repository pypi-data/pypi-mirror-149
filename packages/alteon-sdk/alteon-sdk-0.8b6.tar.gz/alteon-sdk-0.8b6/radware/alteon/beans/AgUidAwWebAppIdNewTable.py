
from radware.sdk.beans_common import *


class EnumAgAccessNewUserAwWebAppAddDelete(BaseBeanEnum):
    delete = 2
    add = 1


class AgUidAwWebAppIdNewTable(DeviceBean):
    def __init__(self, **kwargs):
        self.AccessNewUserIdx = kwargs.get('AccessNewUserIdx', None)
        self.AccessNewUserAwWebAppIdx = kwargs.get('AccessNewUserAwWebAppIdx', None)
        self.AccessNewUserAwWebAppAddDelete = EnumAgAccessNewUserAwWebAppAddDelete.enum(kwargs.get('AccessNewUserAwWebAppAddDelete', None))

    def get_indexes(self):
        return self.AccessNewUserIdx, self.AccessNewUserAwWebAppIdx,
    
    @classmethod
    def get_index_names(cls):
        return 'AccessNewUserIdx', 'AccessNewUserAwWebAppIdx',

