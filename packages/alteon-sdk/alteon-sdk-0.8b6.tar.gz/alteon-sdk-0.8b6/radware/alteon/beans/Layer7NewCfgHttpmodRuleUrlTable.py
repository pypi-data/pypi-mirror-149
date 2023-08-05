
from radware.sdk.beans_common import *


class EnumLayer7HttpmodRuleUrlMtchProtcol(BaseBeanEnum):
    http = 1
    https = 2


class EnumLayer7HttpmodRuleUrlMtchHostTyp(BaseBeanEnum):
    suffix = 1
    prefix = 2
    equal = 3
    include = 4
    any = 5


class EnumLayer7HttpmodRuleUrlMtchPathTyp(BaseBeanEnum):
    suffix = 1
    prefix = 2
    equal = 3
    include = 4
    any = 5


class EnumLayer7HttpmodRuleUrlActnProtcl(BaseBeanEnum):
    http = 1
    https = 2


class EnumLayer7HttpmodRuleUrlActnHostTyp(BaseBeanEnum):
    insert = 1
    replace = 2
    remove = 3
    none = 4


class EnumLayer7HttpmodRuleUrlActnHstSec(BaseBeanEnum):
    before = 1
    after = 2


class EnumLayer7HttpmodRuleUrlActnPathTyp(BaseBeanEnum):
    insert = 1
    replace = 2
    remove = 3
    none = 4


class EnumLayer7HttpmodRuleUrlActnPthSctn(BaseBeanEnum):
    before = 1
    after = 2


class Layer7NewCfgHttpmodRuleUrlTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ListIdIndex = kwargs.get('ListIdIndex', None)
        self.Index = kwargs.get('Index', None)
        self.MtchProtcol = EnumLayer7HttpmodRuleUrlMtchProtcol.enum(kwargs.get('MtchProtcol', None))
        self.MtchPort = kwargs.get('MtchPort', None)
        self.MtchHostTyp = EnumLayer7HttpmodRuleUrlMtchHostTyp.enum(kwargs.get('MtchHostTyp', None))
        self.MtchHost = kwargs.get('MtchHost', None)
        self.MtchPathTyp = EnumLayer7HttpmodRuleUrlMtchPathTyp.enum(kwargs.get('MtchPathTyp', None))
        self.MtchPath = kwargs.get('MtchPath', None)
        self.MtchPgName = kwargs.get('MtchPgName', None)
        self.MtchPgTyp = kwargs.get('MtchPgTyp', None)
        self.ActnProtcl = EnumLayer7HttpmodRuleUrlActnProtcl.enum(kwargs.get('ActnProtcl', None))
        self.ActnPort = kwargs.get('ActnPort', None)
        self.ActnHostTyp = EnumLayer7HttpmodRuleUrlActnHostTyp.enum(kwargs.get('ActnHostTyp', None))
        self.ActnHost = kwargs.get('ActnHost', None)
        self.ActnHstSec = EnumLayer7HttpmodRuleUrlActnHstSec.enum(kwargs.get('ActnHstSec', None))
        self.ActnHstRplc = kwargs.get('ActnHstRplc', None)
        self.ActnPathTyp = EnumLayer7HttpmodRuleUrlActnPathTyp.enum(kwargs.get('ActnPathTyp', None))
        self.ActnPath = kwargs.get('ActnPath', None)
        self.ActnPthSctn = EnumLayer7HttpmodRuleUrlActnPthSctn.enum(kwargs.get('ActnPthSctn', None))
        self.ActnPthRplc = kwargs.get('ActnPthRplc', None)
        self.ActnPgName = kwargs.get('ActnPgName', None)
        self.ActnPgTyp = kwargs.get('ActnPgTyp', None)

    def get_indexes(self):
        return self.ListIdIndex, self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'ListIdIndex', 'Index',

