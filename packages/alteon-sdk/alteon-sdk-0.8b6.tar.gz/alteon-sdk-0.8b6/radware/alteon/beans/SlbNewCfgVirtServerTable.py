
from radware.sdk.beans_common import *


class EnumSlbVirtServerLayer3Only(BaseBeanEnum):
    layer3Only = 1
    disabled = 2


class EnumSlbVirtServerState(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumSlbVirtServerDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumSlbVirtServerIpVer(BaseBeanEnum):
    ipv4 = 1
    ipv6 = 2


class EnumSlbVirtServerCReset(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServerIsDnsSecVip(BaseBeanEnum):
    no = 0
    yes = 1


class SlbNewCfgVirtServerTable(DeviceBean):
    def __init__(self, **kwargs):
        self.VirtServerIndex = kwargs.get('VirtServerIndex', None)
        self.VirtServerIpAddress = kwargs.get('VirtServerIpAddress', None)
        self.VirtServerLayer3Only = EnumSlbVirtServerLayer3Only.enum(kwargs.get('VirtServerLayer3Only', None))
        self.VirtServerState = EnumSlbVirtServerState.enum(kwargs.get('VirtServerState', None))
        self.VirtServerDname = kwargs.get('VirtServerDname', None)
        self.VirtServerBwmContract = kwargs.get('VirtServerBwmContract', None)
        self.VirtServerDelete = EnumSlbVirtServerDelete.enum(kwargs.get('VirtServerDelete', None))
        self.VirtServerWeight = kwargs.get('VirtServerWeight', None)
        self.VirtServerAvail = kwargs.get('VirtServerAvail', None)
        self.VirtServerRule = kwargs.get('VirtServerRule', None)
        self.VirtServerAddRule = kwargs.get('VirtServerAddRule', None)
        self.VirtServerRemoveRule = kwargs.get('VirtServerRemoveRule', None)
        self.VirtServerVname = kwargs.get('VirtServerVname', None)
        self.VirtServerIpVer = EnumSlbVirtServerIpVer.enum(kwargs.get('VirtServerIpVer', None))
        self.VirtServerIpv6Addr = kwargs.get('VirtServerIpv6Addr', None)
        self.VirtServerFreeServiceIdx = kwargs.get('VirtServerFreeServiceIdx', None)
        self.VirtServerCReset = EnumSlbVirtServerCReset.enum(kwargs.get('VirtServerCReset', None))
        self.VirtServerSrcNetwork = kwargs.get('VirtServerSrcNetwork', None)
        self.VirtServerNat = kwargs.get('VirtServerNat', None)
        self.VirtServerNat6 = kwargs.get('VirtServerNat6', None)
        self.VirtServerIsDnsSecVip = EnumSlbVirtServerIsDnsSecVip.enum(kwargs.get('VirtServerIsDnsSecVip', None))

    def get_indexes(self):
        return self.VirtServerIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'VirtServerIndex',

