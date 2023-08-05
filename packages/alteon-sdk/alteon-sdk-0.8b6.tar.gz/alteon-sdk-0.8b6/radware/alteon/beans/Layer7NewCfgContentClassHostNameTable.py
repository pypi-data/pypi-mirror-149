
from radware.sdk.beans_common import *


class EnumLayer7ContentClassHostNameMatchType(BaseBeanEnum):
    sufx = 1
    prefx = 2
    equal = 3
    include = 4
    regex = 5


class EnumLayer7ContentClassHostNameDelete(BaseBeanEnum):
    other = 1
    delete = 2


class Layer7NewCfgContentClassHostNameTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ContentClassID = kwargs.get('ContentClassID', None)
        self.ID = kwargs.get('ID', None)
        self.HostName = kwargs.get('HostName', None)
        self.MatchType = EnumLayer7ContentClassHostNameMatchType.enum(kwargs.get('MatchType', None))
        self.Delete = EnumLayer7ContentClassHostNameDelete.enum(kwargs.get('Delete', None))
        self.DataclassID = kwargs.get('DataclassID', None)
        self.Copy = kwargs.get('Copy', None)

    def get_indexes(self):
        return self.ContentClassID, self.ID,
    
    @classmethod
    def get_index_names(cls):
        return 'ContentClassID', 'ID',

