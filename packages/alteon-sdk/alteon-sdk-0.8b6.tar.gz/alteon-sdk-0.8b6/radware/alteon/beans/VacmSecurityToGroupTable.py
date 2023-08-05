
from radware.sdk.beans_common import *


class EnumSecurityModel(BaseBeanEnum):
    SNMPV1 = 1
    SNMPV2 = 2
    USM = 3


class VacmSecurityToGroupTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Model = EnumSecurityModel.enum(kwargs.get('Model', None))
        self.Name = kwargs.get('Name', None)
        self.GroupName = kwargs.get('GroupName', None)
        self.StorageType = kwargs.get('StorageType', None)
        self.Status = kwargs.get('Status', None)   #RowStatus


    def get_indexes(self):
        return self.Model, self.Name,

    @classmethod
    def get_index_names(cls):
        return 'Model', 'Name',

