
from radware.sdk.beans_common import *


class EnumGslbDnsSecKeyType(BaseBeanEnum):
    keyTypeKSK = 1
    keyTypeZSK = 2
    keyTypeInvalid = 3


class EnumGslbDnsSecKeyStatus(BaseBeanEnum):
    enable = 1
    disable = 2


class EnumGslbDnsSecKeySize(BaseBeanEnum):
    keySize1024 = 1
    keySize2048 = 2
    keySize4096 = 3
    keySizeInvalid = 4


class EnumGslbDnsSecKeyAlgo(BaseBeanEnum):
    keyAlgoRsaSha1 = 1
    keyAlgoRsaSha256 = 2
    keyAlgoRsaSha512 = 3


class EnumGslbDnsSecKeyDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumGslbDnsSecKeyGenerate(BaseBeanEnum):
    other = 1
    generate = 2


class EnumGslbDnsSecKeyGenerateStatus(BaseBeanEnum):
    notGenerated = 1
    generated = 2
    inProgress = 3


class GslbNewDnsSecKeyTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ID = kwargs.get('ID', None)
        self.UseCount = kwargs.get('UseCount', None)
        self.Type = EnumGslbDnsSecKeyType.enum(kwargs.get('Type', None))
        self.Status = EnumGslbDnsSecKeyStatus.enum(kwargs.get('Status', None))
        self.Size = EnumGslbDnsSecKeySize.enum(kwargs.get('Size', None))
        self.Algo = EnumGslbDnsSecKeyAlgo.enum(kwargs.get('Algo', None))
        self.TTL = kwargs.get('TTL', None)
        self.ExpPeriod = kwargs.get('ExpPeriod', None)
        self.RollOverPeriod = kwargs.get('RollOverPeriod', None)
        self.ValidityPeriod = kwargs.get('ValidityPeriod', None)
        self.PublicationPeriod = kwargs.get('PublicationPeriod', None)
        self.Delete = EnumGslbDnsSecKeyDelete.enum(kwargs.get('Delete', None))
        self.Generate = EnumGslbDnsSecKeyGenerate.enum(kwargs.get('Generate', None))
        self.GenerateStatus = EnumGslbDnsSecKeyGenerateStatus.enum(kwargs.get('GenerateStatus', None))

    def get_indexes(self):
        return self.ID,
    
    @classmethod
    def get_index_names(cls):
        return 'ID',

