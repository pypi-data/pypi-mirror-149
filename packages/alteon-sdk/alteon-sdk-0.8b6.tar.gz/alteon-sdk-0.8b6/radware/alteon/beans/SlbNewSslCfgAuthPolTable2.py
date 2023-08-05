
from radware.sdk.beans_common import *


class EnumSlbSslAuthPolTable2PassinfoSerialFlag(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslAuthPolTable2PassinfoAlgoFlag(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslAuthPolTable2PassinfoIssuerFlag(BaseBeanEnum):
    enabled = 1
    disabled = 2


class SlbNewSslCfgAuthPolTable2(DeviceBean):
    def __init__(self, **kwargs):
        self.NameIdIndex = kwargs.get('NameIdIndex', None)
        self.PassinfoSerialName = kwargs.get('PassinfoSerialName', None)
        self.PassinfoSerialFlag = EnumSlbSslAuthPolTable2PassinfoSerialFlag.enum(kwargs.get('PassinfoSerialFlag', None))
        self.PassinfoAlgoName = kwargs.get('PassinfoAlgoName', None)
        self.PassinfoAlgoFlag = EnumSlbSslAuthPolTable2PassinfoAlgoFlag.enum(kwargs.get('PassinfoAlgoFlag', None))
        self.PassinfoIssuerName = kwargs.get('PassinfoIssuerName', None)
        self.PassinfoIssuerFlag = EnumSlbSslAuthPolTable2PassinfoIssuerFlag.enum(kwargs.get('PassinfoIssuerFlag', None))

    def get_indexes(self):
        return self.NameIdIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'NameIdIndex',

