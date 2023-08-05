
from radware.sdk.beans_common import *


class EnumSlbVirtServiceDummyDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumSlbVirtServiceDirect(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceThash(BaseBeanEnum):
    sip = 1
    sip_sport = 2


class EnumSlbVirtServiceLdapreset(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceLdapslb(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceSip(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceXForwardedFor(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceHttpRedir(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServicePbindRport(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceEgressPip(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceCookieDname(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceWts(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceUhash(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbVirtServiceSdpNat(BaseBeanEnum):
    enabled = 1
    disabled = 2


class SlbNewCfgEnhVirtServicesSixthPartTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ServSixthPartIndex = kwargs.get('ServSixthPartIndex', None)
        self.SixthPartIndex = kwargs.get('SixthPartIndex', None)
        self.Hname = kwargs.get('Hname', None)
        self.Cname = kwargs.get('Cname', None)
        self.CExpire = kwargs.get('CExpire', None)
        self.UrlHashLen = kwargs.get('UrlHashLen', None)
        self.DummyDelete = EnumSlbVirtServiceDummyDelete.enum(kwargs.get('DummyDelete', None))
        self.Direct = EnumSlbVirtServiceDirect.enum(kwargs.get('Direct', None))
        self.Thash = EnumSlbVirtServiceThash.enum(kwargs.get('Thash', None))
        self.Ldapreset = EnumSlbVirtServiceLdapreset.enum(kwargs.get('Ldapreset', None))
        self.Ldapslb = EnumSlbVirtServiceLdapslb.enum(kwargs.get('Ldapslb', None))
        self.Sip = EnumSlbVirtServiceSip.enum(kwargs.get('Sip', None))
        self.XForwardedFor = EnumSlbVirtServiceXForwardedFor.enum(kwargs.get('XForwardedFor', None))
        self.HttpRedir = EnumSlbVirtServiceHttpRedir.enum(kwargs.get('HttpRedir', None))
        self.PbindRport = EnumSlbVirtServicePbindRport.enum(kwargs.get('PbindRport', None))
        self.EgressPip = EnumSlbVirtServiceEgressPip.enum(kwargs.get('EgressPip', None))
        self.CookieDname = EnumSlbVirtServiceCookieDname.enum(kwargs.get('CookieDname', None))
        self.Wts = EnumSlbVirtServiceWts.enum(kwargs.get('Wts', None))
        self.Uhash = EnumSlbVirtServiceUhash.enum(kwargs.get('Uhash', None))
        self.TimeOut = kwargs.get('TimeOut', None)
        self.SdpNat = EnumSlbVirtServiceSdpNat.enum(kwargs.get('SdpNat', None))

    def get_indexes(self):
        return self.ServSixthPartIndex, self.SixthPartIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'ServSixthPartIndex', 'SixthPartIndex',

