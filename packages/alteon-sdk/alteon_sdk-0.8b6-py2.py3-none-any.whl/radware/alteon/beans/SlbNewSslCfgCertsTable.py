
from radware.sdk.beans_common import *


class EnumSlbSslCertsType(BaseBeanEnum):
    key = 1
    certificateRequest = 2
    serverCertificate = 3
    trustedCertificate = 4
    intermediateCertificate = 5
    crl = 6


class EnumSlbSslCertsKeySize(BaseBeanEnum):
    ks512 = 1
    ks1024 = 2
    ks2048 = 3
    ks4096 = 4
    unknown = 6


class EnumSlbSslCertsHashAlgo(BaseBeanEnum):
    md5 = 1
    sha1 = 2
    sha256 = 3
    sha384 = 4
    sha512 = 5
    unknown = 6


class EnumSlbSslCertsDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumSlbSslCertsGenerate(BaseBeanEnum):
    other = 1
    generate = 2
    idle = 3
    inprogress = 4
    generated = 5
    notGenerated = 6


class EnumSlbSslCertsStatus(BaseBeanEnum):
    generated = 1
    notGenerated = 2
    inProgress = 3


class EnumSlbSslCertsKeyType(BaseBeanEnum):
    rsa = 1
    ec = 2
    unknown = 6


class EnumSlbSslCertsKeySizeEc(BaseBeanEnum):
    ks0 = 0
    ks192 = 1
    ks224 = 2
    ks256 = 3
    ks384 = 4
    ks521 = 5
    unknown = 6


class EnumSlbSslCurveNameEc(BaseBeanEnum):
    secp112r1 = 1
    secp112r2 = 2
    secp128r1 = 3
    secp128r2 = 4
    secp160k1 = 5
    secp160r1 = 6
    secp160r2 = 7
    secp192k1 = 8
    secp224k1 = 9
    secp224r1 = 10
    secp256k1 = 11
    secp384r1 = 12
    secp521r1 = 13
    prime192v1 = 14
    prime192v2 = 15
    prime192v3 = 16
    prime239v1 = 17
    prime239v2 = 18
    prime239v3 = 19
    prime256v1 = 20
    sect113r1 = 21
    sect113r2 = 22
    sect131r1 = 23
    sect131r2 = 24
    sect163k1 = 25
    sect163r1 = 26
    sect163r2 = 27
    sect193r1 = 28
    sect193r2 = 29
    sect233k1 = 30
    sect233r1 = 31
    sect239k1 = 32
    sect283k1 = 33
    sect283r1 = 34
    sect409k1 = 35
    sect409r1 = 36
    sect571k1 = 37
    sect571r1 = 38
    c2pnb163v1 = 39
    c2pnb163v2 = 40
    c2pnb163v3 = 41
    c2pnb176v1 = 42
    c2tnb191v1 = 43
    c2tnb191v2 = 44
    c2tnb191v3 = 45
    c2pnb208w1 = 46
    c2tnb239v1 = 47
    c2tnb239v2 = 48
    c2tnb239v3 = 49
    c2pnb272w1 = 50
    c2pnb304w1 = 51
    c2tnb359v1 = 52
    c2pnb368w1 = 53
    c2tnb431r1 = 54
    wtls1 = 55
    wtls3 = 56
    wtls4 = 57
    wtls5 = 58
    wtls6 = 59
    wtls7 = 60
    wtls8 = 61
    wtls9 = 62
    wtls10 = 63
    wtls11 = 64
    wtls12 = 65
    unknown = 0


class SlbNewSslCfgCertsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ID = kwargs.get('ID', None)
        self.Type = EnumSlbSslCertsType.enum(kwargs.get('Type', None))
        self.Name = kwargs.get('Name', None)
        self.KeySize = EnumSlbSslCertsKeySize.enum(kwargs.get('KeySize', None))
        self.Expirty = kwargs.get('Expirty', None)
        self.CommonName = kwargs.get('CommonName', None)
        self.HashAlgo = EnumSlbSslCertsHashAlgo.enum(kwargs.get('HashAlgo', None))
        self.CountryName = kwargs.get('CountryName', None)
        self.PrpvinceName = kwargs.get('PrpvinceName', None)
        self.LocalityName = kwargs.get('LocalityName', None)
        self.OrganizationName = kwargs.get('OrganizationName', None)
        self.OrganizationUnitName = kwargs.get('OrganizationUnitName', None)
        self.EMail = kwargs.get('EMail', None)
        self.ValidityPeriod = kwargs.get('ValidityPeriod', None)
        self.Delete = EnumSlbSslCertsDelete.enum(kwargs.get('Delete', None))
        self.Generate = EnumSlbSslCertsGenerate.enum(kwargs.get('Generate', None))
        self.Status = EnumSlbSslCertsStatus.enum(kwargs.get('Status', None))
        self.KeyType = EnumSlbSslCertsKeyType.enum(kwargs.get('KeyType', None))
        self.KeySizeEc = EnumSlbSslCertsKeySizeEc.enum(kwargs.get('KeySizeEc', None))
        self.CurveNameEc = EnumSlbSslCurveNameEc.enum(kwargs.get('CurveNameEc', None))
        self.KeySizeCommon = kwargs.get('KeySizeCommon', None)
        self.IntermcaChainName = kwargs.get('IntermcaChainName', None)
        self.IntermcaChainType = kwargs.get('IntermcaChainType', None)
        self.Serial = kwargs.get('Serial', None)
        self.SubjectAltName = kwargs.get('SubjectAltName', None)

    def get_indexes(self):
        return self.ID, self.Type,
    
    @classmethod
    def get_index_names(cls):
        return 'ID', 'Type',

