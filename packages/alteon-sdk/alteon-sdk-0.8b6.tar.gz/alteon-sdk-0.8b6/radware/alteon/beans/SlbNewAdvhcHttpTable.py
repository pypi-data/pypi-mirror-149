
from radware.sdk.beans_common import *


class EnumSlbAdvhcHttpMethod(BaseBeanEnum):
    get = 1
    post = 2
    head = 3


class EnumSlbAdvhcHttpAuthLevel(BaseBeanEnum):
    none = 1
    basic = 2
    ntlm2 = 3
    ntlmssp = 4


class EnumSlbAdvhcHttpResponseType(BaseBeanEnum):
    none = 1
    incl = 2
    excl = 4


class EnumSlbAdvhcHttpOverloadType(BaseBeanEnum):
    none = 1
    incl = 2


class EnumSlbAdvhcHttpConnTerm(BaseBeanEnum):
    fin = 1
    rst = 2


class EnumSlbAdvhcHttpHttpsCipherName(BaseBeanEnum):
    userDefined = 1
    low = 2
    medium = 3
    high = 4


class SlbNewAdvhcHttpTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ID = kwargs.get('ID', None)
        self.Name = kwargs.get('Name', None)
        self.DPort = kwargs.get('DPort', None)
        self.IPVer = kwargs.get('IPVer', None)
        self.HostName = kwargs.get('HostName', None)
        self.Transparent = kwargs.get('Transparent', None)
        self.Interval = kwargs.get('Interval', None)
        self.Retries = kwargs.get('Retries', None)
        self.RestoreRetries = kwargs.get('RestoreRetries', None)
        self.Timeout = kwargs.get('Timeout', None)
        self.Overflow = kwargs.get('Overflow', None)
        self.DownInterval = kwargs.get('DownInterval', None)
        self.Invert = kwargs.get('Invert', None)
        self.Https = kwargs.get('Https', None)
        self.Host = kwargs.get('Host', None)
        self.Path = kwargs.get('Path', None)
        self.Method = EnumSlbAdvhcHttpMethod.enum(kwargs.get('Method', None))
        self.Headers = kwargs.get('Headers', None)
        self.Body = kwargs.get('Body', None)
        self.AuthLevel = EnumSlbAdvhcHttpAuthLevel.enum(kwargs.get('AuthLevel', None))
        self.UserName = kwargs.get('UserName', None)
        self.Password = kwargs.get('Password', None)
        self.ResponseType = EnumSlbAdvhcHttpResponseType.enum(kwargs.get('ResponseType', None))
        self.OverloadType = EnumSlbAdvhcHttpOverloadType.enum(kwargs.get('OverloadType', None))
        self.ResponseCode = kwargs.get('ResponseCode', None)
        self.ReceiveString = kwargs.get('ReceiveString', None)
        self.ResponseCodeOverload = kwargs.get('ResponseCodeOverload', None)
        self.OverloadString = kwargs.get('OverloadString', None)
        self.Copy = kwargs.get('Copy', None)
        self.Delete = kwargs.get('Delete', None)
        self.Proxy = kwargs.get('Proxy', None)
        self.ConnTerm = EnumSlbAdvhcHttpConnTerm.enum(kwargs.get('ConnTerm', None))
        self.HttpsCipherName = EnumSlbAdvhcHttpHttpsCipherName.enum(kwargs.get('HttpsCipherName', None))
        self.HttpsCipherUserdef = kwargs.get('HttpsCipherUserdef', None)
        self.Http2 = kwargs.get('Http2', None)
        self.Always = kwargs.get('Always', None)

    def get_indexes(self):
        return self.ID,
    
    @classmethod
    def get_index_names(cls):
        return 'ID',

