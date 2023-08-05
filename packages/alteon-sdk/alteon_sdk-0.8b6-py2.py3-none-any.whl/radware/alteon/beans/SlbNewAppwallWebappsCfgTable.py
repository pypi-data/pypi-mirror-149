
from radware.sdk.beans_common import *


class EnumSlbAppwallWebappEnable(BaseBeanEnum):
    disable = 0
    enable = 1


class EnumSlbAppwallWebappEnableWaf(BaseBeanEnum):
    disable = 0
    enable = 1


class EnumSlbAppwallWebappEnableAuthSso(BaseBeanEnum):
    disable = 0
    enable = 1


class EnumSlbAppwallWebappMode(BaseBeanEnum):
    oop = 0
    inline = 1


class EnumSlbAppwallWebappDel(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewAppwallWebappsCfgTable(DeviceBean):
    def __init__(self, **kwargs):
        self.WebappId = kwargs.get('WebappId', None)
        self.WebappName = kwargs.get('WebappName', None)
        self.WebappEnable = EnumSlbAppwallWebappEnable.enum(kwargs.get('WebappEnable', None))
        self.WebappEnableWaf = EnumSlbAppwallWebappEnableWaf.enum(kwargs.get('WebappEnableWaf', None))
        self.WebappEnableAuthSso = EnumSlbAppwallWebappEnableAuthSso.enum(kwargs.get('WebappEnableAuthSso', None))
        self.WebappMode = EnumSlbAppwallWebappMode.enum(kwargs.get('WebappMode', None))
        self.WebappDel = EnumSlbAppwallWebappDel.enum(kwargs.get('WebappDel', None))

    def get_indexes(self):
        return self.WebappId,
    
    @classmethod
    def get_index_names(cls):
        return 'WebappId',

