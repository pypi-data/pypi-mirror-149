
from radware.sdk.beans_common import *


class EnumSlbSslSSLInspectFlowRuleProxyType(BaseBeanEnum):
    transparent = 1
    expicit = 2


class EnumSlbSslSSLInspectFlowRuleInspectHttp(BaseBeanEnum):
    true = 1
    false = 2


class EnumSlbSslSSLInspectFlowRuleOutboundAction(BaseBeanEnum):
    forward = 1
    nat = 2
    llb = 3


class EnumSlbSslSSLInspectFlowRuleDelete(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewSslCfgSSLInspectFlowRuleTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.ProxyType = EnumSlbSslSSLInspectFlowRuleProxyType.enum(kwargs.get('ProxyType', None))
        self.InspectHttp = EnumSlbSslSSLInspectFlowRuleInspectHttp.enum(kwargs.get('InspectHttp', None))
        self.HttpsPort = kwargs.get('HttpsPort', None)
        self.HttpsDecryptPort = kwargs.get('HttpsDecryptPort', None)
        self.HttpPort = kwargs.get('HttpPort', None)
        self.IngressPort = kwargs.get('IngressPort', None)
        self.EgressPort = kwargs.get('EgressPort', None)
        self.AddIngressPort = kwargs.get('AddIngressPort', None)
        self.AddEgressPort = kwargs.get('AddEgressPort', None)
        self.RemIngressPort = kwargs.get('RemIngressPort', None)
        self.RemEgressPort = kwargs.get('RemEgressPort', None)
        self.OutboundAction = EnumSlbSslSSLInspectFlowRuleOutboundAction.enum(kwargs.get('OutboundAction', None))
        self.FloatId = kwargs.get('FloatId', None)
        self.OutboundFilterHttps = kwargs.get('OutboundFilterHttps', None)
        self.OutboundFilterHttp = kwargs.get('OutboundFilterHttp', None)
        self.BackendFilterHttps = kwargs.get('BackendFilterHttps', None)
        self.BackendFilterHttp = kwargs.get('BackendFilterHttp', None)
        self.NetworkAddr = kwargs.get('NetworkAddr', None)
        self.GWAddr = kwargs.get('GWAddr', None)
        self.NATAddr = kwargs.get('NATAddr', None)
        self.WanLinkGrID = kwargs.get('WanLinkGrID', None)
        self.Delete = EnumSlbSslSSLInspectFlowRuleDelete.enum(kwargs.get('Delete', None))
        self.NATMASKAddr = kwargs.get('NATMASKAddr', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

