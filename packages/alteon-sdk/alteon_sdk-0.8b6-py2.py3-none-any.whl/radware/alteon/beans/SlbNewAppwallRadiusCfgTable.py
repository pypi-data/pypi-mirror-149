
from radware.sdk.beans_common import *


class EnumSlbAppwallRadiusDel(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewAppwallRadiusCfgTable(DeviceBean):
    def __init__(self, **kwargs):
        self.RadiusId = kwargs.get('RadiusId', None)
        self.RadiusPrimaryIpAddress = kwargs.get('RadiusPrimaryIpAddress', None)
        self.RadiusPrimaryPort = kwargs.get('RadiusPrimaryPort', None)
        self.RadiusPrimarySecret = kwargs.get('RadiusPrimarySecret', None)
        self.RadiusSecondaryIpAddress = kwargs.get('RadiusSecondaryIpAddress', None)
        self.RadiusSecondaryPort = kwargs.get('RadiusSecondaryPort', None)
        self.RadiusSecondarySecret = kwargs.get('RadiusSecondarySecret', None)
        self.RadiusRetries = kwargs.get('RadiusRetries', None)
        self.RadiusTimeout = kwargs.get('RadiusTimeout', None)
        self.RadiusDel = EnumSlbAppwallRadiusDel.enum(kwargs.get('RadiusDel', None))
        self.RadiusTertiaryIpAddress = kwargs.get('RadiusTertiaryIpAddress', None)
        self.RadiusTertiaryPort = kwargs.get('RadiusTertiaryPort', None)
        self.RadiusTertiarySecret = kwargs.get('RadiusTertiarySecret', None)

    def get_indexes(self):
        return self.RadiusId,
    
    @classmethod
    def get_index_names(cls):
        return 'RadiusId',

