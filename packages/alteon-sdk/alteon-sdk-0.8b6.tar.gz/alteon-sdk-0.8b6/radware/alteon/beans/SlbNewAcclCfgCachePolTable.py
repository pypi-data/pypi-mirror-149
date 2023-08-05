
from radware.sdk.beans_common import *


class EnumSlbAcclCachePolStore(BaseBeanEnum):
    srvrhdr = 1
    cacheall = 2


class EnumSlbAcclCachePolServe(BaseBeanEnum):
    clnthdr = 1
    refresh = 2
    cache = 3


class EnumSlbAcclCachePolQuery(BaseBeanEnum):
    consider = 1
    ignore = 2


class EnumSlbAcclCachePolBrowser(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclCachePolAdminStatus(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclCachePolDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumSlbAcclCachePolCombineCSS(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclCachePolCombineJS(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclCachePolDynamicCache(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclCachePolInlineCSS(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclCachePolInlineJS(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclCachePolImageDim(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclCachePolRemoveCmnt(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclCachePolRemoveWS(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclCachePolTrimURL(BaseBeanEnum):
    enabled = 1
    disabled = 2


class SlbNewAcclCfgCachePolTable(DeviceBean):
    def __init__(self, **kwargs):
        self.NameIdIndex = kwargs.get('NameIdIndex', None)
        self.Name = kwargs.get('Name', None)
        self.ExpireTime = kwargs.get('ExpireTime', None)
        self.MinSize = kwargs.get('MinSize', None)
        self.MaxSize = kwargs.get('MaxSize', None)
        self.URLList = kwargs.get('URLList', None)
        self.Store = EnumSlbAcclCachePolStore.enum(kwargs.get('Store', None))
        self.Serve = EnumSlbAcclCachePolServe.enum(kwargs.get('Serve', None))
        self.Query = EnumSlbAcclCachePolQuery.enum(kwargs.get('Query', None))
        self.Browser = EnumSlbAcclCachePolBrowser.enum(kwargs.get('Browser', None))
        self.AdminStatus = EnumSlbAcclCachePolAdminStatus.enum(kwargs.get('AdminStatus', None))
        self.Delete = EnumSlbAcclCachePolDelete.enum(kwargs.get('Delete', None))
        self.CombineCSS = EnumSlbAcclCachePolCombineCSS.enum(kwargs.get('CombineCSS', None))
        self.CombineJS = EnumSlbAcclCachePolCombineJS.enum(kwargs.get('CombineJS', None))
        self.DynamicCache = EnumSlbAcclCachePolDynamicCache.enum(kwargs.get('DynamicCache', None))
        self.InlineCSS = EnumSlbAcclCachePolInlineCSS.enum(kwargs.get('InlineCSS', None))
        self.InlineJS = EnumSlbAcclCachePolInlineJS.enum(kwargs.get('InlineJS', None))
        self.ImageDim = EnumSlbAcclCachePolImageDim.enum(kwargs.get('ImageDim', None))
        self.RemoveCmnt = EnumSlbAcclCachePolRemoveCmnt.enum(kwargs.get('RemoveCmnt', None))
        self.RemoveWS = EnumSlbAcclCachePolRemoveWS.enum(kwargs.get('RemoveWS', None))
        self.TrimURL = EnumSlbAcclCachePolTrimURL.enum(kwargs.get('TrimURL', None))
        self.OptList = kwargs.get('OptList', None)

    def get_indexes(self):
        return self.NameIdIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'NameIdIndex',

