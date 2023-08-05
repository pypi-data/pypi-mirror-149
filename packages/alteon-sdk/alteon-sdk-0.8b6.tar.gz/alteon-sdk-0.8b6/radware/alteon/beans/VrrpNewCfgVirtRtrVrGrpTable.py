
from radware.sdk.beans_common import *


class EnumVrrpVirtRtrVrGrpState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpVirtRtrVrGrpDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumVrrpVirtRtrVrGrpTckIpIntf(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpVirtRtrVrGrpTckVlanPort(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpVirtRtrVrGrpTckL4Port(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpVirtRtrVrGrpTckRServer(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpVirtRtrVrGrpTckHsrp(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpVirtRtrVrGrpTckHsrv(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpVirtRtrVrGrpPreemption(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpVirtRtrVrGrpSharing(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpVirtRtrVrGrpTckSwExt(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumVrrpVirtRtrVrGrpTckIslPort(BaseBeanEnum):
    include = 1
    exclude = 2


class VrrpNewCfgVirtRtrVrGrpTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Indx = kwargs.get('Indx', None)
        self.Name = kwargs.get('Name', None)
        self.Add = kwargs.get('Add', None)
        self.Rem = kwargs.get('Rem', None)
        self.State = EnumVrrpVirtRtrVrGrpState.enum(kwargs.get('State', None))
        self.Delete = EnumVrrpVirtRtrVrGrpDelete.enum(kwargs.get('Delete', None))
        self.Bmap = kwargs.get('Bmap', None)
        self.Priority = kwargs.get('Priority', None)
        self.TckIpIntf = EnumVrrpVirtRtrVrGrpTckIpIntf.enum(kwargs.get('TckIpIntf', None))
        self.TckVlanPort = EnumVrrpVirtRtrVrGrpTckVlanPort.enum(kwargs.get('TckVlanPort', None))
        self.TckL4Port = EnumVrrpVirtRtrVrGrpTckL4Port.enum(kwargs.get('TckL4Port', None))
        self.TckRServer = EnumVrrpVirtRtrVrGrpTckRServer.enum(kwargs.get('TckRServer', None))
        self.TckHsrp = EnumVrrpVirtRtrVrGrpTckHsrp.enum(kwargs.get('TckHsrp', None))
        self.TckHsrv = EnumVrrpVirtRtrVrGrpTckHsrv.enum(kwargs.get('TckHsrv', None))
        self.TckVirtRtrNo = kwargs.get('TckVirtRtrNo', None)
        self.AdverInterval = kwargs.get('AdverInterval', None)
        self.Preemption = EnumVrrpVirtRtrVrGrpPreemption.enum(kwargs.get('Preemption', None))
        self.Sharing = EnumVrrpVirtRtrVrGrpSharing.enum(kwargs.get('Sharing', None))
        self.OspfCost = kwargs.get('OspfCost', None)
        self.TckSwExt = EnumVrrpVirtRtrVrGrpTckSwExt.enum(kwargs.get('TckSwExt', None))
        self.TckIslPort = EnumVrrpVirtRtrVrGrpTckIslPort.enum(kwargs.get('TckIslPort', None))

    def get_indexes(self):
        return self.Indx,
    
    @classmethod
    def get_index_names(cls):
        return 'Indx',

