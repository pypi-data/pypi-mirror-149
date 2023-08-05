
from radware.sdk.beans_common import *


class EnumVADCState(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVADCDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumVADCFeatGlobal(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVADCFeatBWM(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVADCFeatITM(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVADCFeatADOS(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVADCFeatLLB(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVADCStatus(BaseBeanEnum):
    disabled = 0
    init = 1
    running = 2
    down = 3
    stopping = 4
    restarting = 5
    querying = 6


class EnumVADCPreserveDisk(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVADCFeatLP(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVADCFeatIPRep(BaseBeanEnum):
    enabled = 1
    disabled = 0


class EnumVADCFeatURLFilter(BaseBeanEnum):
    enabled = 1
    disabled = 0
    #enabled = 2
    #disabled = 3
    #TODO - mib has been fixed in 32.2.3.50 - need to apply when we update software alteon version in alteon-sdk


class VADCNewCfgTable(DeviceBean):
    def __init__(self, **kwargs):
        self.VADCId = kwargs.get('VADCId', None)
        self.VlanId = kwargs.get('VlanId', None)
        self.AddVlan = kwargs.get('AddVlan', None)
        self.RemoveVlan = kwargs.get('RemoveVlan', None)
        self.Name = kwargs.get('Name', None)
        self.CU = kwargs.get('CU', None)
        self.Limit = kwargs.get('Limit', None)
        self.State = EnumVADCState.enum(kwargs.get('State', None))
        self.Delete = EnumVADCDelete.enum(kwargs.get('Delete', None))
        self.FeatGlobal = EnumVADCFeatGlobal.enum(kwargs.get('FeatGlobal', None))
        self.FeatBWM = EnumVADCFeatBWM.enum(kwargs.get('FeatBWM', None))
        self.FeatITM = EnumVADCFeatITM.enum(kwargs.get('FeatITM', None))
        self.FeatADOS = EnumVADCFeatADOS.enum(kwargs.get('FeatADOS', None))
        self.FeatLLB = EnumVADCFeatLLB.enum(kwargs.get('FeatLLB', None))
        self.SslLimit = kwargs.get('SslLimit', None)
        self.CompLimit = kwargs.get('CompLimit', None)
        self.ResetImageVersion = kwargs.get('ResetImageVersion', None)
        self.SyncPeerSwitch = kwargs.get('SyncPeerSwitch', None)
        self.ApmLimit = kwargs.get('ApmLimit', None)
        self.Status = EnumVADCStatus.enum(kwargs.get('Status', None))
        self.SPcpu = kwargs.get('SPcpu', None)
        self.Throughput = kwargs.get('Throughput', None)
        self.AwCU = kwargs.get('AwCU', None)
        self.WafLimit = kwargs.get('WafLimit', None)
        self.AuthLimit = kwargs.get('AuthLimit', None)
        self.FastviewLimit = kwargs.get('FastviewLimit', None)
        self.FastviewCu = kwargs.get('FastviewCu', None)
        self.TotalCUs = kwargs.get('TotalCUs', None)
        self.PreserveDisk = EnumVADCPreserveDisk.enum(kwargs.get('PreserveDisk', None))
        self.FeatLP = EnumVADCFeatLP.enum(kwargs.get('FeatLP', None))
        self.MPCPU = kwargs.get('MPCPU', None)
        self.FeatIPRep = EnumVADCFeatIPRep.enum(kwargs.get('FeatIPRep', None))
        self.FeatURLFilter = EnumVADCFeatURLFilter.enum(kwargs.get('FeatURLFilter', None))

    def get_indexes(self):
        return self.VADCId,
    
    @classmethod
    def get_index_names(cls):
        return 'VADCId',

