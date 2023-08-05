
from radware.sdk.beans_common import *


class EnumAgAccessUserCos(BaseBeanEnum):
    user = 0
    crtadmin = 1
    slboper = 2
    l4oper = 3
    oper = 4
    slbadmin = 5
    l4admin = 6
    admin = 7
    slbview = 8
    l3oper = 9
    l3admin = 10
    l1oper = 11
    l2oper = 12
    wsadmin = 13
    wsowner = 14
    wsview = 15


class EnumAgAccessUserBackDoor(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumAgAccessUserCrtMng(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumAgAccessUserState(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumAgAccessUserDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumAgAccessUserLanguage(BaseBeanEnum):
    english = 0
    chinese = 1
    korean = 2
    japanese = 3


class AgAccessUserNewCfgTable(DeviceBean):
    def __init__(self, **kwargs):
        self.UId = kwargs.get('UId', None)
        self.Cos = EnumAgAccessUserCos.enum(kwargs.get('Cos', None))
        self.Name = kwargs.get('Name', None)
        self.AdminPswd = kwargs.get('AdminPswd', None)
        self.Pswd = kwargs.get('Pswd', None)
        self.ConfPswd = kwargs.get('ConfPswd', None)
        self.BackDoor = EnumAgAccessUserBackDoor.enum(kwargs.get('BackDoor', None))
        self.CrtMng = EnumAgAccessUserCrtMng.enum(kwargs.get('CrtMng', None))
        self.RealAdd = kwargs.get('RealAdd', None)
        self.RealRem = kwargs.get('RealRem', None)
        self.State = EnumAgAccessUserState.enum(kwargs.get('State', None))
        self.Delete = EnumAgAccessUserDelete.enum(kwargs.get('Delete', None))
        self.Bmap = kwargs.get('Bmap', None)
        self.EnhRealAdd = kwargs.get('EnhRealAdd', None)
        self.EnhRealRem = kwargs.get('EnhRealRem', None)
        self.Language = EnumAgAccessUserLanguage.enum(kwargs.get('Language', None))
        self.Sshkey = kwargs.get('Sshkey', None)

    def get_indexes(self):
        return self.UId,
    
    @classmethod
    def get_index_names(cls):
        return 'UId',

