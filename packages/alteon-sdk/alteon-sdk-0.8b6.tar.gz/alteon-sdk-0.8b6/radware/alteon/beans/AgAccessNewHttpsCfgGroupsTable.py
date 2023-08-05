
from radware.sdk.beans_common import *


class EnumAgAccessHttpsGroupsType(BaseBeanEnum):
    intermediateCertificate = 5


class EnumAgAccessHttpsGroupsDelete(BaseBeanEnum):
    other = 1
    delete = 2


class AgAccessNewHttpsCfgGroupsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ID = kwargs.get('ID', None)
        self.Name = kwargs.get('Name', None)
        self.Type = EnumAgAccessHttpsGroupsType.enum(kwargs.get('Type', None))
        self.Delete = EnumAgAccessHttpsGroupsDelete.enum(kwargs.get('Delete', None))
        self.DefaultCert = kwargs.get('DefaultCert', None)
        self.AddCert = kwargs.get('AddCert', None)
        self.RemCert = kwargs.get('RemCert', None)
        self.CertBmap = kwargs.get('CertBmap', None)

    def get_indexes(self):
        return self.ID,
    
    @classmethod
    def get_index_names(cls):
        return 'ID',

