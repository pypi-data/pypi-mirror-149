
from radware.sdk.beans_common import *

class EnumSecurityModel(BaseBeanEnum):
    SNMPV1 = 1
    SNMPV2c = 2
    UserBased = 3


class EnumSecurityLevel(BaseBeanEnum):
    NoAuthNoPriv = 1
    AuthNoPriv = 2
    AuthAndPriv = 3

class EnumContextMatch(BaseBeanEnum):
    Exact = 1
    Prefix = 2


class VacmAccessTable(DeviceBean):
    def __init__(self, **kwargs):
        self.GroupName = kwargs.get('GroupName', None)
        self.ContextPrefix = kwargs.get('ContextPrefix', None)
        self.SecurityModel = EnumSecurityModel.enum(kwargs.get('SecurityModel', None))
        self.SecurityLevel = EnumSecurityLevel.enum(kwargs.get('SecurityLevel', None))
        self.ContextMatch = EnumContextMatch.enum(kwargs.get('ContextMatch', None))
        self.ReadViewName = kwargs.get('ReadViewName', None)
        self.WriteViewName = kwargs.get('WriteViewName', None)
        self.NotifyViewName = kwargs.get('NotifyViewName', None)
        self.StorageType = kwargs.get('StorageType', None)
        self.Status = kwargs.get('Status', None)   #RowStatus


    def get_indexes(self):
        return self.GroupName, self.ContextPrefix, self.SecurityModel, self.SecurityLevel,

    @classmethod
    def get_index_names(cls):
        return 'GroupName', 'ContextPrefix', 'SecurityModel', 'SecurityLevel',

