
from radware.sdk.beans_common import *


class EnumSlbSslSSLPolPassInfoCipherFlag(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslSSLPolPassInfoVersionFlag(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslSSLPolPassInfoHeadBitsFlag(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslSSLPolPassInfoFrontend(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslSSLPolCipherName(BaseBeanEnum):
    rsa = 0
    all = 1
    all_non_null_ciphers = 2
    sslv3 = 3
    tlsv1 = 4
    tlsv1_2 = 5
    export = 6
    low = 7
    medium = 8
    high = 9
    rsa_rc4_128_md5 = 10
    rsa_rc4_128_sha1 = 11
    rsa_des_sha1 = 12
    rsa_3des_sha1 = 13
    rsa_aes_128_sha1 = 14
    rsa_aes_256_sha1 = 15
    pci_dss_compliance = 16
    user_defined = 17
    user_defined_expert = 18
    main = 19
    http2 = 20


class EnumSlbSslSSLPolBecipher(BaseBeanEnum):
    low = 0
    medium = 1
    high = 2
    user_defined = 3
    user_defined_expert = 4
    main = 5


class EnumSlbSslSSLPolBessl(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslSSLPolConvert(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslSSLPolAdminStatus(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslSSLPolDel(BaseBeanEnum):
    other = 1
    delete = 2


class EnumSlbSslSSLPolPassInfoComply(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslSSLPolFessl(BaseBeanEnum):
    enabled = 1
    disabled = 2
    connect = 3


class EnumSlbSslSSLPolFESslv3Version(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslSSLPolFETls10Version(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslSSLPolFETls11Version(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslSSLPolBESslv3Version(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslSSLPolBETls10Version(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslSSLPolBETls11Version(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslSSLPolFETls12Version(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslSSLPolBETls12Version(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslSSLPolDHkey(BaseBeanEnum):
    keySize1024 = 1
    keySize2048 = 2


class EnumSlbSslSSLPolHwoffldFeRsa(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslSSLPolHwoffldFeDh(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslSSLPolHwoffldFeEc(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslSSLPolHwoffldFeBulk(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslSSLPolHwoffldFePkey(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslSSLPolHwoffldFeFeatures(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslSSLPolHwoffldBeRsa(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslSSLPolHwoffldBeDh(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslSSLPolHwoffldBeEc(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslSSLPolHwoffldBeBulk(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslSSLPolHwoffldBePkey(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslSSLPolHwoffldBeFeatures(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslSSLPolBesni(BaseBeanEnum):
    enabled = 1
    disabled = 2


class SlbNewSslCfgSSLPolTable(DeviceBean):
    def __init__(self, **kwargs):
        self.NameIdIndex = kwargs.get('NameIdIndex', None)
        self.Name = kwargs.get('Name', None)
        self.PassInfoCipherName = kwargs.get('PassInfoCipherName', None)
        self.PassInfoCipherFlag = EnumSlbSslSSLPolPassInfoCipherFlag.enum(kwargs.get('PassInfoCipherFlag', None))
        self.PassInfoVersionName = kwargs.get('PassInfoVersionName', None)
        self.PassInfoVersionFlag = EnumSlbSslSSLPolPassInfoVersionFlag.enum(kwargs.get('PassInfoVersionFlag', None))
        self.PassInfoHeadBitsName = kwargs.get('PassInfoHeadBitsName', None)
        self.PassInfoHeadBitsFlag = EnumSlbSslSSLPolPassInfoHeadBitsFlag.enum(kwargs.get('PassInfoHeadBitsFlag', None))
        self.PassInfoFrontend = EnumSlbSslSSLPolPassInfoFrontend.enum(kwargs.get('PassInfoFrontend', None))
        self.CipherName = EnumSlbSslSSLPolCipherName.enum(kwargs.get('CipherName', None))
        self.CipherUserdef = kwargs.get('CipherUserdef', None)
        self.IntermcaChainName = kwargs.get('IntermcaChainName', None)
        self.IntermcaChainType = kwargs.get('IntermcaChainType', None)
        self.Becipher = EnumSlbSslSSLPolBecipher.enum(kwargs.get('Becipher', None))
        self.Authpol = kwargs.get('Authpol', None)
        self.Convuri = kwargs.get('Convuri', None)
        self.Bessl = EnumSlbSslSSLPolBessl.enum(kwargs.get('Bessl', None))
        self.Convert = EnumSlbSslSSLPolConvert.enum(kwargs.get('Convert', None))
        self.AdminStatus = EnumSlbSslSSLPolAdminStatus.enum(kwargs.get('AdminStatus', None))
        self.Del = EnumSlbSslSSLPolDel.enum(kwargs.get('Del', None))
        self.PassInfoComply = EnumSlbSslSSLPolPassInfoComply.enum(kwargs.get('PassInfoComply', None))
        self.Fessl = EnumSlbSslSSLPolFessl.enum(kwargs.get('Fessl', None))
        self.FESslv3Version = EnumSlbSslSSLPolFESslv3Version.enum(kwargs.get('FESslv3Version', None))
        self.FETls10Version = EnumSlbSslSSLPolFETls10Version.enum(kwargs.get('FETls10Version', None))
        self.FETls11Version = EnumSlbSslSSLPolFETls11Version.enum(kwargs.get('FETls11Version', None))
        self.BESslv3Version = EnumSlbSslSSLPolBESslv3Version.enum(kwargs.get('BESslv3Version', None))
        self.BETls10Version = EnumSlbSslSSLPolBETls10Version.enum(kwargs.get('BETls10Version', None))
        self.BETls11Version = EnumSlbSslSSLPolBETls11Version.enum(kwargs.get('BETls11Version', None))
        self.FETls12Version = EnumSlbSslSSLPolFETls12Version.enum(kwargs.get('FETls12Version', None))
        self.BETls12Version = EnumSlbSslSSLPolBETls12Version.enum(kwargs.get('BETls12Version', None))
        self.CipherExpertUserdef = kwargs.get('CipherExpertUserdef', None)
        self.BeCipherUserdef = kwargs.get('BeCipherUserdef', None)
        self.BeCipherExpertUserdef = kwargs.get('BeCipherExpertUserdef', None)
        self.BEClientCertName = kwargs.get('BEClientCertName', None)
        self.BETrustedCAcertName = kwargs.get('BETrustedCAcertName', None)
        self.BETrustedCAcertType = kwargs.get('BETrustedCAcertType', None)
        self.Secreneg = kwargs.get('Secreneg', None)
        self.DHkey = EnumSlbSslSSLPolDHkey.enum(kwargs.get('DHkey', None))
        self.BEAuthpol = kwargs.get('BEAuthpol', None)
        self.HwoffldFeRsa = EnumSlbSslSSLPolHwoffldFeRsa.enum(kwargs.get('HwoffldFeRsa', None))
        self.HwoffldFeDh = EnumSlbSslSSLPolHwoffldFeDh.enum(kwargs.get('HwoffldFeDh', None))
        self.HwoffldFeEc = EnumSlbSslSSLPolHwoffldFeEc.enum(kwargs.get('HwoffldFeEc', None))
        self.HwoffldFeBulk = EnumSlbSslSSLPolHwoffldFeBulk.enum(kwargs.get('HwoffldFeBulk', None))
        self.HwoffldFePkey = EnumSlbSslSSLPolHwoffldFePkey.enum(kwargs.get('HwoffldFePkey', None))
        self.HwoffldFeFeatures = EnumSlbSslSSLPolHwoffldFeFeatures.enum(kwargs.get('HwoffldFeFeatures', None))
        self.HwoffldBeRsa = EnumSlbSslSSLPolHwoffldBeRsa.enum(kwargs.get('HwoffldBeRsa', None))
        self.HwoffldBeDh = EnumSlbSslSSLPolHwoffldBeDh.enum(kwargs.get('HwoffldBeDh', None))
        self.HwoffldBeEc = EnumSlbSslSSLPolHwoffldBeEc.enum(kwargs.get('HwoffldBeEc', None))
        self.HwoffldBeBulk = EnumSlbSslSSLPolHwoffldBeBulk.enum(kwargs.get('HwoffldBeBulk', None))
        self.HwoffldBePkey = EnumSlbSslSSLPolHwoffldBePkey.enum(kwargs.get('HwoffldBePkey', None))
        self.HwoffldBeFeatures = EnumSlbSslSSLPolHwoffldBeFeatures.enum(kwargs.get('HwoffldBeFeatures', None))
        self.Besni = EnumSlbSslSSLPolBesni.enum(kwargs.get('Besni', None))

    def get_indexes(self):
        return self.NameIdIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'NameIdIndex',

