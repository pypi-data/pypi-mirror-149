
from radware.sdk.beans_common import *


class EnumLayer7ContentClassFileNameMatchType(BaseBeanEnum):
    sufx = 1
    prefx = 2
    equal = 3
    include = 4
    regex = 5


class EnumLayer7ContentClassFileNameCase(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumLayer7ContentClassFileNameDelete(BaseBeanEnum):
    other = 1
    delete = 2


class Layer7NewCfgContentClassFileNameTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ContentClassID = kwargs.get('ContentClassID', None)
        self.ID = kwargs.get('ID', None)
        self.FileName = kwargs.get('FileName', None)
        self.MatchType = EnumLayer7ContentClassFileNameMatchType.enum(kwargs.get('MatchType', None))
        self.Case = EnumLayer7ContentClassFileNameCase.enum(kwargs.get('Case', None))
        self.Delete = EnumLayer7ContentClassFileNameDelete.enum(kwargs.get('Delete', None))
        self.Copy = kwargs.get('Copy', None)

    def get_indexes(self):
        return self.ContentClassID, self.ID,
    
    @classmethod
    def get_index_names(cls):
        return 'ContentClassID', 'ID',

