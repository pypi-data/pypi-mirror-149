
from radware.sdk.beans_common import *


class EnumSlbStatContRuleActionGroupRealStatus(BaseBeanEnum):
    up = 0
    down = 1
    admindown = 2
    warning = 3
    shutdown = 4
    error = 5


class SlbStatEnhContRuleActionGroupTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ActionVirtServIndex = kwargs.get('ActionVirtServIndex', None)
        self.ActionVirtServiceIndex = kwargs.get('ActionVirtServiceIndex', None)
        self.Index = kwargs.get('Index', None)
        self.EnhContActionRealServerIndex = kwargs.get('EnhContActionRealServerIndex', None)
        self.CurrSess = kwargs.get('CurrSess', None)
        self.TotSess = kwargs.get('TotSess', None)
        self.HighSess = kwargs.get('HighSess', None)
        self.TotOcts = kwargs.get('TotOcts', None)
        self.RealStatus = EnumSlbStatContRuleActionGroupRealStatus.enum(kwargs.get('RealStatus', None))
        self.HcReason = kwargs.get('HcReason', None)

    def get_indexes(self):
        return self.ActionVirtServIndex, self.ActionVirtServiceIndex, self.Index, self.EnhContActionRealServerIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'ActionVirtServIndex', 'ActionVirtServiceIndex', 'Index', 'EnhContActionRealServerIndex',

