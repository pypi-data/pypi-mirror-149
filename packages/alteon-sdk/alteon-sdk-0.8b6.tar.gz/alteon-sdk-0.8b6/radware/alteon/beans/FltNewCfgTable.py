
from radware.sdk.beans_common import *


class EnumFltAction(BaseBeanEnum):
    allow = 1
    deny = 2
    redirect = 3
    nat = 4
    goto = 5
    outbound_llb = 6


class EnumFltLog(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumFltNat(BaseBeanEnum):
    destination_address = 1
    source_address = 2
    multicast_address = 3


class EnumFltCache(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltInvert(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltClientProxy(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltTcpAck(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltFtpNatActive(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltAclTcpUrg(BaseBeanEnum):
    enable = 1
    disable = 2


class EnumFltAclTcpAck(BaseBeanEnum):
    enable = 1
    disable = 2


class EnumFltAclTcpPsh(BaseBeanEnum):
    enable = 1
    disable = 2


class EnumFltAclTcpRst(BaseBeanEnum):
    enable = 1
    disable = 2


class EnumFltAclTcpSyn(BaseBeanEnum):
    enable = 1
    disable = 2


class EnumFltAclTcpFin(BaseBeanEnum):
    enable = 1
    disable = 2


class EnumFltAclIpOption(BaseBeanEnum):
    enable = 1
    disable = 2


class EnumFltFwlb(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltLinklb(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltWapRadiusSnoop(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltSrcIpMac(BaseBeanEnum):
    ip = 1
    mac = 2


class EnumFltDstIpMac(BaseBeanEnum):
    ip = 1
    mac = 2


class EnumFltIdslbHash(BaseBeanEnum):
    sip = 1
    dip = 2
    sipdip = 3
    sipsport = 4
    dipdport = 5
    all = 6


class EnumFltTcpRateLimit(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltHash(BaseBeanEnum):
    auto = 1
    sip = 2
    dip = 3
    both = 4
    sipsport = 5
    dip32 = 6


class EnumFltLayer7DenyState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltRadiusWapPersist(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltPbind(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltPatternMatch(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltLayer7DenyMatchAll(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltLayer7ParseAll(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltSecurityParseAll(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltCfg8021pBitsMatch(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltEgressPip(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltDbind(BaseBeanEnum):
    enabled = 1
    disabled = 2
    forceproxy = 3


class EnumFltReverse(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltParseChn(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltSipParsing(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltSessionMirror(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltIpVer(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2


class EnumFltHdrHash(BaseBeanEnum):
    none = 1
    headerhash = 2


class EnumFltL3Filter(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltL7SipFilt(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltNbind(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltLayer7InvertAction(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltRtsrcmac(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltRtproxy(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltSesslog(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltApplicType(BaseBeanEnum):
    none = 1
    basic = 2
    http = 3
    sip = 4
    dns = 5


class EnumFltRtsport(BaseBeanEnum):
    mod5060 = 1
    preserve = 2
    disabled = 3


class EnumFltSrcAddrType(BaseBeanEnum):
    ipAddress = 1
    network = 2


class EnumFltDstAddrType(BaseBeanEnum):
    ipAddress = 1
    network = 2


class EnumFltUdpAge(BaseBeanEnum):
    onlydns = 1
    disabled = 2
    enabled = 3


class EnumFltSslInspectionEna(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltSrvCertGroup(BaseBeanEnum):
    group = 1
    cert = 2
    none = 3


class EnumFltMatchDev(BaseBeanEnum):
    allexclif = 1
    all = 2
    none = 3


class EnumFltSslL7Action(BaseBeanEnum):
    none = 1
    bypass = 2
    inspect = 3


class EnumFltFallback(BaseBeanEnum):
    allow = 1
    deny = 2
    goto = 5
    contFlow = 6


class EnumFltVpnFlood(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltMacToMe(BaseBeanEnum):
    enabled = 1
    disabled = 2


class FltNewCfgTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.SrcIp = kwargs.get('SrcIp', None)
        self.SrcIpMask = kwargs.get('SrcIpMask', None)
        self.DstIp = kwargs.get('DstIp', None)
        self.DstIpMask = kwargs.get('DstIpMask', None)
        self.Protocol = kwargs.get('Protocol', None)
        self.RangeHighSrcPort = kwargs.get('RangeHighSrcPort', None)
        self.RangeLowSrcPort = kwargs.get('RangeLowSrcPort', None)
        self.RangeLowDstPort = kwargs.get('RangeLowDstPort', None)
        self.RangeHighDstPort = kwargs.get('RangeHighDstPort', None)
        self.Action = EnumFltAction.enum(kwargs.get('Action', None))
        self.RedirPort = kwargs.get('RedirPort', None)
        self.RedirGroup = kwargs.get('RedirGroup', None)
        self.Log = EnumFltLog.enum(kwargs.get('Log', None))
        self.State = EnumFltState.enum(kwargs.get('State', None))
        self.Delete = EnumFltDelete.enum(kwargs.get('Delete', None))
        self.Nat = EnumFltNat.enum(kwargs.get('Nat', None))
        self.Cache = EnumFltCache.enum(kwargs.get('Cache', None))
        self.Invert = EnumFltInvert.enum(kwargs.get('Invert', None))
        self.ClientProxy = EnumFltClientProxy.enum(kwargs.get('ClientProxy', None))
        self.TcpAck = EnumFltTcpAck.enum(kwargs.get('TcpAck', None))
        self.SrcMac = kwargs.get('SrcMac', None)
        self.DstMac = kwargs.get('DstMac', None)
        self.FtpNatActive = EnumFltFtpNatActive.enum(kwargs.get('FtpNatActive', None))
        self.AclTcpUrg = EnumFltAclTcpUrg.enum(kwargs.get('AclTcpUrg', None))
        self.AclTcpAck = EnumFltAclTcpAck.enum(kwargs.get('AclTcpAck', None))
        self.AclTcpPsh = EnumFltAclTcpPsh.enum(kwargs.get('AclTcpPsh', None))
        self.AclTcpRst = EnumFltAclTcpRst.enum(kwargs.get('AclTcpRst', None))
        self.AclTcpSyn = EnumFltAclTcpSyn.enum(kwargs.get('AclTcpSyn', None))
        self.AclTcpFin = EnumFltAclTcpFin.enum(kwargs.get('AclTcpFin', None))
        self.AclIcmp = kwargs.get('AclIcmp', None)
        self.AclIpOption = EnumFltAclIpOption.enum(kwargs.get('AclIpOption', None))
        self.BwmContract = kwargs.get('BwmContract', None)
        self.AclIpTos = kwargs.get('AclIpTos', None)
        self.AclIpTosMask = kwargs.get('AclIpTosMask', None)
        self.AclIpTosNew = kwargs.get('AclIpTosNew', None)
        self.Fwlb = EnumFltFwlb.enum(kwargs.get('Fwlb', None))
        self.NatTimeout = kwargs.get('NatTimeout', None)
        self.Linklb = EnumFltLinklb.enum(kwargs.get('Linklb', None))
        self.WapRadiusSnoop = EnumFltWapRadiusSnoop.enum(kwargs.get('WapRadiusSnoop', None))
        self.SrcIpMac = EnumFltSrcIpMac.enum(kwargs.get('SrcIpMac', None))
        self.DstIpMac = EnumFltDstIpMac.enum(kwargs.get('DstIpMac', None))
        self.IdslbHash = EnumFltIdslbHash.enum(kwargs.get('IdslbHash', None))
        self.Vlan = kwargs.get('Vlan', None)
        self.Name = kwargs.get('Name', None)
        self.TcpRateLimit = EnumFltTcpRateLimit.enum(kwargs.get('TcpRateLimit', None))
        self.TcpRateMaxConn = kwargs.get('TcpRateMaxConn', None)
        self.Hash = EnumFltHash.enum(kwargs.get('Hash', None))
        self.Layer7DenyState = EnumFltLayer7DenyState.enum(kwargs.get('Layer7DenyState', None))
        self.Layer7DenyUrlBmap = kwargs.get('Layer7DenyUrlBmap', None)
        self.Layer7DenyAddUrl = kwargs.get('Layer7DenyAddUrl', None)
        self.Layer7DenyRemUrl = kwargs.get('Layer7DenyRemUrl', None)
        self.GotoFilter = kwargs.get('GotoFilter', None)
        self.RadiusWapPersist = EnumFltRadiusWapPersist.enum(kwargs.get('RadiusWapPersist', None))
        self.Pbind = EnumFltPbind.enum(kwargs.get('Pbind', None))
        self.TimeWindow = kwargs.get('TimeWindow', None)
        self.HoldDuration = kwargs.get('HoldDuration', None)
        self.PatternMatch = EnumFltPatternMatch.enum(kwargs.get('PatternMatch', None))
        self.Layer7DenyMatchAll = EnumFltLayer7DenyMatchAll.enum(kwargs.get('Layer7DenyMatchAll', None))
        self.ProxyIp = kwargs.get('ProxyIp', None)
        self.Layer7ParseAll = EnumFltLayer7ParseAll.enum(kwargs.get('Layer7ParseAll', None))
        self.SecurityParseAll = EnumFltSecurityParseAll.enum(kwargs.get('SecurityParseAll', None))
        self.PatternMatchGroupBmap = kwargs.get('PatternMatchGroupBmap', None)
        self.AddPatternMatchGroup = kwargs.get('AddPatternMatchGroup', None)
        self.RemPatternMatchGroup = kwargs.get('RemPatternMatchGroup', None)
        self.Cfg8021pBitsValue = kwargs.get('Cfg8021pBitsValue', None)
        self.Cfg8021pBitsMatch = EnumFltCfg8021pBitsMatch.enum(kwargs.get('Cfg8021pBitsMatch', None))
        self.AclIpLength = kwargs.get('AclIpLength', None)
        self.IdsGroup = kwargs.get('IdsGroup', None)
        self.EgressPip = EnumFltEgressPip.enum(kwargs.get('EgressPip', None))
        self.Dbind = EnumFltDbind.enum(kwargs.get('Dbind', None))
        self.RevBwmContract = kwargs.get('RevBwmContract', None)
        self.Reverse = EnumFltReverse.enum(kwargs.get('Reverse', None))
        self.ParseChn = EnumFltParseChn.enum(kwargs.get('ParseChn', None))
        self.RtpBwmContract = kwargs.get('RtpBwmContract', None)
        self.SipParsing = EnumFltSipParsing.enum(kwargs.get('SipParsing', None))
        self.SessionMirror = EnumFltSessionMirror.enum(kwargs.get('SessionMirror', None))
        self.IpVer = EnumFltIpVer.enum(kwargs.get('IpVer', None))
        self.Ipv6Sip = kwargs.get('Ipv6Sip', None)
        self.Ipv6Sprefix = kwargs.get('Ipv6Sprefix', None)
        self.Ipv6Dip = kwargs.get('Ipv6Dip', None)
        self.Ipv6Dprefix = kwargs.get('Ipv6Dprefix', None)
        self.HdrHash = EnumFltHdrHash.enum(kwargs.get('HdrHash', None))
        self.HdrName = kwargs.get('HdrName', None)
        self.HdrHashLen = kwargs.get('HdrHashLen', None)
        self.L3Filter = EnumFltL3Filter.enum(kwargs.get('L3Filter', None))
        self.NatIp = kwargs.get('NatIp', None)
        self.Ipv6Nip = kwargs.get('Ipv6Nip', None)
        self.Ipv6Proxy = kwargs.get('Ipv6Proxy', None)
        self.L7SipFilt = EnumFltL7SipFilt.enum(kwargs.get('L7SipFilt', None))
        self.NatMcastVlan = kwargs.get('NatMcastVlan', None)
        self.Nbind = EnumFltNbind.enum(kwargs.get('Nbind', None))
        self.Layer7InvertAction = EnumFltLayer7InvertAction.enum(kwargs.get('Layer7InvertAction', None))
        self.SrcClassId = kwargs.get('SrcClassId', None)
        self.DstClassId = kwargs.get('DstClassId', None)
        self.Rtsrcmac = EnumFltRtsrcmac.enum(kwargs.get('Rtsrcmac', None))
        self.Rtproxy = EnumFltRtproxy.enum(kwargs.get('Rtproxy', None))
        self.Sesslog = EnumFltSesslog.enum(kwargs.get('Sesslog', None))
        self.Cntclass = kwargs.get('Cntclass', None)
        self.ApplicType = EnumFltApplicType.enum(kwargs.get('ApplicType', None))
        self.Rtsport = EnumFltRtsport.enum(kwargs.get('Rtsport', None))
        self.SrcAddrType = EnumFltSrcAddrType.enum(kwargs.get('SrcAddrType', None))
        self.DstAddrType = EnumFltDstAddrType.enum(kwargs.get('DstAddrType', None))
        self.CosStr = kwargs.get('CosStr', None)
        self.UdpAge = EnumFltUdpAge.enum(kwargs.get('UdpAge', None))
        self.FeTcpPolId = kwargs.get('FeTcpPolId', None)
        self.BeTcpPolId = kwargs.get('BeTcpPolId', None)
        self.Comppol = kwargs.get('Comppol', None)
        self.SslInspectionEna = EnumFltSslInspectionEna.enum(kwargs.get('SslInspectionEna', None))
        self.SrvCertGroup = EnumFltSrvCertGroup.enum(kwargs.get('SrvCertGroup', None))
        self.SrvCert = kwargs.get('SrvCert', None)
        self.SslPolicy = kwargs.get('SslPolicy', None)
        self.MatchDev = EnumFltMatchDev.enum(kwargs.get('MatchDev', None))
        self.SslL7Action = EnumFltSslL7Action.enum(kwargs.get('SslL7Action', None))
        self.Fallback = EnumFltFallback.enum(kwargs.get('Fallback', None))
        self.Fbgoto = kwargs.get('Fbgoto', None)
        self.VpnFlood = EnumFltVpnFlood.enum(kwargs.get('VpnFlood', None))
        self.UrlFltPol = kwargs.get('UrlFltPol', None)
        self.Ports = kwargs.get('Ports', None)
        self.AddPort = kwargs.get('AddPort', None)
        self.RemovePort = kwargs.get('RemovePort', None)
        self.Fbport = kwargs.get('Fbport', None)
        self.MacToMe = EnumFltMacToMe.enum(kwargs.get('MacToMe', None))

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

