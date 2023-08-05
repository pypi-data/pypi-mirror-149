
from radware.sdk.beans_common import *


class EnumGslbDnsCaaRecordType(BaseBeanEnum):
    issue = 0
    issuewild = 1
    iodef = 2


class EnumGslbDnsCaaRecordDelete(BaseBeanEnum):
    other = 1
    delete = 2


class GslbNewDnsCaaRecordTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Id = kwargs.get('Id', None)
        self.DomainName = kwargs.get('DomainName', None)
        self.Type = EnumGslbDnsCaaRecordType.enum(kwargs.get('Type', None))
        self.Value = kwargs.get('Value', None)
        self.Ttl = kwargs.get('Ttl', None)
        self.Delete = EnumGslbDnsCaaRecordDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.Id,
    
    @classmethod
    def get_index_names(cls):
        return 'Id',

