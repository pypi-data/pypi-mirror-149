
from radware.sdk.beans_common import *


class EnumFltExtendedLayer7DenyState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltExtendedRadiusWapPersist(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltExtendedPbind(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltExtendedPatternMatch(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltExtendedLayer7DenyMatchAll(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltExtendedLayer7ParseAll(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltExtendedSecurityParseAll(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltExtended8021pBitsMatch(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltExtendedEgressPip(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltExtendedDbind(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltExtendedReverse(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltExtendedParseChn(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltExtendedSipParsing(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltExtendedSessionMirror(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltExtendedIpVer(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2


class EnumFltExtendedHdrHash(BaseBeanEnum):
    none = 1
    headerhash = 2


class EnumFltExtendedL7SipFilt(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltExtendedNbind(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltExtendedL3State(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumFltExtendedProx(BaseBeanEnum):
    enabled = 1
    disabled = 2


class FltNewCfgExtendedTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.Layer7DenyState = EnumFltExtendedLayer7DenyState.enum(kwargs.get('Layer7DenyState', None))
        self.Layer7DenyUrlBmap = kwargs.get('Layer7DenyUrlBmap', None)
        self.Layer7DenyAddUrl = kwargs.get('Layer7DenyAddUrl', None)
        self.Layer7DenyRemUrl = kwargs.get('Layer7DenyRemUrl', None)
        self.GotoFilter = kwargs.get('GotoFilter', None)
        self.RadiusWapPersist = EnumFltExtendedRadiusWapPersist.enum(kwargs.get('RadiusWapPersist', None))
        self.Pbind = EnumFltExtendedPbind.enum(kwargs.get('Pbind', None))
        self.TimeWindow = kwargs.get('TimeWindow', None)
        self.HoldDuration = kwargs.get('HoldDuration', None)
        self.PatternMatch = EnumFltExtendedPatternMatch.enum(kwargs.get('PatternMatch', None))
        self.Layer7DenyMatchAll = EnumFltExtendedLayer7DenyMatchAll.enum(kwargs.get('Layer7DenyMatchAll', None))
        self.ProxyIp = kwargs.get('ProxyIp', None)
        self.Layer7ParseAll = EnumFltExtendedLayer7ParseAll.enum(kwargs.get('Layer7ParseAll', None))
        self.SecurityParseAll = EnumFltExtendedSecurityParseAll.enum(kwargs.get('SecurityParseAll', None))
        self.PatternMatchGroupBmap = kwargs.get('PatternMatchGroupBmap', None)
        self.AddPatternMatchGroup = kwargs.get('AddPatternMatchGroup', None)
        self.RemPatternMatchGroup = kwargs.get('RemPatternMatchGroup', None)
        self.Extended8021pBitsValue = kwargs.get('Extended8021pBitsValue', None)
        self.Extended8021pBitsMatch = EnumFltExtended8021pBitsMatch.enum(kwargs.get('Extended8021pBitsMatch', None))
        self.AclIpLength = kwargs.get('AclIpLength', None)
        self.IdsGroup = kwargs.get('IdsGroup', None)
        self.EgressPip = EnumFltExtendedEgressPip.enum(kwargs.get('EgressPip', None))
        self.Dbind = EnumFltExtendedDbind.enum(kwargs.get('Dbind', None))
        self.RevBwmContract = kwargs.get('RevBwmContract', None)
        self.Reverse = EnumFltExtendedReverse.enum(kwargs.get('Reverse', None))
        self.ParseChn = EnumFltExtendedParseChn.enum(kwargs.get('ParseChn', None))
        self.RtpBwmContract = kwargs.get('RtpBwmContract', None)
        self.SipParsing = EnumFltExtendedSipParsing.enum(kwargs.get('SipParsing', None))
        self.SessionMirror = EnumFltExtendedSessionMirror.enum(kwargs.get('SessionMirror', None))
        self.IpVer = EnumFltExtendedIpVer.enum(kwargs.get('IpVer', None))
        self.Ipv6Sip = kwargs.get('Ipv6Sip', None)
        self.Ipv6Sprefix = kwargs.get('Ipv6Sprefix', None)
        self.Ipv6Dip = kwargs.get('Ipv6Dip', None)
        self.Ipv6Dprefix = kwargs.get('Ipv6Dprefix', None)
        self.HdrHash = EnumFltExtendedHdrHash.enum(kwargs.get('HdrHash', None))
        self.HdrName = kwargs.get('HdrName', None)
        self.HdrHashLen = kwargs.get('HdrHashLen', None)
        self.NatIp = kwargs.get('NatIp', None)
        self.Ipv6Nip = kwargs.get('Ipv6Nip', None)
        self.Ipv6Proxy = kwargs.get('Ipv6Proxy', None)
        self.L7SipFilt = EnumFltExtendedL7SipFilt.enum(kwargs.get('L7SipFilt', None))
        self.NatMcastVlan = kwargs.get('NatMcastVlan', None)
        self.Nbind = EnumFltExtendedNbind.enum(kwargs.get('Nbind', None))
        self.L3State = EnumFltExtendedL3State.enum(kwargs.get('L3State', None))
        self.RedirGroup = kwargs.get('RedirGroup', None)
        self.IdsGroupEnh = kwargs.get('IdsGroupEnh', None)
        self.SourceIp = kwargs.get('SourceIp', None)
        self.DestIp = kwargs.get('DestIp', None)
        self.SourceMask = kwargs.get('SourceMask', None)
        self.DestMask = kwargs.get('DestMask', None)
        self.Prox = EnumFltExtendedProx.enum(kwargs.get('Prox', None))

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

