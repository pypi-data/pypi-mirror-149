
from radware.sdk.beans_common import *


class EnumLayer7ContentClassCookieMatchTypeKey(BaseBeanEnum):
    equal = 3
    include = 4
    regex = 5


class EnumLayer7ContentClassCookieMatchTypeVal(BaseBeanEnum):
    equal = 3
    include = 4
    regex = 5


class EnumLayer7ContentClassCookieCase(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumLayer7ContentClassCookieDelete(BaseBeanEnum):
    other = 1
    delete = 2


class Layer7NewCfgContentClassCookieTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ContentClassID = kwargs.get('ContentClassID', None)
        self.ID = kwargs.get('ID', None)
        self.Key = kwargs.get('Key', None)
        self.Val = kwargs.get('Val', None)
        self.MatchTypeKey = EnumLayer7ContentClassCookieMatchTypeKey.enum(kwargs.get('MatchTypeKey', None))
        self.MatchTypeVal = EnumLayer7ContentClassCookieMatchTypeVal.enum(kwargs.get('MatchTypeVal', None))
        self.Case = EnumLayer7ContentClassCookieCase.enum(kwargs.get('Case', None))
        self.Delete = EnumLayer7ContentClassCookieDelete.enum(kwargs.get('Delete', None))
        self.Copy = kwargs.get('Copy', None)

    def get_indexes(self):
        return self.ContentClassID, self.ID,
    
    @classmethod
    def get_index_names(cls):
        return 'ContentClassID', 'ID',

