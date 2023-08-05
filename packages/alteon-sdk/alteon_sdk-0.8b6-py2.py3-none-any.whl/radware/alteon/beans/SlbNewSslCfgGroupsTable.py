
from radware.sdk.beans_common import *


class EnumSlbSslGroupsType(BaseBeanEnum):
    serverCertificate = 3
    trustedCertificate = 4
    intermediateCertificate = 5


class EnumSlbSslGroupsDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumSlbSslGroupsConfigType(BaseBeanEnum):
    regular = 1
    read_only = 2


class EnumSlbSslGroupsChainingMode(BaseBeanEnum):
    bySubjectIssuer = 0
    bySkidAkid = 1


class SlbNewSslCfgGroupsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ID = kwargs.get('ID', None)
        self.Name = kwargs.get('Name', None)
        self.Type = EnumSlbSslGroupsType.enum(kwargs.get('Type', None))
        self.Delete = EnumSlbSslGroupsDelete.enum(kwargs.get('Delete', None))
        self.DefaultCert = kwargs.get('DefaultCert', None)
        self.AddCert = kwargs.get('AddCert', None)
        self.RemCert = kwargs.get('RemCert', None)
        self.CertBmap = kwargs.get('CertBmap', None)
        self.ConfigType = EnumSlbSslGroupsConfigType.enum(kwargs.get('ConfigType', None))
        self.ChainingMode = EnumSlbSslGroupsChainingMode.enum(kwargs.get('ChainingMode', None))

    def get_indexes(self):
        return self.ID,
    
    @classmethod
    def get_index_names(cls):
        return 'ID',

