
from radware.sdk.beans_common import *


class EnumVrrpVirtRtrPreempt(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpVirtRtrState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpVirtRtrDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumVrrpVirtRtrSharing(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpVirtRtrTckVirtRtr(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpVirtRtrTckIpIntf(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpVirtRtrTckVlanPort(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpVirtRtrTckL4Port(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpVirtRtrTckRServer(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpVirtRtrTckHsrp(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpVirtRtrTckHsrv(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpVirtRtrVersion(BaseBeanEnum):
    v4 = 1
    v6 = 2


class EnumVrrpVirtRtrTckSwExt(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpVirtRtrTckIslPort(BaseBeanEnum):
    include = 1
    exclude = 2


class VrrpNewCfgVirtRtrTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.ID = kwargs.get('ID', None)
        self.Addr = kwargs.get('Addr', None)
        self.IfIndex = kwargs.get('IfIndex', None)
        self.Interval = kwargs.get('Interval', None)
        self.Priority = kwargs.get('Priority', None)
        self.Preempt = EnumVrrpVirtRtrPreempt.enum(kwargs.get('Preempt', None))
        self.State = EnumVrrpVirtRtrState.enum(kwargs.get('State', None))
        self.Delete = EnumVrrpVirtRtrDelete.enum(kwargs.get('Delete', None))
        self.Sharing = EnumVrrpVirtRtrSharing.enum(kwargs.get('Sharing', None))
        self.TckVirtRtr = EnumVrrpVirtRtrTckVirtRtr.enum(kwargs.get('TckVirtRtr', None))
        self.TckIpIntf = EnumVrrpVirtRtrTckIpIntf.enum(kwargs.get('TckIpIntf', None))
        self.TckVlanPort = EnumVrrpVirtRtrTckVlanPort.enum(kwargs.get('TckVlanPort', None))
        self.TckL4Port = EnumVrrpVirtRtrTckL4Port.enum(kwargs.get('TckL4Port', None))
        self.TckRServer = EnumVrrpVirtRtrTckRServer.enum(kwargs.get('TckRServer', None))
        self.TckHsrp = EnumVrrpVirtRtrTckHsrp.enum(kwargs.get('TckHsrp', None))
        self.TckHsrv = EnumVrrpVirtRtrTckHsrv.enum(kwargs.get('TckHsrv', None))
        self.Version = EnumVrrpVirtRtrVersion.enum(kwargs.get('Version', None))
        self.Ipv6Addr = kwargs.get('Ipv6Addr', None)
        self.Ipv6Interval = kwargs.get('Ipv6Interval', None)
        self.OspfCost = kwargs.get('OspfCost', None)
        self.TckSwExt = EnumVrrpVirtRtrTckSwExt.enum(kwargs.get('TckSwExt', None))
        self.TckIslPort = EnumVrrpVirtRtrTckIslPort.enum(kwargs.get('TckIslPort', None))

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

