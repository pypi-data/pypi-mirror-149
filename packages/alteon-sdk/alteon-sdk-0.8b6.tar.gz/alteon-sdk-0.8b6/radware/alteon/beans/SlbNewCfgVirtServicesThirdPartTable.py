
from radware.sdk.beans_common import *


class EnumSlbVirtServUrlchangPathType(BaseBeanEnum):
    sufx = 1
    prefx = 2
    eq = 3
    incl = 4
    any = 5
    none = 6


class EnumSlbVirtServUrlchangActnType(BaseBeanEnum):
    insert = 1
    replace = 2
    remove = 3
    none = 4


class EnumSlbVirtServUrlchangInsrtPostn(BaseBeanEnum):
    before = 1
    after = 2


class SlbNewCfgVirtServicesThirdPartTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ServThirdPartIndex = kwargs.get('ServThirdPartIndex', None)
        self.ThirdPartIndex = kwargs.get('ThirdPartIndex', None)
        self.ServUrlchangHostName = kwargs.get('ServUrlchangHostName', None)
        self.ServUrlchangPathType = EnumSlbVirtServUrlchangPathType.enum(kwargs.get('ServUrlchangPathType', None))
        self.ServUrlchangPathMatch = kwargs.get('ServUrlchangPathMatch', None)
        self.ServUrlchangPageName = kwargs.get('ServUrlchangPageName', None)
        self.ServUrlchangPageType = kwargs.get('ServUrlchangPageType', None)
        self.ServUrlchangActnType = EnumSlbVirtServUrlchangActnType.enum(kwargs.get('ServUrlchangActnType', None))
        self.ServUrlchangPathInsrt = kwargs.get('ServUrlchangPathInsrt', None)
        self.ServUrlchangInsrtPostn = EnumSlbVirtServUrlchangInsrtPostn.enum(kwargs.get('ServUrlchangInsrtPostn', None))

    def get_indexes(self):
        return self.ServThirdPartIndex, self.ThirdPartIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'ServThirdPartIndex', 'ThirdPartIndex',

