
from radware.sdk.beans_common import *


class EnumVADCUserCos(BaseBeanEnum):
    user = 0
    l3oper = 1
    slboper = 2
    slbview = 3
    crtadmin = 4
    l4oper = 5
    oper = 6
    l3admin = 7
    slbadmin = 8
    l4admin = 9
    admin = 10


class EnumVADCUserBackdoor(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVADCUserCrtMng(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVADCUserState(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVADCUserDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumVADCUserLanguage(BaseBeanEnum):
    english = 0
    chinese = 1
    korean = 2
    japanese = 3


class VADCUserNewCfgTable(DeviceBean):
    def __init__(self, **kwargs):
        self.VADCId = kwargs.get('VADCId', None)
        self.UId = kwargs.get('UId', None)
        self.Cos = EnumVADCUserCos.enum(kwargs.get('Cos', None))
        self.Name = kwargs.get('Name', None)
        self.AdminPswd = kwargs.get('AdminPswd', None)
        self.Pswd = kwargs.get('Pswd', None)
        self.ConfPswd = kwargs.get('ConfPswd', None)
        self.Backdoor = EnumVADCUserBackdoor.enum(kwargs.get('Backdoor', None))
        self.CrtMng = EnumVADCUserCrtMng.enum(kwargs.get('CrtMng', None))
        self.State = EnumVADCUserState.enum(kwargs.get('State', None))
        self.Delete = EnumVADCUserDelete.enum(kwargs.get('Delete', None))
        self.Language = EnumVADCUserLanguage.enum(kwargs.get('Language', None))

    def get_indexes(self):
        return self.VADCId, self.UId,
    
    @classmethod
    def get_index_names(cls):
        return 'VADCId', 'UId',

