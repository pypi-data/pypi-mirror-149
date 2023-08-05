
from radware.sdk.beans_common import *


class EnumSlbDomainRecordState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbDrecordDelete(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewCfgDrecordTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.DomainRecordState = EnumSlbDomainRecordState.enum(kwargs.get('DomainRecordState', None))
        self.DomainRecordName = kwargs.get('DomainRecordName', None)
        self.Delete = EnumSlbDrecordDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

