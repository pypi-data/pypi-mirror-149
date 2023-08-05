
from radware.sdk.beans_common import *


class EnumTargetAddrEnaTrap(BaseBeanEnum):
    console = 1
    system = 2
    mgmt = 3
    cli = 4
    stp = 5
    vlan = 6
    slb = 7
    gslb = 8
    filter = 9
    ssh = 10
    vrrp = 11
    bgp = 12
    ntp = 13
    ip = 16
    synatk = 19
    tcplim = 20
    ospf = 21
    slbatk = 23
    security = 24
    rmon = 25
    ip6 = 28
    appsvc = 29
    ospfv3 = 32
    web = 18
    vautoip = 33
    fastview = 34
    audit = 35
    ha = 36


class EnumTargetAddrDisTrap(BaseBeanEnum):
    console = 1
    system = 2
    mgmt = 3
    cli = 4
    stp = 5
    vlan = 6
    slb = 7
    gslb = 8
    filter = 9
    ssh = 10
    vrrp = 11
    bgp = 12
    ntp = 13
    ip = 16
    synatk = 19
    tcplim = 20
    ospf = 21
    slbatk = 23
    security = 24
    rmon = 25
    ip6 = 28
    appsvc = 29
    ospfv3 = 32
    web = 18
    vautoip = 33
    fastview = 34
    audit = 35
    ha = 36


class EnumTargetAddrDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumTargetAddrIpVer(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2


class TargetAddrNewCfgTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Name = kwargs.get('Name', None)
        self.TransIp = kwargs.get('TransIp', None)
        self.TransPort = kwargs.get('TransPort', None)
        self.TagList = kwargs.get('TagList', None)
        self.ParamsName = kwargs.get('ParamsName', None)
        self.EnaTrap = EnumTargetAddrEnaTrap.enum(kwargs.get('EnaTrap', None))
        self.DisTrap = EnumTargetAddrDisTrap.enum(kwargs.get('DisTrap', None))
        self.Delete = EnumTargetAddrDelete.enum(kwargs.get('Delete', None))
        self.TransIpv6 = kwargs.get('TransIpv6', None)
        self.IpVer = EnumTargetAddrIpVer.enum(kwargs.get('IpVer', None))
        self.TrapBmap = kwargs.get('TrapBmap', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

