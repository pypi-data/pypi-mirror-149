
from radware.sdk.beans_common import *


class EnumSlbUrlLbPathPatternStringType(BaseBeanEnum):
    ascii = 1
    binary = 2
    none = 3


class EnumSlbUrlLbPathOper(BaseBeanEnum):
    eq = 1
    gt = 2
    lt = 3
    none = 4


class EnumSlbUrlLbPathAllowRegExp(BaseBeanEnum):
    yes = 1
    no = 2


class EnumSlbUrlLbPathDnsType(BaseBeanEnum):
    dns = 1
    dnssec = 2
    any = 3


class EnumSlbUrlLbPathApplication(BaseBeanEnum):
    http = 1
    dns = 2
    other = 3


class EnumSlbUrlLbPathDelete(BaseBeanEnum):
    other = 1
    delete = 2


class SlbNewCfgUrlLbPathTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.String = kwargs.get('String', None)
        self.DnsQueryTypes = kwargs.get('DnsQueryTypes', None)
        self.BwmContract = kwargs.get('BwmContract', None)
        self.HTTPHeader = kwargs.get('HTTPHeader', None)
        self.HTTPHeaderValue = kwargs.get('HTTPHeaderValue', None)
        self.PatternStringType = EnumSlbUrlLbPathPatternStringType.enum(kwargs.get('PatternStringType', None))
        self.Offset = kwargs.get('Offset', None)
        self.Depth = kwargs.get('Depth', None)
        self.Oper = EnumSlbUrlLbPathOper.enum(kwargs.get('Oper', None))
        self.CompleteString = kwargs.get('CompleteString', None)
        self.AllowRegExp = EnumSlbUrlLbPathAllowRegExp.enum(kwargs.get('AllowRegExp', None))
        self.DnsType = EnumSlbUrlLbPathDnsType.enum(kwargs.get('DnsType', None))
        self.Application = EnumSlbUrlLbPathApplication.enum(kwargs.get('Application', None))
        self.Delete = EnumSlbUrlLbPathDelete.enum(kwargs.get('Delete', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

