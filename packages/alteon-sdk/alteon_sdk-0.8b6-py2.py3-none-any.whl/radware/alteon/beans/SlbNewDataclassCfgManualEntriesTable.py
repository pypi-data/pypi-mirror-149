
from radware.sdk.beans_common import *


class EnumSlbDataclassManualEntriesEntryDel(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewDataclassCfgManualEntriesTable(DeviceBean):
    def __init__(self, **kwargs):
        self.DcId = kwargs.get('DcId', None)
        self.Id = kwargs.get('Id', None)
        self.Key = kwargs.get('Key', None)
        self.Value = kwargs.get('Value', None)
        self.Del = EnumSlbDataclassManualEntriesEntryDel.enum(kwargs.get('Del', None))

    def get_indexes(self):
        return self.DcId, self.Id,
    
    @classmethod
    def get_index_names(cls):
        return 'DcId', 'Id',

