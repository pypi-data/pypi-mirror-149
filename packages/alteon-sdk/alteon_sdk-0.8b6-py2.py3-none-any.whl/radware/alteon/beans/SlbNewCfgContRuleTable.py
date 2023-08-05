
from radware.sdk.beans_common import *


class EnumSlbContRuleAction(BaseBeanEnum):
    group = 1
    appredir = 2
    discard = 3
    goto = 4


class EnumSlbContRuleState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbContRuleDelete(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewCfgContRuleTable(DeviceBean):
    def __init__(self, **kwargs):
        self.VirtServIndex = kwargs.get('VirtServIndex', None)
        self.VirtServiceIndex = kwargs.get('VirtServiceIndex', None)
        self.Index = kwargs.get('Index', None)
        self.Name = kwargs.get('Name', None)
        self.ContClass = kwargs.get('ContClass', None)
        self.Action = EnumSlbContRuleAction.enum(kwargs.get('Action', None))
        self.RealGrpNum = kwargs.get('RealGrpNum', None)
        self.GotoRuleNum = kwargs.get('GotoRuleNum', None)
        self.Redirection = kwargs.get('Redirection', None)
        self.Copy = kwargs.get('Copy', None)
        self.State = EnumSlbContRuleState.enum(kwargs.get('State', None))
        self.Delete = EnumSlbContRuleDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.VirtServIndex, self.VirtServiceIndex, self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'VirtServIndex', 'VirtServiceIndex', 'Index',

