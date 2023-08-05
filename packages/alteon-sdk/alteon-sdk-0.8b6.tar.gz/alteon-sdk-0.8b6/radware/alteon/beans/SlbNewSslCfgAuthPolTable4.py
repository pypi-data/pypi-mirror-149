
from radware.sdk.beans_common import *


class EnumSlbSslAuthPolTable4PassinfoKeytypeFlag(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslAuthPolTable4PassinfoMd5Flag(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslAuthPolTable4PassinfoCertFlag(BaseBeanEnum):
    enabled = 1
    disabled = 2


class SlbNewSslCfgAuthPolTable4(DeviceBean):
    def __init__(self, **kwargs):
        self.NameIdIndex = kwargs.get('NameIdIndex', None)
        self.PassinfoKeytypeName = kwargs.get('PassinfoKeytypeName', None)
        self.PassinfoKeytypeFlag = EnumSlbSslAuthPolTable4PassinfoKeytypeFlag.enum(kwargs.get('PassinfoKeytypeFlag', None))
        self.PassinfoMd5Name = kwargs.get('PassinfoMd5Name', None)
        self.PassinfoMd5Flag = EnumSlbSslAuthPolTable4PassinfoMd5Flag.enum(kwargs.get('PassinfoMd5Flag', None))
        self.PassinfoCertName = kwargs.get('PassinfoCertName', None)
        self.PassinfoCertFormat = kwargs.get('PassinfoCertFormat', None)
        self.PassinfoCertFlag = EnumSlbSslAuthPolTable4PassinfoCertFlag.enum(kwargs.get('PassinfoCertFlag', None))
        self.PassinfoCharset = kwargs.get('PassinfoCharset', None)
        self.TrustcaChainName = kwargs.get('TrustcaChainName', None)
        self.TrustcaChainType = kwargs.get('TrustcaChainType', None)
        self.ClientcaReqChainName = kwargs.get('ClientcaReqChainName', None)
        self.ClientcaReqChainType = kwargs.get('ClientcaReqChainType', None)

    def get_indexes(self):
        return self.NameIdIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'NameIdIndex',

