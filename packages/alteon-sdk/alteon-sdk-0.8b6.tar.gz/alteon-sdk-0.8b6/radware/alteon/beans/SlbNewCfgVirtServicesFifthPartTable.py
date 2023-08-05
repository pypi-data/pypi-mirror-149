
from radware.sdk.beans_common import *


class EnumSlbVirtServApplicationType(BaseBeanEnum):
    basic_slb = 1
    dns = 2
    ftp = 3
    ftp_data = 4
    ldap = 5
    http = 6
    https = 7
    ssl = 8
    rtsp = 9
    sip = 10
    wts = 11
    tftp = 12
    smtp = 13
    pop3 = 14
    ip = 15


class EnumSlbVirtServiceAction(BaseBeanEnum):
    group = 1
    redirect = 2
    discard = 3


class EnumSlbVirtServiceServCertGrpMark(BaseBeanEnum):
    cert = 1
    group = 2


class EnumSlbVirtServiceDnsType(BaseBeanEnum):
    dns = 1
    dnssec = 2
    both = 3


class EnumSlbVirtServiceClntproxType(BaseBeanEnum):
    none = 1
    http = 2
    https = 3


class EnumSlbVirtServiceZerowinSize(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceCookieSecure(BaseBeanEnum):
    no = 1
    yes = 2


class EnumSlbVirtServiceNoRtsp(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceCkRebind(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceParseLimit(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceUriNorm(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceGranularity(BaseBeanEnum):
    service = 0
    real = 2


class EnumSlbVirtServiceSessLog(BaseBeanEnum):
    enabled = 1
    disabled = 2


class SlbNewCfgVirtServicesFifthPartTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ServFifthPartIndex = kwargs.get('ServFifthPartIndex', None)
        self.FifthPartIndex = kwargs.get('FifthPartIndex', None)
        self.ServTextrepMatchText = kwargs.get('ServTextrepMatchText', None)
        self.ServTextrepReplacTxt = kwargs.get('ServTextrepReplacTxt', None)
        self.ServApplicationType = EnumSlbVirtServApplicationType.enum(kwargs.get('ServApplicationType', None))
        self.Name = kwargs.get('Name', None)
        self.Action = EnumSlbVirtServiceAction.enum(kwargs.get('Action', None))
        self.Redirect = kwargs.get('Redirect', None)
        self.ServCertGrpMark = EnumSlbVirtServiceServCertGrpMark.enum(kwargs.get('ServCertGrpMark', None))
        self.DnsType = EnumSlbVirtServiceDnsType.enum(kwargs.get('DnsType', None))
        self.ClntproxType = EnumSlbVirtServiceClntproxType.enum(kwargs.get('ClntproxType', None))
        self.ZerowinSize = EnumSlbVirtServiceZerowinSize.enum(kwargs.get('ZerowinSize', None))
        self.CookiePath = kwargs.get('CookiePath', None)
        self.CookieSecure = EnumSlbVirtServiceCookieSecure.enum(kwargs.get('CookieSecure', None))
        self.NoRtsp = EnumSlbVirtServiceNoRtsp.enum(kwargs.get('NoRtsp', None))
        self.CkRebind = EnumSlbVirtServiceCkRebind.enum(kwargs.get('CkRebind', None))
        self.ParseLimit = EnumSlbVirtServiceParseLimit.enum(kwargs.get('ParseLimit', None))
        self.ParseLength = kwargs.get('ParseLength', None)
        self.UriNorm = EnumSlbVirtServiceUriNorm.enum(kwargs.get('UriNorm', None))
        self.Granularity = EnumSlbVirtServiceGranularity.enum(kwargs.get('Granularity', None))
        self.SessLog = EnumSlbVirtServiceSessLog.enum(kwargs.get('SessLog', None))
        self.AppwallWebappId = kwargs.get('AppwallWebappId', None)

    def get_indexes(self):
        return self.ServFifthPartIndex, self.FifthPartIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'ServFifthPartIndex', 'FifthPartIndex',

