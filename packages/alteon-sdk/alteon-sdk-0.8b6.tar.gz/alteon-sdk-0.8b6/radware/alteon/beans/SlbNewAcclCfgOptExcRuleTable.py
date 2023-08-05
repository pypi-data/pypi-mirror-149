
from radware.sdk.beans_common import *


class EnumSlbAcclOptExcRuleResType(BaseBeanEnum):
    html = 1
    js = 2
    css = 3
    image = 4
    other = 5


class EnumSlbAcclOptExcRuleCombineCSS(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclOptExcRuleCombineJS(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclOptExcRuleDynamicCache(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclOptExcRuleInlineCSS(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclOptExcRuleInlineJS(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclOptExcRuleImageDim(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclOptExcRuleRemoveComments(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclOptExcRuleRemoveWS(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclOptExcRuleTrimURL(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclOptExcRuleAdminStatus(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclOptExcRuleDelete(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewAcclCfgOptExcRuleTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ListIdIndex = kwargs.get('ListIdIndex', None)
        self.Index = kwargs.get('Index', None)
        self.Name = kwargs.get('Name', None)
        self.ResType = EnumSlbAcclOptExcRuleResType.enum(kwargs.get('ResType', None))
        self.URI = kwargs.get('URI', None)
        self.CombineCSS = EnumSlbAcclOptExcRuleCombineCSS.enum(kwargs.get('CombineCSS', None))
        self.CombineJS = EnumSlbAcclOptExcRuleCombineJS.enum(kwargs.get('CombineJS', None))
        self.DynamicCache = EnumSlbAcclOptExcRuleDynamicCache.enum(kwargs.get('DynamicCache', None))
        self.InlineCSS = EnumSlbAcclOptExcRuleInlineCSS.enum(kwargs.get('InlineCSS', None))
        self.InlineJS = EnumSlbAcclOptExcRuleInlineJS.enum(kwargs.get('InlineJS', None))
        self.ImageDim = EnumSlbAcclOptExcRuleImageDim.enum(kwargs.get('ImageDim', None))
        self.RemoveComments = EnumSlbAcclOptExcRuleRemoveComments.enum(kwargs.get('RemoveComments', None))
        self.RemoveWS = EnumSlbAcclOptExcRuleRemoveWS.enum(kwargs.get('RemoveWS', None))
        self.TrimURL = EnumSlbAcclOptExcRuleTrimURL.enum(kwargs.get('TrimURL', None))
        self.AdminStatus = EnumSlbAcclOptExcRuleAdminStatus.enum(kwargs.get('AdminStatus', None))
        self.Delete = EnumSlbAcclOptExcRuleDelete.enum(kwargs.get('Delete', None))
        self.Copy = kwargs.get('Copy', None)

    def get_indexes(self):
        return self.ListIdIndex, self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'ListIdIndex', 'Index',

