
from radware.sdk.beans_common import *


class EnumPortInfoSpeed(BaseBeanEnum):
    mbs10 = 2
    mbs100 = 3
    mbs1000 = 4
    any = 5
    mbs10000 = 6
    mbs40000 = 7
    auto = 8
    mbs100000 = 9


class EnumPortInfoMode(BaseBeanEnum):
    full_duplex = 2
    half_duplex = 3
    any = 4


class EnumPortInfoFlowCtrl(BaseBeanEnum):
    transmit = 2
    receive = 3
    both = 4
    none = 5


class EnumPortInfoLink(BaseBeanEnum):
    up = 1
    down = 2
    disabled = 3
    inoperative = 4


class EnumPortInfoPhyIfType(BaseBeanEnum):
    other = 1
    regular1822 = 2
    hdh1822 = 3
    ddn_x25 = 4
    rfc877_x25 = 5
    ethernet_csmacd = 6
    iso88023_csmacd = 7
    iso88024_tokenBus = 8
    iso88025_tokenRing = 9
    iso88026_man = 10
    starLan = 11
    proteon_10Mbit = 12
    proteon_80Mbit = 13
    hyperchannel = 14
    fddi = 15
    lapb = 16
    sdlc = 17
    ds1 = 18
    e1 = 19
    basicISDN = 20
    primaryISDN = 21
    propPointToPointSerial = 22
    ppp = 23
    softwareLoopback = 24
    eon = 25
    ethernet_3Mbit = 26
    nsip = 27
    slip = 28
    ultra = 29
    ds3 = 30
    sip = 31
    frame_relay = 32


class EnumPortInfoPhyIfOperStatus(BaseBeanEnum):
    up = 1
    down = 2
    testing = 3


class EnumPortInfoPhyConnType(BaseBeanEnum):
    feCopper = 1
    geCopper = 2
    geSFP = 3
    unknown = 4
    xGeSFP = 5
    xGeQSFP = 6


class EnumPortInfoPreferred(BaseBeanEnum):
    invalid = 1
    copper = 2
    sfp = 3


class EnumPortInfoBackup(BaseBeanEnum):
    invalid = 1
    none = 2
    copper = 3
    sfp = 4


class EnumPortInfoSFPType(BaseBeanEnum):
    invalid = 1
    sfpTypeSX = 2
    sfpTypeLX = 3
    sfpTypeCX = 4
    sfpTypeCopper = 5


class EnumPortInfoShared(BaseBeanEnum):
    enabled = 1
    disabled = 2


class PortInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.Speed = EnumPortInfoSpeed.enum(kwargs.get('Speed', None))
        self.Mode = EnumPortInfoMode.enum(kwargs.get('Mode', None))
        self.FlowCtrl = EnumPortInfoFlowCtrl.enum(kwargs.get('FlowCtrl', None))
        self.Link = EnumPortInfoLink.enum(kwargs.get('Link', None))
        self.PhyIfDescr = kwargs.get('PhyIfDescr', None)
        self.PhyIfType = EnumPortInfoPhyIfType.enum(kwargs.get('PhyIfType', None))
        self.PhyIfMtu = kwargs.get('PhyIfMtu', None)
        self.PhyIfPhysAddress = kwargs.get('PhyIfPhysAddress', None)
        self.PhyIfOperStatus = EnumPortInfoPhyIfOperStatus.enum(kwargs.get('PhyIfOperStatus', None))
        self.PhyIfLastChange = kwargs.get('PhyIfLastChange', None)
        self.PhyConnType = EnumPortInfoPhyConnType.enum(kwargs.get('PhyConnType', None))
        self.Preferred = EnumPortInfoPreferred.enum(kwargs.get('Preferred', None))
        self.Backup = EnumPortInfoBackup.enum(kwargs.get('Backup', None))
        self.SFPName = kwargs.get('SFPName', None)
        self.SFPType = EnumPortInfoSFPType.enum(kwargs.get('SFPType', None))
        self.Shared = EnumPortInfoShared.enum(kwargs.get('Shared', None))
        self.VADC = kwargs.get('VADC', None)
        self.VADCs = kwargs.get('VADCs', None)

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

