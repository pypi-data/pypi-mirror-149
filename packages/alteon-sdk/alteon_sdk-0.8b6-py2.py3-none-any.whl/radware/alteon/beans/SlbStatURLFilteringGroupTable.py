
from radware.sdk.beans_common import *


class SlbStatURLFilteringGroupTable(DeviceBean):
    def __init__(self, **kwargs):
        self.SubCategoryIndex = kwargs.get('SubCategoryIndex', None)
        self.SubCategoryName = kwargs.get('SubCategoryName', None)
        self.CategoryName = kwargs.get('CategoryName', None)
        self.SubCategoryCount = kwargs.get('SubCategoryCount', None)

    def get_indexes(self):
        return self.SubCategoryIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'SubCategoryIndex',

