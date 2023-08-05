
from radware.sdk.beans_common import *


class EnumSlbVirtServiceUDPBalance(BaseBeanEnum):
    udp = 2
    tcp = 3
    stateless = 4
    tcpAndUdp = 5


class EnumSlbVirtServiceDirServerRtn(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceRtspUrlParse(BaseBeanEnum):
    none = 1
    l4hash = 2
    hash = 3
    patternMatch = 4


class EnumSlbVirtServiceDBind(BaseBeanEnum):
    enabled = 1
    disabled = 2
    forceproxy = 3


class EnumSlbVirtServiceFtpParsing(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceRemapUDPFrags(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceDnsSlb(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServicePBind(BaseBeanEnum):
    clientip = 2
    disabled = 3
    sslid = 4
    cookie = 5


class EnumSlbVirtServiceUriCookie(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceCookieMode(BaseBeanEnum):
    rewrite = 1
    passive = 2
    insert = 3


class EnumSlbVirtServiceHttpSlb(BaseBeanEnum):
    disabled = 1
    urlslb = 2
    urlhash = 3
    cookie = 4
    host = 5
    browser = 6
    others = 7
    headerhash = 8
    version = 9


class EnumSlbVirtServiceHttpSlbOption(BaseBeanEnum):
    and_ = 1
    or_ = 2
    none = 3


class EnumSlbVirtServiceHttpSlb2(BaseBeanEnum):
    disabled = 1
    urlslb = 2
    urlhash = 3
    cookie = 4
    host = 5
    browser = 6
    others = 7
    headerhash = 8
    version = 9


class EnumSlbVirtServiceDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumSlbVirtServiceApm(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceNonHTTP(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceIpRep(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceCdnProxy(BaseBeanEnum):
    enabled = 1
    disabled = 2


class SlbNewCfgEnhVirtServicesTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ServIndex = kwargs.get('ServIndex', None)
        self.Index = kwargs.get('Index', None)
        self.VirtPort = kwargs.get('VirtPort', None)
        self.RealPort = kwargs.get('RealPort', None)
        self.UDPBalance = EnumSlbVirtServiceUDPBalance.enum(kwargs.get('UDPBalance', None))
        self.BwmContract = kwargs.get('BwmContract', None)
        self.DirServerRtn = EnumSlbVirtServiceDirServerRtn.enum(kwargs.get('DirServerRtn', None))
        self.RtspUrlParse = EnumSlbVirtServiceRtspUrlParse.enum(kwargs.get('RtspUrlParse', None))
        self.DBind = EnumSlbVirtServiceDBind.enum(kwargs.get('DBind', None))
        self.FtpParsing = EnumSlbVirtServiceFtpParsing.enum(kwargs.get('FtpParsing', None))
        self.RemapUDPFrags = EnumSlbVirtServiceRemapUDPFrags.enum(kwargs.get('RemapUDPFrags', None))
        self.DnsSlb = EnumSlbVirtServiceDnsSlb.enum(kwargs.get('DnsSlb', None))
        self.ResponseCount = kwargs.get('ResponseCount', None)
        self.PBind = EnumSlbVirtServicePBind.enum(kwargs.get('PBind', None))
        self.Coffset = kwargs.get('Coffset', None)
        self.Clength = kwargs.get('Clength', None)
        self.UriCookie = EnumSlbVirtServiceUriCookie.enum(kwargs.get('UriCookie', None))
        self.CookieMode = EnumSlbVirtServiceCookieMode.enum(kwargs.get('CookieMode', None))
        self.HttpSlb = EnumSlbVirtServiceHttpSlb.enum(kwargs.get('HttpSlb', None))
        self.HttpSlbOption = EnumSlbVirtServiceHttpSlbOption.enum(kwargs.get('HttpSlbOption', None))
        self.HttpSlb2 = EnumSlbVirtServiceHttpSlb2.enum(kwargs.get('HttpSlb2', None))
        self.Delete = EnumSlbVirtServiceDelete.enum(kwargs.get('Delete', None))
        self.Apm = EnumSlbVirtServiceApm.enum(kwargs.get('Apm', None))
        self.NonHTTP = EnumSlbVirtServiceNonHTTP.enum(kwargs.get('NonHTTP', None))
        self.IpRep = EnumSlbVirtServiceIpRep.enum(kwargs.get('IpRep', None))
        self.CdnProxy = EnumSlbVirtServiceCdnProxy.enum(kwargs.get('CdnProxy', None))

    def get_indexes(self):
        return self.ServIndex, self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'ServIndex', 'Index',

