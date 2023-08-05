
from radware.sdk.beans_common import *


class EnumSlbVirtServPathHideStatus(BaseBeanEnum):
    enable = 1
    disable = 2
    clear = 3


class EnumSlbVirtServPathHideHostType(BaseBeanEnum):
    sufx = 1
    prefx = 2
    eq = 3
    incl = 4
    any = 5


class EnumSlbVirtServPathHidePathType(BaseBeanEnum):
    sufx = 1
    prefx = 2
    eq = 3
    none = 4


class EnumSlbVirtServTextrepStatus(BaseBeanEnum):
    enable = 1
    disable = 2
    clear = 3


class EnumSlbVirtServTextrepAction(BaseBeanEnum):
    none = 0
    replace = 1
    remove = 2


class SlbNewCfgEnhVirtServicesFourthPartTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ServFourthPartIndex = kwargs.get('ServFourthPartIndex', None)
        self.FourthPartIndex = kwargs.get('FourthPartIndex', None)
        self.ServUrlchangNewPgName = kwargs.get('ServUrlchangNewPgName', None)
        self.ServUrlchangNewPgType = kwargs.get('ServUrlchangNewPgType', None)
        self.ServPathHideStatus = EnumSlbVirtServPathHideStatus.enum(kwargs.get('ServPathHideStatus', None))
        self.ServPathHideHostType = EnumSlbVirtServPathHideHostType.enum(kwargs.get('ServPathHideHostType', None))
        self.ServPathHideHostName = kwargs.get('ServPathHideHostName', None)
        self.ServPathHidePathType = EnumSlbVirtServPathHidePathType.enum(kwargs.get('ServPathHidePathType', None))
        self.ServPathHidePathName = kwargs.get('ServPathHidePathName', None)
        self.ServTextrepStatus = EnumSlbVirtServTextrepStatus.enum(kwargs.get('ServTextrepStatus', None))
        self.ServTextrepAction = EnumSlbVirtServTextrepAction.enum(kwargs.get('ServTextrepAction', None))

    def get_indexes(self):
        return self.ServFourthPartIndex, self.FourthPartIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'ServFourthPartIndex', 'FourthPartIndex',

