
from radware.sdk.beans_common import *


class EnumVADCSysMmgmtState(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVADCSysHttpsState(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVADCSysSshState(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVADCSysHttpState(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVADCSysSnmpState(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVADCSysSyslogState(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVADCSysRadiusState(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVADCSysTacacsState(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVADCSysIdleState(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVADCSysSmtpState(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVADCSyslogDelegation(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVADCRadiusDelegation(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVADCTacacsDelegation(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVADCSmtpDelegation(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVADCSysTnetState(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVADCIdleDelegation(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVADCSysMmgmtDelegation(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVADCSysGlobalLanguage(BaseBeanEnum):
    english = 0
    chinese = 1
    korean = 2
    japanese = 3


class VADCNewCfgSysTable(DeviceBean):
    def __init__(self, **kwargs):
        self.MmgmtAddr = kwargs.get('MmgmtAddr', None)
        self.MmgmtMask = kwargs.get('MmgmtMask', None)
        self.MmgmtGw = kwargs.get('MmgmtGw', None)
        self.MmgmtState = EnumVADCSysMmgmtState.enum(kwargs.get('MmgmtState', None))
        self.PeerAddr = kwargs.get('PeerAddr', None)
        self.PeerMask = kwargs.get('PeerMask', None)
        self.PeerGw = kwargs.get('PeerGw', None)
        self.HttpsState = EnumVADCSysHttpsState.enum(kwargs.get('HttpsState', None))
        self.SshState = EnumVADCSysSshState.enum(kwargs.get('SshState', None))
        self.HttpState = EnumVADCSysHttpState.enum(kwargs.get('HttpState', None))
        self.SnmpState = EnumVADCSysSnmpState.enum(kwargs.get('SnmpState', None))
        self.SyslogState = EnumVADCSysSyslogState.enum(kwargs.get('SyslogState', None))
        self.RadiusState = EnumVADCSysRadiusState.enum(kwargs.get('RadiusState', None))
        self.TacacsState = EnumVADCSysTacacsState.enum(kwargs.get('TacacsState', None))
        self.IdleState = EnumVADCSysIdleState.enum(kwargs.get('IdleState', None))
        self.SmtpState = EnumVADCSysSmtpState.enum(kwargs.get('SmtpState', None))
        self.SyslogDelegation = EnumVADCSyslogDelegation.enum(kwargs.get('SyslogDelegation', None))
        self.RadiusDelegation = EnumVADCRadiusDelegation.enum(kwargs.get('RadiusDelegation', None))
        self.TacacsDelegation = EnumVADCTacacsDelegation.enum(kwargs.get('TacacsDelegation', None))
        self.SmtpDelegation = EnumVADCSmtpDelegation.enum(kwargs.get('SmtpDelegation', None))
        self.MmgmtIpv6Addr = kwargs.get('MmgmtIpv6Addr', None)
        self.MmgmtIpv6PrefixLen = kwargs.get('MmgmtIpv6PrefixLen', None)
        self.MmgmtIpv6Gateway = kwargs.get('MmgmtIpv6Gateway', None)
        self.PeerIpv6Addr = kwargs.get('PeerIpv6Addr', None)
        self.PeerIpv6PrefixLen = kwargs.get('PeerIpv6PrefixLen', None)
        self.PeerIpv6Gateway = kwargs.get('PeerIpv6Gateway', None)
        self.TnetState = EnumVADCSysTnetState.enum(kwargs.get('TnetState', None))
        self.HaId = kwargs.get('HaId', None)
        self.PeerId = kwargs.get('PeerId', None)
        self.VADCId = kwargs.get('VADCId', None)
        self.IdleDelegation = EnumVADCIdleDelegation.enum(kwargs.get('IdleDelegation', None))
        self.MmgmtDelegation = EnumVADCSysMmgmtDelegation.enum(kwargs.get('MmgmtDelegation', None))
        self.PeerName = kwargs.get('PeerName', None)
        self.GlobalLanguage = EnumVADCSysGlobalLanguage.enum(kwargs.get('GlobalLanguage', None))

    def get_indexes(self):
        return self.VADCId,
    
    @classmethod
    def get_index_names(cls):
        return 'VADCId',

