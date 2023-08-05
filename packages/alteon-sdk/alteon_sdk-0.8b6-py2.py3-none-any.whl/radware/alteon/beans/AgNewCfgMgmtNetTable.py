
from radware.sdk.beans_common import *


class EnumAgMgmtNetDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumAgMgmtNetProtocol(BaseBeanEnum):
    ssh = 1
    telnet = 2
    sshTelnet = 3
    http = 4
    sshHttp = 5
    telnetHttp = 6
    sshTelnetHttp = 7
    https = 8
    sshHttps = 9
    httpsTelnet = 10
    sshTelnetHttps = 11
    httpHttps = 12
    sshHttpHttps = 13
    telnetHttpHttps = 14
    sshTelnetHttpHttps = 15
    snmp = 16
    sshSnmp = 17
    telnetSnmp = 18
    sshTelnetSnmp = 19
    httpSnmp = 20
    sshHttpSnmp = 21
    telnetHttpSnmp = 22
    sshTelnetHttpSnmp = 23
    httpsSnmp = 24
    sshHttpsSnmp = 25
    telnetHttpsSnmp = 26
    sshTelnetHttpsSnmp = 27
    httpHttpsSnmp = 28
    sshHttpHttpsSnmp = 29
    telnetHttpHttpsSnmp = 30
    sshTelnetHttpHttpsSnmp = 31
    report = 32
    sshreport = 33
    telnetreport = 34
    sshTelnetreport = 35
    httpreport = 36
    sshHttpreport = 37
    telnetHttpreport = 38
    sshTelnetHttpreport = 39
    httpsreport = 40
    sshHttpsreport = 41
    httpsTelnetreport = 42
    sshTelnetHttpsreport = 43
    httpHttpsreport = 44
    sshHttpHttpsreport = 45
    telnetHttpHttpsreport = 46
    sshTelnetHttpHttpsreport = 47
    snmpreport = 48
    sshSnmpreport = 49
    telnetSnmpreport = 50
    sshTelnetSnmpreport = 51
    httpSnmpreport = 52
    sshHttpSnmpreport = 53
    telnetHttpSnmpreport = 54
    sshTelnetHttpSnmpreport = 55
    httpsSnmpreport = 56
    sshHttpsSnmpreport = 57
    telnetHttpsSnmpreport = 58
    sshTelnetHttpsSnmpreport = 59
    httpHttpsSnmpreport = 60
    sshHttpHttpsSnmpreport = 61
    telnetHttpHttpsSnmpreport = 62
    sshTelnetHttpHttpsSnmpreport = 63
    none = 64


class AgNewCfgMgmtNetTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Subnet = kwargs.get('Subnet', None)
        self.Mask = kwargs.get('Mask', None)
        self.Delete = EnumAgMgmtNetDelete.enum(kwargs.get('Delete', None))
        self.Protocol = EnumAgMgmtNetProtocol.enum(kwargs.get('Protocol', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

