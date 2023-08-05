
from radware.sdk.beans_common import *


class EnumSlbDrecordEntryState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbDrecordEntryDelete(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewCfgDrecordVirtRealMappingTable(DeviceBean):
    def __init__(self, **kwargs):
        self.DomainRecordIndex = kwargs.get('DomainRecordIndex', None)
        self.EntryIndex = kwargs.get('EntryIndex', None)
        self.Server = kwargs.get('Server', None)
        self.RealServer = kwargs.get('RealServer', None)
        self.EntryState = EnumSlbDrecordEntryState.enum(kwargs.get('EntryState', None))
        self.EntryDelete = EnumSlbDrecordEntryDelete.enum(kwargs.get('EntryDelete', None))
        self.EnhVirtServer = kwargs.get('EnhVirtServer', None)
        self.EnhRealServer = kwargs.get('EnhRealServer', None)

    def get_indexes(self):
        return self.DomainRecordIndex, self.EntryIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'DomainRecordIndex', 'EntryIndex',

