
from radware.sdk.beans_common import *


class EnumIfType(BaseBeanEnum):
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


class EnumIfAdminStatus(BaseBeanEnum):
    up = 1
    down = 2
    testing = 3


class EnumIfOperStatus(BaseBeanEnum):
    up = 1
    down = 2
    testing = 3


class IfTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Descr = kwargs.get('Descr', None)
        self.Type = EnumIfType.enum(kwargs.get('Type', None))
        self.Mtu = kwargs.get('Mtu', None)
        self.Speed = kwargs.get('Speed', None)
        self.PhysAddress = kwargs.get('PhysAddress', None)
        self.AdminStatus = EnumIfAdminStatus.enum(kwargs.get('AdminStatus', None))
        self.OperStatus = EnumIfOperStatus.enum(kwargs.get('OperStatus', None))
        self.LastChange = kwargs.get('LastChange', None)
        self.InOctets = kwargs.get('InOctets', None)
        self.InUcastPkts = kwargs.get('InUcastPkts', None)
        self.InNUcastPkts = kwargs.get('InNUcastPkts', None)
        self.InDiscards = kwargs.get('InDiscards', None)
        self.InErrors = kwargs.get('InErrors', None)
        self.InUnknownProtos = kwargs.get('InUnknownProtos', None)
        self.OutOctets = kwargs.get('OutOctets', None)
        self.OutUcastPkts = kwargs.get('OutUcastPkts', None)
        self.OutNUcastPkts = kwargs.get('OutNUcastPkts', None)
        self.OutDiscards = kwargs.get('OutDiscards', None)
        self.OutErrors = kwargs.get('OutErrors', None)
        self.OutQLen = kwargs.get('OutQLen', None)
        self.Specific = kwargs.get('Specific', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

