
from radware.sdk.beans_common import *


class EnumViewTreeFamilyType(BaseBeanEnum):
    Included = 1
    Excluded = 2


class VacmViewTreeFamilyTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ViewName = kwargs.get('ViewName', None)
        self.Subtree = kwargs.get('Subtree', None)
        self.Mask = kwargs.get('Mask', None)
        self.Type = EnumViewTreeFamilyType.enum(kwargs.get('Type', None))

    def get_indexes(self):
        return self.ViewName,  self.Subtree,
    
    @classmethod
    def get_index_names(cls):
        return  'ViewName', 'Subtree',

