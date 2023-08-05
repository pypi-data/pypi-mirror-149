
from radware.sdk.beans_common import *


class EnumSlbVirtServiceConnmgtStatus(BaseBeanEnum):
    disabled = 0
    pooling = 1
    muxenabled = 2


class EnumSlbVirtServiceCloaksrv(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServErrcodeStatus(BaseBeanEnum):
    enabled = 1
    disabled = 2
    clear = 3


class EnumSlbVirtServErrcodeHttpRedir(BaseBeanEnum):
    yes = 1
    no = 2


class EnumSlbVirtServUrlchangStatus(BaseBeanEnum):
    enable = 1
    disable = 2
    clear = 3


class EnumSlbVirtServUrlchangHostType(BaseBeanEnum):
    sufx = 1
    prefx = 2
    eq = 3
    incl = 4
    any = 5


class SlbNewCfgVirtServicesSecondPartTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ServSecondPartIndex = kwargs.get('ServSecondPartIndex', None)
        self.SecondPartIndex = kwargs.get('SecondPartIndex', None)
        self.ConnmgtStatus = EnumSlbVirtServiceConnmgtStatus.enum(kwargs.get('ConnmgtStatus', None))
        self.ConnmgtTimeout = kwargs.get('ConnmgtTimeout', None)
        self.Cachepol = kwargs.get('Cachepol', None)
        self.Comppol = kwargs.get('Comppol', None)
        self.SSLpol = kwargs.get('SSLpol', None)
        self.ServCert = kwargs.get('ServCert', None)
        self.HttpmodList = kwargs.get('HttpmodList', None)
        self.Cloaksrv = EnumSlbVirtServiceCloaksrv.enum(kwargs.get('Cloaksrv', None))
        self.ServErrcodeStatus = EnumSlbVirtServErrcodeStatus.enum(kwargs.get('ServErrcodeStatus', None))
        self.ServErrcodeMatch = kwargs.get('ServErrcodeMatch', None)
        self.ServErrcodeHttpRedir = EnumSlbVirtServErrcodeHttpRedir.enum(kwargs.get('ServErrcodeHttpRedir', None))
        self.ServErrcodeUrl = kwargs.get('ServErrcodeUrl', None)
        self.ServErrcode = kwargs.get('ServErrcode', None)
        self.ServErrcodeNew = kwargs.get('ServErrcodeNew', None)
        self.ServErrcodeReason = kwargs.get('ServErrcodeReason', None)
        self.ServUrlchangStatus = EnumSlbVirtServUrlchangStatus.enum(kwargs.get('ServUrlchangStatus', None))
        self.ServUrlchangHostType = EnumSlbVirtServUrlchangHostType.enum(kwargs.get('ServUrlchangHostType', None))

    def get_indexes(self):
        return self.ServSecondPartIndex, self.SecondPartIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'ServSecondPartIndex', 'SecondPartIndex',

