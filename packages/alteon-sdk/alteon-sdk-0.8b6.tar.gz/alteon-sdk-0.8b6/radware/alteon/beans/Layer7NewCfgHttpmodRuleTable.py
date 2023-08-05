
from radware.sdk.beans_common import *


class EnumLayer7HttpmodRuleDirectn(BaseBeanEnum):
    request = 1
    response = 2
    bidirectional = 3


class EnumLayer7HttpmodRuleAction(BaseBeanEnum):
    insert = 1
    replace = 2
    remove = 3
    none = 4


class EnumLayer7HttpmodRuleAdminStatus(BaseBeanEnum):
    enable = 1
    disable = 2


class EnumLayer7HttpmodRuleDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumLayer7HttpmodRuleElement(BaseBeanEnum):
    url = 1
    header = 2
    cookie = 3
    filetype = 4
    statusline = 5
    text = 6


class EnumLayer7HttpmodRuleHttpBody(BaseBeanEnum):
    include = 1
    exclude = 2


class Layer7NewCfgHttpmodRuleTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ListIdIndex = kwargs.get('ListIdIndex', None)
        self.Index = kwargs.get('Index', None)
        self.Name = kwargs.get('Name', None)
        self.Directn = EnumLayer7HttpmodRuleDirectn.enum(kwargs.get('Directn', None))
        self.Action = EnumLayer7HttpmodRuleAction.enum(kwargs.get('Action', None))
        self.AdminStatus = EnumLayer7HttpmodRuleAdminStatus.enum(kwargs.get('AdminStatus', None))
        self.Copy = kwargs.get('Copy', None)
        self.Delete = EnumLayer7HttpmodRuleDelete.enum(kwargs.get('Delete', None))
        self.Element = EnumLayer7HttpmodRuleElement.enum(kwargs.get('Element', None))
        self.HttpBody = EnumLayer7HttpmodRuleHttpBody.enum(kwargs.get('HttpBody', None))

    def get_indexes(self):
        return self.ListIdIndex, self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'ListIdIndex', 'Index',

