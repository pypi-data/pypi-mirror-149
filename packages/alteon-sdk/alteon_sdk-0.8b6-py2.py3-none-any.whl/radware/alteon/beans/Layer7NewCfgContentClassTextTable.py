
from radware.sdk.beans_common import *


class EnumLayer7ContentClassTextMatchType(BaseBeanEnum):
    include = 4
    regex = 5


class EnumLayer7ContentClassTextLookupArea(BaseBeanEnum):
    header = 1
    body = 2
    both = 3


class EnumLayer7ContentClassTextCase(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumLayer7ContentClassTextDelete(BaseBeanEnum):
    other = 1
    delete = 2


class Layer7NewCfgContentClassTextTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ContentClassID = kwargs.get('ContentClassID', None)
        self.ID = kwargs.get('ID', None)
        self.Text = kwargs.get('Text', None)
        self.MatchType = EnumLayer7ContentClassTextMatchType.enum(kwargs.get('MatchType', None))
        self.LookupArea = EnumLayer7ContentClassTextLookupArea.enum(kwargs.get('LookupArea', None))
        self.Case = EnumLayer7ContentClassTextCase.enum(kwargs.get('Case', None))
        self.Delete = EnumLayer7ContentClassTextDelete.enum(kwargs.get('Delete', None))
        self.Copy = kwargs.get('Copy', None)

    def get_indexes(self):
        return self.ContentClassID, self.ID,
    
    @classmethod
    def get_index_names(cls):
        return 'ContentClassID', 'ID',

