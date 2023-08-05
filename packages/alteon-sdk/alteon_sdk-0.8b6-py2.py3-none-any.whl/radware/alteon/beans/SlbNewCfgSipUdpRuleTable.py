
from radware.sdk.beans_common import *


class EnumSlbSipUdpRuleHdrFld(BaseBeanEnum):
    none = 0
    callid = 1
    contact = 2
    contentlen = 3
    cseq = 4
    expires = 5
    from_ = 6
    replyto = 7
    to = 8
    via = 9
    reqline = 10
    method = 11
    sdpcontent = 12


class EnumSlbSipUdpRuleState(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSipUdpRuleDelete(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewCfgSipUdpRuleTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.HdrFld = EnumSlbSipUdpRuleHdrFld.enum(kwargs.get('HdrFld', None))
        self.Content = kwargs.get('Content', None)
        self.Contract = kwargs.get('Contract', None)
        self.Msg = kwargs.get('Msg', None)
        self.Severity = kwargs.get('Severity', None)
        self.Add = kwargs.get('Add', None)
        self.Rem = kwargs.get('Rem', None)
        self.State = EnumSlbSipUdpRuleState.enum(kwargs.get('State', None))
        self.Delete = EnumSlbSipUdpRuleDelete.enum(kwargs.get('Delete', None))
        self.Bmap = kwargs.get('Bmap', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

