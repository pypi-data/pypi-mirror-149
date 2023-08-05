
from radware.sdk.beans_common import *


class EnumSlbSslAuthPolValidityUriprior(BaseBeanEnum):
    clientcert = 1
    staticuri = 2


class EnumSlbSslAuthPolValidityVchain(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslAuthPolValiditySecure(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslAuthPolPassinfoVersionFlag(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslAuthPolPassinfoSerialFlag(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslAuthPolPassinfoAlgoFlag(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslAuthPolPassinfoIssuerFlag(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslAuthPolPassinfoNbeforeFlag(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslAuthPolPassinfoNafterFlag(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslAuthPolPassinfoSubjectFlag(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslAuthPolPassinfoKeytypeFlag(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslAuthPolPassinfoMd5Flag(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslAuthPolPassinfoCertFlag(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslAuthPolAdminStatus(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslAuthPolDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumSlbSslAuthPolPassinfoComp2424(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslAuthPolValidityCdpPreference(BaseBeanEnum):
    embedded = 1
    userdefined = 2


class EnumSlbSslAuthPolType(BaseBeanEnum):
    frontend = 1
    backend = 2


class EnumSlbSslAuthPolSerCertExp(BaseBeanEnum):
    ignore = 1
    reject = 2


class EnumSlbSslAuthPolSerCertMis(BaseBeanEnum):
    ignore = 1
    reject = 2


class EnumSlbSslAuthPolSerCertUntrust(BaseBeanEnum):
    ignore = 1
    reject = 2


class EnumSlbSslAuthPolIssuerNamesOrder(BaseBeanEnum):
    regular = 0
    reverse = 1


class EnumSlbSslAuthPolSubjectNamesOrder(BaseBeanEnum):
    regular = 0
    reverse = 1


class SlbNewSslCfgAuthPolTable(DeviceBean):
    def __init__(self, **kwargs):
        self.NameIdIndex = kwargs.get('NameIdIndex', None)
        self.Name = kwargs.get('Name', None)
        self.ValidityMethod = kwargs.get('ValidityMethod', None)
        self.ValidityStaturi = kwargs.get('ValidityStaturi', None)
        self.ValidityUriprior = EnumSlbSslAuthPolValidityUriprior.enum(kwargs.get('ValidityUriprior', None))
        self.ValidityCachtime = kwargs.get('ValidityCachtime', None)
        self.ValidityTimedev = kwargs.get('ValidityTimedev', None)
        self.ValidityAlgorthmName = kwargs.get('ValidityAlgorthmName', None)
        self.ValidityVchain = EnumSlbSslAuthPolValidityVchain.enum(kwargs.get('ValidityVchain', None))
        self.ValiditySecure = EnumSlbSslAuthPolValiditySecure.enum(kwargs.get('ValiditySecure', None))
        self.PassinfoVersionName = kwargs.get('PassinfoVersionName', None)
        self.PassinfoVersionFlag = EnumSlbSslAuthPolPassinfoVersionFlag.enum(kwargs.get('PassinfoVersionFlag', None))
        self.PassinfoSerialName = kwargs.get('PassinfoSerialName', None)
        self.PassinfoSerialFlag = EnumSlbSslAuthPolPassinfoSerialFlag.enum(kwargs.get('PassinfoSerialFlag', None))
        self.PassinfoAlgoName = kwargs.get('PassinfoAlgoName', None)
        self.PassinfoAlgoFlag = EnumSlbSslAuthPolPassinfoAlgoFlag.enum(kwargs.get('PassinfoAlgoFlag', None))
        self.PassinfoIssuerName = kwargs.get('PassinfoIssuerName', None)
        self.PassinfoIssuerFlag = EnumSlbSslAuthPolPassinfoIssuerFlag.enum(kwargs.get('PassinfoIssuerFlag', None))
        self.PassinfoNbeforeName = kwargs.get('PassinfoNbeforeName', None)
        self.PassinfoNbeforeFlag = EnumSlbSslAuthPolPassinfoNbeforeFlag.enum(kwargs.get('PassinfoNbeforeFlag', None))
        self.PassinfoNafterName = kwargs.get('PassinfoNafterName', None)
        self.PassinfoNafterFlag = EnumSlbSslAuthPolPassinfoNafterFlag.enum(kwargs.get('PassinfoNafterFlag', None))
        self.PassinfoSubjectName = kwargs.get('PassinfoSubjectName', None)
        self.PassinfoSubjectFlag = EnumSlbSslAuthPolPassinfoSubjectFlag.enum(kwargs.get('PassinfoSubjectFlag', None))
        self.PassinfoKeytypeName = kwargs.get('PassinfoKeytypeName', None)
        self.PassinfoKeytypeFlag = EnumSlbSslAuthPolPassinfoKeytypeFlag.enum(kwargs.get('PassinfoKeytypeFlag', None))
        self.PassinfoMd5Name = kwargs.get('PassinfoMd5Name', None)
        self.PassinfoMd5Flag = EnumSlbSslAuthPolPassinfoMd5Flag.enum(kwargs.get('PassinfoMd5Flag', None))
        self.PassinfoCertName = kwargs.get('PassinfoCertName', None)
        self.PassinfoCertFormat = kwargs.get('PassinfoCertFormat', None)
        self.PassinfoCertFlag = EnumSlbSslAuthPolPassinfoCertFlag.enum(kwargs.get('PassinfoCertFlag', None))
        self.PassinfoCharset = kwargs.get('PassinfoCharset', None)
        self.TrustcaChainName = kwargs.get('TrustcaChainName', None)
        self.TrustcaChainType = kwargs.get('TrustcaChainType', None)
        self.Cadepth = kwargs.get('Cadepth', None)
        self.Caverify = kwargs.get('Caverify', None)
        self.Failurl = kwargs.get('Failurl', None)
        self.AdminStatus = EnumSlbSslAuthPolAdminStatus.enum(kwargs.get('AdminStatus', None))
        self.Delete = EnumSlbSslAuthPolDelete.enum(kwargs.get('Delete', None))
        self.PassinfoComp2424 = EnumSlbSslAuthPolPassinfoComp2424.enum(kwargs.get('PassinfoComp2424', None))
        self.ValidityCrlFile = kwargs.get('ValidityCrlFile', None)
        self.ValidityCdpGroup = kwargs.get('ValidityCdpGroup', None)
        self.ValidityCdpGracetime = kwargs.get('ValidityCdpGracetime', None)
        self.ValidityCdpInterval = kwargs.get('ValidityCdpInterval', None)
        self.ValidityCdpPreference = EnumSlbSslAuthPolValidityCdpPreference.enum(kwargs.get('ValidityCdpPreference', None))
        self.ClientcaReqChainName = kwargs.get('ClientcaReqChainName', None)
        self.ClientcaReqChainType = kwargs.get('ClientcaReqChainType', None)
        self.Type = EnumSlbSslAuthPolType.enum(kwargs.get('Type', None))
        self.SerCertExp = EnumSlbSslAuthPolSerCertExp.enum(kwargs.get('SerCertExp', None))
        self.SerCertMis = EnumSlbSslAuthPolSerCertMis.enum(kwargs.get('SerCertMis', None))
        self.SerCertUntrust = EnumSlbSslAuthPolSerCertUntrust.enum(kwargs.get('SerCertUntrust', None))
        self.IssuerNamesOrder = EnumSlbSslAuthPolIssuerNamesOrder.enum(kwargs.get('IssuerNamesOrder', None))
        self.SubjectNamesOrder = EnumSlbSslAuthPolSubjectNamesOrder.enum(kwargs.get('SubjectNamesOrder', None))

    def get_indexes(self):
        return self.NameIdIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'NameIdIndex',

