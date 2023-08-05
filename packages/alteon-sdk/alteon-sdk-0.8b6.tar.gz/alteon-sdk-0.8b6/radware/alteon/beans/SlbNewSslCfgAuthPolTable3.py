
from radware.sdk.beans_common import *


class EnumSlbSslAuthPolTable3PassinfoNbeforeFlag(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslAuthPolTable3PassinfoNafterFlag(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslAuthPolTable3PassinfoSubjectFlag(BaseBeanEnum):
    enabled = 1
    disabled = 2


class SlbNewSslCfgAuthPolTable3(DeviceBean):
    def __init__(self, **kwargs):
        self.NameIdIndex = kwargs.get('NameIdIndex', None)
        self.PassinfoNbeforeName = kwargs.get('PassinfoNbeforeName', None)
        self.PassinfoNbeforeFlag = EnumSlbSslAuthPolTable3PassinfoNbeforeFlag.enum(kwargs.get('PassinfoNbeforeFlag', None))
        self.PassinfoNafterName = kwargs.get('PassinfoNafterName', None)
        self.PassinfoNafterFlag = EnumSlbSslAuthPolTable3PassinfoNafterFlag.enum(kwargs.get('PassinfoNafterFlag', None))
        self.PassinfoSubjectName = kwargs.get('PassinfoSubjectName', None)
        self.PassinfoSubjectFlag = EnumSlbSslAuthPolTable3PassinfoSubjectFlag.enum(kwargs.get('PassinfoSubjectFlag', None))

    def get_indexes(self):
        return self.NameIdIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'NameIdIndex',

