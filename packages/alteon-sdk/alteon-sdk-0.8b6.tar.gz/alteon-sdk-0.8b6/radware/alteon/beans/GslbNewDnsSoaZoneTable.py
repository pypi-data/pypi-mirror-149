
from radware.sdk.beans_common import *


class EnumGslbDnsSoaZoneDelete(BaseBeanEnum):
    other = 1
    delete = 2


class GslbNewDnsSoaZoneTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Id = kwargs.get('Id', None)
        self.Name = kwargs.get('Name', None)
        self.NameServ = kwargs.get('NameServ', None)
        self.RespMail = kwargs.get('RespMail', None)
        self.Serial = kwargs.get('Serial', None)
        self.Delete = EnumGslbDnsSoaZoneDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.Id,
    
    @classmethod
    def get_index_names(cls):
        return 'Id',

