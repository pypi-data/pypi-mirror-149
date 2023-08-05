
from radware.sdk.beans_common import *


class EnumAgCurCfgSecurityDosState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSecurityDosState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgCurCfgSecurityIpAclState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSecurityIpAclState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgCurCfgSecurityUbState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSecurityUbState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgCurCfgSecurityBogonState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSecurityBogonState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgNewCfgSecurityAddAttack(BaseBeanEnum):
    iplen = 1
    ipversion = 2
    broadcast = 3
    loopback = 4
    land = 5
    ipreserved = 6
    ipttl = 7
    ipprot = 8
    ipoptlen = 9
    fragmoredont = 10
    fragdata = 11
    fragboundary = 12
    fraglast = 13
    fragdontoff = 14
    fragopt = 15
    fragoff = 16
    fragoversize = 17
    tcplen = 18
    tcpportzero = 19
    blat = 20
    tcpreserved = 21
    nullscan = 22
    fullxmasscan = 23
    finscan = 24
    vecnascan = 25
    xmassscan = 26
    synfinscan = 27
    flagabnormal = 28
    syndata = 29
    synfrag = 30
    ftpport = 31
    dnsport = 32
    seqzero = 33
    ackzero = 34
    tcpoptlen = 35
    udplen = 36
    udpportzero = 37
    fraggle = 38
    pepsi = 39
    rc8 = 40
    snmpnull = 41
    icmplen = 42
    smurf = 43
    icmpdata = 44
    icmpoff = 45
    icmptype = 46
    igmplen = 47
    igmpfrag = 48
    igmptype = 49
    arplen = 50
    arpnbcast = 51
    arpnucast = 52
    arpspoof = 53
    garp = 54
    ip6len = 55
    ip6version = 56


class EnumAgNewCfgSecurityRemAttack(BaseBeanEnum):
    iplen = 1
    ipversion = 2
    broadcast = 3
    loopback = 4
    land = 5
    ipreserved = 6
    ipttl = 7
    ipprot = 8
    ipoptlen = 9
    fragmoredont = 10
    fragdata = 11
    fragboundary = 12
    fraglast = 13
    fragdontoff = 14
    fragopt = 15
    fragoff = 16
    fragoversize = 17
    tcplen = 18
    tcpportzero = 19
    blat = 20
    tcpreserved = 21
    nullscan = 22
    fullxmasscan = 23
    finscan = 24
    vecnascan = 25
    xmassscan = 26
    synfinscan = 27
    flagabnormal = 28
    syndata = 29
    synfrag = 30
    ftpport = 31
    dnsport = 32
    seqzero = 33
    ackzero = 34
    tcpoptlen = 35
    udplen = 36
    udpportzero = 37
    fraggle = 38
    pepsi = 39
    rc8 = 40
    snmpnull = 41
    icmplen = 42
    smurf = 43
    icmpdata = 44
    icmpoff = 45
    icmptype = 46
    igmplen = 47
    igmpfrag = 48
    igmptype = 49
    arplen = 50
    arpnbcast = 51
    arpnucast = 52
    arpspoof = 53
    garp = 54
    ip6len = 55
    ip6version = 56


class EnumAgNewCfgSecurityDoSAttacks(BaseBeanEnum):
    ok = 1
    addall = 2
    remall = 3


class AgCfgSecurityPortTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.CurCfgSecurityDosState = EnumAgCurCfgSecurityDosState.enum(kwargs.get('CurCfgSecurityDosState', None))
        self.NewCfgSecurityDosState = EnumAgNewCfgSecurityDosState.enum(kwargs.get('NewCfgSecurityDosState', None))
        self.CurCfgSecurityIpAclState = EnumAgCurCfgSecurityIpAclState.enum(kwargs.get('CurCfgSecurityIpAclState', None))
        self.NewCfgSecurityIpAclState = EnumAgNewCfgSecurityIpAclState.enum(kwargs.get('NewCfgSecurityIpAclState', None))
        self.CurCfgSecurityUbState = EnumAgCurCfgSecurityUbState.enum(kwargs.get('CurCfgSecurityUbState', None))
        self.NewCfgSecurityUbState = EnumAgNewCfgSecurityUbState.enum(kwargs.get('NewCfgSecurityUbState', None))
        self.CurCfgSecurityBogonState = EnumAgCurCfgSecurityBogonState.enum(kwargs.get('CurCfgSecurityBogonState', None))
        self.NewCfgSecurityBogonState = EnumAgNewCfgSecurityBogonState.enum(kwargs.get('NewCfgSecurityBogonState', None))
        self.CurCfgSecurityAttacksBmap = kwargs.get('CurCfgSecurityAttacksBmap', None)
        self.NewCfgSecurityAttacksBmap = kwargs.get('NewCfgSecurityAttacksBmap', None)
        self.NewCfgSecurityAddAttack = EnumAgNewCfgSecurityAddAttack.enum(kwargs.get('NewCfgSecurityAddAttack', None))
        self.NewCfgSecurityRemAttack = EnumAgNewCfgSecurityRemAttack.enum(kwargs.get('NewCfgSecurityRemAttack', None))
        self.NewCfgSecurityDoSAttacks = EnumAgNewCfgSecurityDoSAttacks.enum(kwargs.get('NewCfgSecurityDoSAttacks', None))

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

