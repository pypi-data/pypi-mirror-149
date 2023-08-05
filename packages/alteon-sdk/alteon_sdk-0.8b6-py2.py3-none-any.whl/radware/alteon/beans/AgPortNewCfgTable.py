
from radware.sdk.beans_common import *


class EnumAgPortState(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumAgPortVlanTag(BaseBeanEnum):
    tagged = 2
    untagged = 3


class EnumAgPortRmon(BaseBeanEnum):
    on = 2
    off = 3


class EnumAgPortFastEthAutoNeg(BaseBeanEnum):
    on = 2
    off = 3
    auto = 4


class EnumAgPortFastEthSpeed(BaseBeanEnum):
    mbs10 = 2
    mbs100 = 3
    any = 4
    mbs1000 = 5
    mbs10000 = 6
    mbs40000 = 7
    auto = 8
    mbs100000 = 9


class EnumAgPortFastEthMode(BaseBeanEnum):
    full_duplex = 2
    half_duplex = 3
    full_or_half_duplex = 4


class EnumAgPortFastEthFctl(BaseBeanEnum):
    transmit = 2
    receive = 3
    both = 4
    none = 5


class EnumAgPortGigEthAutoNeg(BaseBeanEnum):
    on = 2
    off = 3


class EnumAgPortGigEthFctl(BaseBeanEnum):
    transmit = 2
    receive = 3
    both = 4
    none = 5


class EnumAgPortDiscardNonIPs(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumAgPortLinkTrap(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumAgPortPreferred(BaseBeanEnum):
    copper = 1
    sfp = 2


class EnumAgPortBackup(BaseBeanEnum):
    none = 1
    copper = 2
    sfp = 3


class EnumAgPortGigEthSpeed(BaseBeanEnum):
    mbs10 = 2
    mbs100 = 3
    any = 4
    mbs1000 = 5
    mbs10000 = 6
    mbs40000 = 7
    mbs100000 = 9


class EnumAgPortGigEthMode(BaseBeanEnum):
    full_duplex = 2
    half_duplex = 3
    full_or_half_duplex = 4


class EnumAgPortPortStp(BaseBeanEnum):
    on = 1
    off = 2


class EnumAgPortPortIpFwd(BaseBeanEnum):
    enabled = 1
    disabled = 2


class AgPortNewCfgTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.State = EnumAgPortState.enum(kwargs.get('State', None))
        self.VlanTag = EnumAgPortVlanTag.enum(kwargs.get('VlanTag', None))
        self.Rmon = EnumAgPortRmon.enum(kwargs.get('Rmon', None))
        self.PVID = kwargs.get('PVID', None)
        self.FastEthAutoNeg = EnumAgPortFastEthAutoNeg.enum(kwargs.get('FastEthAutoNeg', None))
        self.FastEthSpeed = EnumAgPortFastEthSpeed.enum(kwargs.get('FastEthSpeed', None))
        self.FastEthMode = EnumAgPortFastEthMode.enum(kwargs.get('FastEthMode', None))
        self.FastEthFctl = EnumAgPortFastEthFctl.enum(kwargs.get('FastEthFctl', None))
        self.GigEthAutoNeg = EnumAgPortGigEthAutoNeg.enum(kwargs.get('GigEthAutoNeg', None))
        self.GigEthFctl = EnumAgPortGigEthFctl.enum(kwargs.get('GigEthFctl', None))
        self.PortName = kwargs.get('PortName', None)
        self.BwmContract = kwargs.get('BwmContract', None)
        self.DiscardNonIPs = EnumAgPortDiscardNonIPs.enum(kwargs.get('DiscardNonIPs', None))
        self.LinkTrap = EnumAgPortLinkTrap.enum(kwargs.get('LinkTrap', None))
        self.Preferred = EnumAgPortPreferred.enum(kwargs.get('Preferred', None))
        self.Backup = EnumAgPortBackup.enum(kwargs.get('Backup', None))
        self.EgressBW = kwargs.get('EgressBW', None)
        self.NonIPBwmContract = kwargs.get('NonIPBwmContract', None)
        self.GigEthSpeed = EnumAgPortGigEthSpeed.enum(kwargs.get('GigEthSpeed', None))
        self.GigEthMode = EnumAgPortGigEthMode.enum(kwargs.get('GigEthMode', None))
        self.PortAlias = kwargs.get('PortAlias', None)
        self.PortStp = EnumAgPortPortStp.enum(kwargs.get('PortStp', None))
        self.PortIpFwd = EnumAgPortPortIpFwd.enum(kwargs.get('PortIpFwd', None))

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

