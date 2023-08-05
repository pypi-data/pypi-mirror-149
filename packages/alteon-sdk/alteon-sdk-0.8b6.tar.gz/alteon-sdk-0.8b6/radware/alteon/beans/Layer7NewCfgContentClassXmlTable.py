
from radware.sdk.beans_common import *


class EnumLayer7ContentClassXmlTagMatchTypeName(BaseBeanEnum):
    sufx = 1
    equal = 3


class EnumLayer7ContentClassXmlTagMatchTypeVal(BaseBeanEnum):
    sufx = 1
    equal = 3
    include = 4


class EnumLayer7ContentClassXmlTagCase(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumLayer7ContentClassXmlTagDelete(BaseBeanEnum):
    other = 1
    delete = 2


class Layer7NewCfgContentClassXmlTable(DeviceBean):
    def __init__(self, **kwargs):
        self.TagContentClassID = kwargs.get('TagContentClassID', None)
        self.TagID = kwargs.get('TagID', None)
        self.TagName = kwargs.get('TagName', None)
        self.TagVal = kwargs.get('TagVal', None)
        self.TagMatchTypeName = EnumLayer7ContentClassXmlTagMatchTypeName.enum(kwargs.get('TagMatchTypeName', None))
        self.TagMatchTypeVal = EnumLayer7ContentClassXmlTagMatchTypeVal.enum(kwargs.get('TagMatchTypeVal', None))
        self.TagCase = EnumLayer7ContentClassXmlTagCase.enum(kwargs.get('TagCase', None))
        self.TagDelete = EnumLayer7ContentClassXmlTagDelete.enum(kwargs.get('TagDelete', None))
        self.TagCopy = kwargs.get('TagCopy', None)

    def get_indexes(self):
        return self.TagContentClassID, self.TagID,
    
    @classmethod
    def get_index_names(cls):
        return 'TagContentClassID', 'TagID',

