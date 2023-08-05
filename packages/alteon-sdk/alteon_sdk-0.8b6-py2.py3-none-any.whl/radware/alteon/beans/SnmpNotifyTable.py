
from radware.sdk.beans_common import *

class EnumSnmpNotifyType(BaseBeanEnum):
    trap = 1
    inform = 2

class EnumSnmpStorageType(BaseBeanEnum):
    other = 1
    volatile = 2
    nonVolatile = 3
    permanent = 4
    readOnly = 5

class EnumSnmpRowStatus(BaseBeanEnum):
    active = 1
    notInService = 2
    notReady = 3
    createAndGo = 4
    createAndWait = 5
    destroy = 6

class SnmpNotifyTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Name = kwargs.get('Name', None)
        self.Tag = kwargs.get('Tag', None)
        self.Type = EnumSnmpNotifyType.enum(kwargs.get('Type', None))
        self.StorageType = EnumSnmpStorageType.enum(kwargs.get('StorageType', None))
        self.RowStatus = EnumSnmpRowStatus.enum(kwargs.get('RowStatus', None))

    def get_indexes(self):
        return self.Name,
    
    @classmethod
    def get_index_names(cls):
        return  'Name',

