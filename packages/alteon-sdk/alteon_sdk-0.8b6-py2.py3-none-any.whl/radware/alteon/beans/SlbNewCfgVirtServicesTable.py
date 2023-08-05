
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


class EnumSlbVirtServiceDirect(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceThash(BaseBeanEnum):
    sip = 1
    sip_sport = 2


class EnumSlbVirtServiceLdapreset(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceLdapslb(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceSip(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceXForwardedFor(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceHttpRedir(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServicePbindRport(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceEgressPip(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceCookieDname(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceWts(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceUhash(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceSessionMirror(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceSoftGrid(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceSdpNat(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceConnPooling(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceProxyIpMode(BaseBeanEnum):
    ingress = 0
    egress = 1
    address = 2
    nwclss = 3
    disable = 4


class EnumSlbVirtServiceProxyIpPersistency(BaseBeanEnum):
    disable = 0
    client = 1
    host = 2


class EnumSlbVirtServiceProxyIpNWclassPersistency(BaseBeanEnum):
    disable = 0
    client = 1


class EnumSlbVirtServiceApm(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceClsRST(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceNonHTTP(BaseBeanEnum):
    enabled = 1
    disabled = 2


class SlbNewCfgVirtServicesTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ServIndex = kwargs.get('ServIndex', None)
        self.Index = kwargs.get('Index', None)
        self.VirtPort = kwargs.get('VirtPort', None)
        self.RealGroup = kwargs.get('RealGroup', None)
        self.RealPort = kwargs.get('RealPort', None)
        self.UDPBalance = EnumSlbVirtServiceUDPBalance.enum(kwargs.get('UDPBalance', None))
        self.Hname = kwargs.get('Hname', None)
        self.BwmContract = kwargs.get('BwmContract', None)
        self.DirServerRtn = EnumSlbVirtServiceDirServerRtn.enum(kwargs.get('DirServerRtn', None))
        self.RtspUrlParse = EnumSlbVirtServiceRtspUrlParse.enum(kwargs.get('RtspUrlParse', None))
        self.DBind = EnumSlbVirtServiceDBind.enum(kwargs.get('DBind', None))
        self.FtpParsing = EnumSlbVirtServiceFtpParsing.enum(kwargs.get('FtpParsing', None))
        self.RemapUDPFrags = EnumSlbVirtServiceRemapUDPFrags.enum(kwargs.get('RemapUDPFrags', None))
        self.DnsSlb = EnumSlbVirtServiceDnsSlb.enum(kwargs.get('DnsSlb', None))
        self.ResponseCount = kwargs.get('ResponseCount', None)
        self.PBind = EnumSlbVirtServicePBind.enum(kwargs.get('PBind', None))
        self.Cname = kwargs.get('Cname', None)
        self.Coffset = kwargs.get('Coffset', None)
        self.Clength = kwargs.get('Clength', None)
        self.UriCookie = EnumSlbVirtServiceUriCookie.enum(kwargs.get('UriCookie', None))
        self.CExpire = kwargs.get('CExpire', None)
        self.CookieMode = EnumSlbVirtServiceCookieMode.enum(kwargs.get('CookieMode', None))
        self.HttpSlb = EnumSlbVirtServiceHttpSlb.enum(kwargs.get('HttpSlb', None))
        self.HttpSlbOption = EnumSlbVirtServiceHttpSlbOption.enum(kwargs.get('HttpSlbOption', None))
        self.HttpSlb2 = EnumSlbVirtServiceHttpSlb2.enum(kwargs.get('HttpSlb2', None))
        self.HttpHdrName = kwargs.get('HttpHdrName', None)
        self.UrlHashLen = kwargs.get('UrlHashLen', None)
        self.Delete = EnumSlbVirtServiceDelete.enum(kwargs.get('Delete', None))
        self.Direct = EnumSlbVirtServiceDirect.enum(kwargs.get('Direct', None))
        self.Thash = EnumSlbVirtServiceThash.enum(kwargs.get('Thash', None))
        self.Ldapreset = EnumSlbVirtServiceLdapreset.enum(kwargs.get('Ldapreset', None))
        self.Ldapslb = EnumSlbVirtServiceLdapslb.enum(kwargs.get('Ldapslb', None))
        self.Sip = EnumSlbVirtServiceSip.enum(kwargs.get('Sip', None))
        self.XForwardedFor = EnumSlbVirtServiceXForwardedFor.enum(kwargs.get('XForwardedFor', None))
        self.HttpRedir = EnumSlbVirtServiceHttpRedir.enum(kwargs.get('HttpRedir', None))
        self.PbindRport = EnumSlbVirtServicePbindRport.enum(kwargs.get('PbindRport', None))
        self.EgressPip = EnumSlbVirtServiceEgressPip.enum(kwargs.get('EgressPip', None))
        self.CookieDname = EnumSlbVirtServiceCookieDname.enum(kwargs.get('CookieDname', None))
        self.Wts = EnumSlbVirtServiceWts.enum(kwargs.get('Wts', None))
        self.Uhash = EnumSlbVirtServiceUhash.enum(kwargs.get('Uhash', None))
        self.TimeOut = kwargs.get('TimeOut', None)
        self.SessionMirror = EnumSlbVirtServiceSessionMirror.enum(kwargs.get('SessionMirror', None))
        self.SoftGrid = EnumSlbVirtServiceSoftGrid.enum(kwargs.get('SoftGrid', None))
        self.SdpNat = EnumSlbVirtServiceSdpNat.enum(kwargs.get('SdpNat', None))
        self.ConnPooling = EnumSlbVirtServiceConnPooling.enum(kwargs.get('ConnPooling', None))
        self.PersistentTimeOut = kwargs.get('PersistentTimeOut', None)
        self.ProxyIpMode = EnumSlbVirtServiceProxyIpMode.enum(kwargs.get('ProxyIpMode', None))
        self.ProxyIpAddr = kwargs.get('ProxyIpAddr', None)
        self.ProxyIpMask = kwargs.get('ProxyIpMask', None)
        self.ProxyIpv6Addr = kwargs.get('ProxyIpv6Addr', None)
        self.ProxyIpv6Prefix = kwargs.get('ProxyIpv6Prefix', None)
        self.ProxyIpPersistency = EnumSlbVirtServiceProxyIpPersistency.enum(kwargs.get('ProxyIpPersistency', None))
        self.ProxyIpNWclass = kwargs.get('ProxyIpNWclass', None)
        self.ProxyIpv6NWclass = kwargs.get('ProxyIpv6NWclass', None)
        self.ProxyIpNWclassPersistency = EnumSlbVirtServiceProxyIpNWclassPersistency.enum(kwargs.get('ProxyIpNWclassPersistency', None))
        self.HashLen = kwargs.get('HashLen', None)
        self.Apm = EnumSlbVirtServiceApm.enum(kwargs.get('Apm', None))
        self.ClsRST = EnumSlbVirtServiceClsRST.enum(kwargs.get('ClsRST', None))
        self.NonHTTP = EnumSlbVirtServiceNonHTTP.enum(kwargs.get('NonHTTP', None))

    def get_indexes(self):
        return self.ServIndex, self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'ServIndex', 'Index',

