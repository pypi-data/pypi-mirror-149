
from radware.sdk.beans_common import *


class EnumSlbGroupMetric(BaseBeanEnum):
    roundRobin = 1
    leastConnections = 2
    minMisses = 3
    hash = 4
    response = 5
    bandwidth = 6
    phash = 7
    svcLeast = 8
    hrw = 9


class EnumSlbGroupHealthCheckLayer(BaseBeanEnum):
    icmp = 1
    tcp = 2
    http = 3
    httphead = 44
    dns = 4
    smtp = 5
    pop3 = 6
    nntp = 7
    ftp = 8
    imap = 9
    radius = 10
    sslh = 11
    script1 = 12
    script2 = 13
    script3 = 14
    script4 = 15
    script5 = 16
    script6 = 17
    script7 = 18
    script8 = 19
    script9 = 20
    script10 = 21
    script11 = 22
    script12 = 23
    script13 = 24
    script14 = 25
    script15 = 26
    script16 = 27
    link = 28
    wsp = 29
    wtls = 30
    ldap = 31
    udpdns = 32
    arp = 33
    snmp1 = 34
    snmp2 = 35
    snmp3 = 36
    snmp4 = 37
    snmp5 = 38
    radiusacs = 39
    tftp = 40
    wtp = 41
    rtsp = 42
    sipping = 43
    sipoptions = 45
    wts = 46
    dhcp = 47
    radiusaa = 48
    sslv3 = 49
    script17 = 116
    script18 = 117
    script19 = 118
    script20 = 119
    script21 = 120
    script22 = 121
    script23 = 122
    script24 = 123
    script25 = 124
    script26 = 125
    script27 = 126
    script28 = 127
    script29 = 128
    script30 = 129
    script31 = 130
    script32 = 131
    script33 = 132
    script34 = 133
    script35 = 134
    script36 = 135
    script37 = 136
    script38 = 137
    script39 = 138
    script40 = 139
    script41 = 140
    script42 = 141
    script43 = 142
    script44 = 143
    script45 = 144
    script46 = 145
    script47 = 146
    script48 = 147
    script49 = 148
    script50 = 149
    script51 = 150
    script52 = 151
    script53 = 152
    script54 = 153
    script55 = 154
    script56 = 155
    script57 = 156
    script58 = 157
    script59 = 158
    script60 = 159
    script61 = 160
    script62 = 161
    script63 = 162
    script64 = 163
    none = 164
    unknown = 165


class EnumSlbGroupVipHealthCheck(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbGroupIdsState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbGroupDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumSlbGroupIdsFlood(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbGroupMinmissHash(BaseBeanEnum):
    minmiss_24 = 1
    minmiss_32 = 2


class EnumSlbGroupRmetric(BaseBeanEnum):
    roundRobin = 1
    hash = 2
    leastConnections = 3


class EnumSlbGroupOperatorAccess(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbGroupIpVer(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2
    mixed = 3


class EnumSlbGroupBackupType(BaseBeanEnum):
    none = 1
    server = 2
    group = 3


class EnumSlbGroupIdsChain(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbGroupMaxConEx(BaseBeanEnum):
    enabled = 1
    disabled = 2


class SlbNewCfgGroupTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.RealServers = kwargs.get('RealServers', None)
        self.AddServer = kwargs.get('AddServer', None)
        self.RemoveServer = kwargs.get('RemoveServer', None)
        self.Metric = EnumSlbGroupMetric.enum(kwargs.get('Metric', None))
        self.BackupServer = kwargs.get('BackupServer', None)
        self.BackupGroup = kwargs.get('BackupGroup', None)
        self.HealthCheckUrl = kwargs.get('HealthCheckUrl', None)
        self.HealthCheckLayer = EnumSlbGroupHealthCheckLayer.enum(kwargs.get('HealthCheckLayer', None))
        self.Name = kwargs.get('Name', None)
        self.RealThreshold = kwargs.get('RealThreshold', None)
        self.VipHealthCheck = EnumSlbGroupVipHealthCheck.enum(kwargs.get('VipHealthCheck', None))
        self.IdsState = EnumSlbGroupIdsState.enum(kwargs.get('IdsState', None))
        self.IdsPort = kwargs.get('IdsPort', None)
        self.Delete = EnumSlbGroupDelete.enum(kwargs.get('Delete', None))
        self.IdsFlood = EnumSlbGroupIdsFlood.enum(kwargs.get('IdsFlood', None))
        self.MinmissHash = EnumSlbGroupMinmissHash.enum(kwargs.get('MinmissHash', None))
        self.PhashMask = kwargs.get('PhashMask', None)
        self.Rmetric = EnumSlbGroupRmetric.enum(kwargs.get('Rmetric', None))
        self.HealthCheckFormula = kwargs.get('HealthCheckFormula', None)
        self.OperatorAccess = EnumSlbGroupOperatorAccess.enum(kwargs.get('OperatorAccess', None))
        self.Wlm = kwargs.get('Wlm', None)
        self.RadiusAuthenString = kwargs.get('RadiusAuthenString', None)
        self.SecBackupGroup = kwargs.get('SecBackupGroup', None)
        self.Slowstart = kwargs.get('Slowstart', None)
        self.MinThreshold = kwargs.get('MinThreshold', None)
        self.MaxThreshold = kwargs.get('MaxThreshold', None)
        self.IpVer = EnumSlbGroupIpVer.enum(kwargs.get('IpVer', None))
        self.Backup = kwargs.get('Backup', None)
        self.BackupType = EnumSlbGroupBackupType.enum(kwargs.get('BackupType', None))
        self.HealthID = kwargs.get('HealthID', None)
        self.PhashPrefixLength = kwargs.get('PhashPrefixLength', None)
        self.IdsChain = EnumSlbGroupIdsChain.enum(kwargs.get('IdsChain', None))
        self.MaxConEx = EnumSlbGroupMaxConEx.enum(kwargs.get('MaxConEx', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

