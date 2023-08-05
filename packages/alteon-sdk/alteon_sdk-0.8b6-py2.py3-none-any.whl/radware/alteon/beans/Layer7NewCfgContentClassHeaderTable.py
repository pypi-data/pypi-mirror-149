
from radware.sdk.beans_common import *


class EnumLayer7ContentClassHeaderMatchTypeName(BaseBeanEnum):
    equal = 3
    include = 4
    regex = 5


class EnumLayer7ContentClassHeaderMatchTypeVal(BaseBeanEnum):
    equal = 3
    include = 4
    regex = 5


class EnumLayer7ContentClassHeaderCase(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumLayer7ContentClassHeaderDelete(BaseBeanEnum):
    other = 1
    delete = 2


class Layer7NewCfgContentClassHeaderTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ContentClassID = kwargs.get('ContentClassID', None)
        self.ID = kwargs.get('ID', None)
        self.Name = kwargs.get('Name', None)
        self.Val = kwargs.get('Val', None)
        self.MatchTypeName = EnumLayer7ContentClassHeaderMatchTypeName.enum(kwargs.get('MatchTypeName', None))
        self.MatchTypeVal = EnumLayer7ContentClassHeaderMatchTypeVal.enum(kwargs.get('MatchTypeVal', None))
        self.Case = EnumLayer7ContentClassHeaderCase.enum(kwargs.get('Case', None))
        self.Delete = EnumLayer7ContentClassHeaderDelete.enum(kwargs.get('Delete', None))
        self.Copy = kwargs.get('Copy', None)

    def get_indexes(self):
        return self.ContentClassID, self.ID,
    
    @classmethod
    def get_index_names(cls):
        return 'ContentClassID', 'ID',

