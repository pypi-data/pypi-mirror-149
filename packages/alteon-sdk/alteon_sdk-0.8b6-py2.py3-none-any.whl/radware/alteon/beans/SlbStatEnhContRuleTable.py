
from radware.sdk.beans_common import *


class EnumSlbStatContRuleAction(BaseBeanEnum):
    group = 1
    appredir = 2
    discard = 3
    goto = 4


class SlbStatEnhContRuleTable(DeviceBean):
    def __init__(self, **kwargs):
        self.VirtServIndex = kwargs.get('VirtServIndex', None)
        self.VirtServiceIndex = kwargs.get('VirtServiceIndex', None)
        self.Index = kwargs.get('Index', None)
        self.Name = kwargs.get('Name', None)
        self.ContClass = kwargs.get('ContClass', None)
        self.Action = EnumSlbStatContRuleAction.enum(kwargs.get('Action', None))
        self.CurrSess = kwargs.get('CurrSess', None)
        self.TotSess = kwargs.get('TotSess', None)
        self.HighSess = kwargs.get('HighSess', None)
        self.TotOcts = kwargs.get('TotOcts', None)

    def get_indexes(self):
        return self.VirtServIndex, self.VirtServiceIndex, self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'VirtServIndex', 'VirtServiceIndex', 'Index',

