
from radware.sdk.beans_common import *


class AgDosPortStatsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.IPLen = kwargs.get('IPLen', None)
        self.IPVersion = kwargs.get('IPVersion', None)
        self.Broadcast = kwargs.get('Broadcast', None)
        self.Loopback = kwargs.get('Loopback', None)
        self.Land = kwargs.get('Land', None)
        self.IPReserved = kwargs.get('IPReserved', None)
        self.IPTTL = kwargs.get('IPTTL', None)
        self.IPProt = kwargs.get('IPProt', None)
        self.IPOptLen = kwargs.get('IPOptLen', None)
        self.FragMoreDont = kwargs.get('FragMoreDont', None)
        self.FragData = kwargs.get('FragData', None)
        self.FragBoundary = kwargs.get('FragBoundary', None)
        self.FragLast = kwargs.get('FragLast', None)
        self.FragDontOff = kwargs.get('FragDontOff', None)
        self.FragOpt = kwargs.get('FragOpt', None)
        self.FragOff = kwargs.get('FragOff', None)
        self.FragOversize = kwargs.get('FragOversize', None)
        self.TCPLen = kwargs.get('TCPLen', None)
        self.TCPPortZero = kwargs.get('TCPPortZero', None)
        self.BlatAttack = kwargs.get('BlatAttack', None)
        self.TCPReserved = kwargs.get('TCPReserved', None)
        self.NullScanAttack = kwargs.get('NullScanAttack', None)
        self.FullXmasScan = kwargs.get('FullXmasScan', None)
        self.FinScan = kwargs.get('FinScan', None)
        self.VecnaScan = kwargs.get('VecnaScan', None)
        self.XmasScanAttack = kwargs.get('XmasScanAttack', None)
        self.SynFinScan = kwargs.get('SynFinScan', None)
        self.FlagAbnormal = kwargs.get('FlagAbnormal', None)
        self.SYNData = kwargs.get('SYNData', None)
        self.SYNFrag = kwargs.get('SYNFrag', None)
        self.FTPPort = kwargs.get('FTPPort', None)
        self.DNSPort = kwargs.get('DNSPort', None)
        self.SeqZero = kwargs.get('SeqZero', None)
        self.AckZero = kwargs.get('AckZero', None)
        self.TCPOptLen = kwargs.get('TCPOptLen', None)
        self.UDPLen = kwargs.get('UDPLen', None)
        self.UDPPortZero = kwargs.get('UDPPortZero', None)
        self.FraggleAttack = kwargs.get('FraggleAttack', None)
        self.Pepsi = kwargs.get('Pepsi', None)
        self.Rc8 = kwargs.get('Rc8', None)
        self.SNMPNull = kwargs.get('SNMPNull', None)
        self.ICMPLen = kwargs.get('ICMPLen', None)
        self.SmurfAttack = kwargs.get('SmurfAttack', None)
        self.ICMPData = kwargs.get('ICMPData', None)
        self.ICMPOff = kwargs.get('ICMPOff', None)
        self.ICMPType = kwargs.get('ICMPType', None)
        self.IGMPLen = kwargs.get('IGMPLen', None)
        self.IGMPFrag = kwargs.get('IGMPFrag', None)
        self.IGMPType = kwargs.get('IGMPType', None)
        self.ARPLen = kwargs.get('ARPLen', None)
        self.ARPNbCast = kwargs.get('ARPNbCast', None)
        self.ARPNuCast = kwargs.get('ARPNuCast', None)
        self.ARPSpoof = kwargs.get('ARPSpoof', None)
        self.GARP = kwargs.get('GARP', None)
        self.IP6Len = kwargs.get('IP6Len', None)
        self.IP6Version = kwargs.get('IP6Version', None)

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

