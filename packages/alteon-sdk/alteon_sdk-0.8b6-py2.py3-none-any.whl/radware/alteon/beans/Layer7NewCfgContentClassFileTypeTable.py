
from radware.sdk.beans_common import *


class EnumLayer7ContentClassFileTypeMatchType(BaseBeanEnum):
    sufx = 1
    prefx = 2
    equal = 3
    include = 4
    regex = 5


class EnumLayer7ContentClassFileTypeCase(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumLayer7ContentClassFileTypeDelete(BaseBeanEnum):
    other = 1
    delete = 2


class Layer7NewCfgContentClassFileTypeTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ContentClassID = kwargs.get('ContentClassID', None)
        self.ID = kwargs.get('ID', None)
        self.FileType = kwargs.get('FileType', None)
        self.MatchType = EnumLayer7ContentClassFileTypeMatchType.enum(kwargs.get('MatchType', None))
        self.Case = EnumLayer7ContentClassFileTypeCase.enum(kwargs.get('Case', None))
        self.Delete = EnumLayer7ContentClassFileTypeDelete.enum(kwargs.get('Delete', None))
        self.Copy = kwargs.get('Copy', None)

    def get_indexes(self):
        return self.ContentClassID, self.ID,
    
    @classmethod
    def get_index_names(cls):
        return 'ContentClassID', 'ID',

