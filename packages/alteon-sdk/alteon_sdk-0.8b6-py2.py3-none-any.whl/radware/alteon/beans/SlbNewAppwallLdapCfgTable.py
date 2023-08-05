
from radware.sdk.beans_common import *


class EnumSlbAppwallLdapSSLEnable(BaseBeanEnum):
    disable = 0
    enable = 1


class EnumSlbAppwallLdapTLSEnable(BaseBeanEnum):
    disable = 0
    enable = 1


class EnumSlbAppwallLdapSrvType(BaseBeanEnum):
    microsoftActDirect = 0
    redhatDirect = 1
    appleOpenDirect = 2
    otherDirect = 3


class EnumSlbAppwallLdapDel(BaseBeanEnum):
    other = 1
    delete = 2


class EnumSlbAppwallLdapIgnoreEnable(BaseBeanEnum):
    disable = 0
    enable = 1


class SlbNewAppwallLdapCfgTable(DeviceBean):
    def __init__(self, **kwargs):
        self.LdapId = kwargs.get('LdapId', None)
        self.LdapPrimaryIpAddress = kwargs.get('LdapPrimaryIpAddress', None)
        self.LdapPrimaryPort = kwargs.get('LdapPrimaryPort', None)
        self.LdapSecondaryIpAddress = kwargs.get('LdapSecondaryIpAddress', None)
        self.LdapSecondaryPort = kwargs.get('LdapSecondaryPort', None)
        self.LdapReqTimeoutSec = kwargs.get('LdapReqTimeoutSec', None)
        self.LdapHostTimeoutSec = kwargs.get('LdapHostTimeoutSec', None)
        self.LdapSSLEnable = EnumSlbAppwallLdapSSLEnable.enum(kwargs.get('LdapSSLEnable', None))
        self.LdapTLSEnable = EnumSlbAppwallLdapTLSEnable.enum(kwargs.get('LdapTLSEnable', None))
        self.LdapSrvType = EnumSlbAppwallLdapSrvType.enum(kwargs.get('LdapSrvType', None))
        self.LdapBase = kwargs.get('LdapBase', None)
        self.LdapUserTest = kwargs.get('LdapUserTest', None)
        self.LdapPassTest = kwargs.get('LdapPassTest', None)
        self.LdapDel = EnumSlbAppwallLdapDel.enum(kwargs.get('LdapDel', None))
        self.LdapIgnoreEnable = EnumSlbAppwallLdapIgnoreEnable.enum(kwargs.get('LdapIgnoreEnable', None))

    def get_indexes(self):
        return self.LdapId,
    
    @classmethod
    def get_index_names(cls):
        return 'LdapId',

