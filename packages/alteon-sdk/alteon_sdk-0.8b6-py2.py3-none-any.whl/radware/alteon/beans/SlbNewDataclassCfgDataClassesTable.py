
from radware.sdk.beans_common import *


class EnumSlbDataclassDataClassesDataType(BaseBeanEnum):
    string = 1
    ip = 2


class EnumSlbDataclassDataClassesDel(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewDataclassCfgDataClassesTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Id = kwargs.get('Id', None)
        self.DataType = EnumSlbDataclassDataClassesDataType.enum(kwargs.get('DataType', None))
        self.Name = kwargs.get('Name', None)
        self.Del = EnumSlbDataclassDataClassesDel.enum(kwargs.get('Del', None))
        self.Copy = kwargs.get('Copy', None)

    def get_indexes(self):
        return self.Id,
    
    @classmethod
    def get_index_names(cls):
        return 'Id',

