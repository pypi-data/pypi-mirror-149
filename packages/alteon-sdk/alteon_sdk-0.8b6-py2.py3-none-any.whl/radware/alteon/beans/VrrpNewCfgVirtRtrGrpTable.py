
from radware.sdk.beans_common import *


class EnumVrrpVirtRtrGrpPreempt(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpVirtRtrGrpState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpVirtRtrGrpDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumVrrpVirtRtrGrpSharing(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpVirtRtrGrpTckVirtRtr(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpVirtRtrGrpTckIpIntf(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpVirtRtrGrpTckVlanPort(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpVirtRtrGrpTckL4Port(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpVirtRtrGrpTckRServer(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpVirtRtrGrpTckHsrp(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpVirtRtrGrpTckHsrv(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpVirtRtrGrpVersion(BaseBeanEnum):
    v4 = 1
    v6 = 2


class EnumVrrpVirtRtrGrpTckSwExt(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpVirtRtrGrpTckIslPort(BaseBeanEnum):
    include = 1
    exclude = 2


class VrrpNewCfgVirtRtrGrpTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.ID = kwargs.get('ID', None)
        self.IfIndex = kwargs.get('IfIndex', None)
        self.Interval = kwargs.get('Interval', None)
        self.Priority = kwargs.get('Priority', None)
        self.Preempt = EnumVrrpVirtRtrGrpPreempt.enum(kwargs.get('Preempt', None))
        self.State = EnumVrrpVirtRtrGrpState.enum(kwargs.get('State', None))
        self.Delete = EnumVrrpVirtRtrGrpDelete.enum(kwargs.get('Delete', None))
        self.Sharing = EnumVrrpVirtRtrGrpSharing.enum(kwargs.get('Sharing', None))
        self.TckVirtRtr = EnumVrrpVirtRtrGrpTckVirtRtr.enum(kwargs.get('TckVirtRtr', None))
        self.TckIpIntf = EnumVrrpVirtRtrGrpTckIpIntf.enum(kwargs.get('TckIpIntf', None))
        self.TckVlanPort = EnumVrrpVirtRtrGrpTckVlanPort.enum(kwargs.get('TckVlanPort', None))
        self.TckL4Port = EnumVrrpVirtRtrGrpTckL4Port.enum(kwargs.get('TckL4Port', None))
        self.TckRServer = EnumVrrpVirtRtrGrpTckRServer.enum(kwargs.get('TckRServer', None))
        self.TckHsrp = EnumVrrpVirtRtrGrpTckHsrp.enum(kwargs.get('TckHsrp', None))
        self.TckHsrv = EnumVrrpVirtRtrGrpTckHsrv.enum(kwargs.get('TckHsrv', None))
        self.Version = EnumVrrpVirtRtrGrpVersion.enum(kwargs.get('Version', None))
        self.Ipv6Interval = kwargs.get('Ipv6Interval', None)
        self.OspfCost = kwargs.get('OspfCost', None)
        self.TckSwExt = EnumVrrpVirtRtrGrpTckSwExt.enum(kwargs.get('TckSwExt', None))
        self.TckIslPort = EnumVrrpVirtRtrGrpTckIslPort.enum(kwargs.get('TckIslPort', None))

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

