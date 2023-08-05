
from radware.sdk.beans_common import *


class EnumSlbAdvhcDhcpDhcpType(BaseBeanEnum):
    inherit = 1
    inform = 2
    request = 3
    relay = 4


class EnumSlbAdvhcDhcpSourcePortType(BaseBeanEnum):
    inherit = 1
    random = 2
    strict = 3


class EnumSlbAdvhcDhcpDhcpDuidType(BaseBeanEnum):
    linklayertime = 1
    linklayer = 3


class SlbNewAdvhcDhcpTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ID = kwargs.get('ID', None)
        self.Name = kwargs.get('Name', None)
        self.DPort = kwargs.get('DPort', None)
        self.IPVer = kwargs.get('IPVer', None)
        self.HostName = kwargs.get('HostName', None)
        self.Transparent = kwargs.get('Transparent', None)
        self.Interval = kwargs.get('Interval', None)
        self.Retries = kwargs.get('Retries', None)
        self.RestoreRetries = kwargs.get('RestoreRetries', None)
        self.Timeout = kwargs.get('Timeout', None)
        self.Overflow = kwargs.get('Overflow', None)
        self.DownInterval = kwargs.get('DownInterval', None)
        self.Invert = kwargs.get('Invert', None)
        self.DhcpType = EnumSlbAdvhcDhcpDhcpType.enum(kwargs.get('DhcpType', None))
        self.SourcePortType = EnumSlbAdvhcDhcpSourcePortType.enum(kwargs.get('SourcePortType', None))
        self.Copy = kwargs.get('Copy', None)
        self.Delete = kwargs.get('Delete', None)
        self.DhcpDuidType = EnumSlbAdvhcDhcpDhcpDuidType.enum(kwargs.get('DhcpDuidType', None))
        self.DhcpDuidLLA = kwargs.get('DhcpDuidLLA', None)
        self.DhcpDuidTime = kwargs.get('DhcpDuidTime', None)

    def get_indexes(self):
        return self.ID,
    
    @classmethod
    def get_index_names(cls):
        return 'ID',

