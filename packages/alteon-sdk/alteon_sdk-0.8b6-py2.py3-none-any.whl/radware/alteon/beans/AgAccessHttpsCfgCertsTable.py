
from radware.sdk.beans_common import *


class EnumAgAccessHttpsCertsKeySize(BaseBeanEnum):
    ks512 = 1
    ks1024 = 2
    ks2048 = 3
    ks4096 = 4
    unknown = 6


class EnumAgAccessHttpsCertsHashAlgo(BaseBeanEnum):
    md5 = 1
    sha1 = 2
    sha256 = 3
    sha384 = 4
    sha512 = 5
    unknown = 6


class EnumAgAccessHttpsCertsDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumAgAccessHttpsCertsGenerate(BaseBeanEnum):
    other = 1
    generate = 2


class EnumAgAccessHttpsCertsStatus(BaseBeanEnum):
    generated = 1
    notGenerated = 2


class AgAccessHttpsCfgCertsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ID = kwargs.get('ID', None)
        self.Name = kwargs.get('Name', None)
        self.KeySize = EnumAgAccessHttpsCertsKeySize.enum(kwargs.get('KeySize', None))
        self.Expiry = kwargs.get('Expiry', None)
        self.CommonName = kwargs.get('CommonName', None)
        self.HashAlgo = EnumAgAccessHttpsCertsHashAlgo.enum(kwargs.get('HashAlgo', None))
        self.CountryName = kwargs.get('CountryName', None)
        self.ProvinceName = kwargs.get('ProvinceName', None)
        self.LocalityName = kwargs.get('LocalityName', None)
        self.OrganizationName = kwargs.get('OrganizationName', None)
        self.OrganizationUnitName = kwargs.get('OrganizationUnitName', None)
        self.EMail = kwargs.get('EMail', None)
        self.ValidityPeriod = kwargs.get('ValidityPeriod', None)
        self.Delete = EnumAgAccessHttpsCertsDelete.enum(kwargs.get('Delete', None))
        self.Generate = EnumAgAccessHttpsCertsGenerate.enum(kwargs.get('Generate', None))
        self.Status = EnumAgAccessHttpsCertsStatus.enum(kwargs.get('Status', None))

    def get_indexes(self):
        return self.ID,
    
    @classmethod
    def get_index_names(cls):
        return 'ID',

