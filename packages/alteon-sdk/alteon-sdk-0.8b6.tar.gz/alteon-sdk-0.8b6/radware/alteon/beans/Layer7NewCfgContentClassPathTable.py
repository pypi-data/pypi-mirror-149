
from radware.sdk.beans_common import *


class EnumLayer7ContentClassPathMatchType(BaseBeanEnum):
    sufx = 1
    prefx = 2
    equal = 3
    include = 4
    regex = 5


class EnumLayer7ContentClassPathCase(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumLayer7ContentClassPathDelete(BaseBeanEnum):
    other = 1
    delete = 2


class Layer7NewCfgContentClassPathTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ContentClassID = kwargs.get('ContentClassID', None)
        self.ID = kwargs.get('ID', None)
        self.FilePath = kwargs.get('FilePath', None)
        self.MatchType = EnumLayer7ContentClassPathMatchType.enum(kwargs.get('MatchType', None))
        self.Case = EnumLayer7ContentClassPathCase.enum(kwargs.get('Case', None))
        self.Delete = EnumLayer7ContentClassPathDelete.enum(kwargs.get('Delete', None))
        self.DataclassID = kwargs.get('DataclassID', None)
        self.Copy = kwargs.get('Copy', None)

    def get_indexes(self):
        return self.ContentClassID, self.ID,
    
    @classmethod
    def get_index_names(cls):
        return 'ContentClassID', 'ID',

