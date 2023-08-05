
from radware.sdk.beans_common import *


class EnumMsgProcModel(BaseBeanEnum):
    SNMPv1 = 0
    SNMPv2c = 1
    SNMPv3 = 3


class EnumSecurityModel(BaseBeanEnum):
    SNMPv1 = 1
    SNMPv2c = 2
    UserBased = 3


class EnumSecurityLevel(BaseBeanEnum):
    NoAuthNoPriv = 1
    AuthNoPriv = 2
    AuthPriv = 3


class SnmpTargetParamsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Name = kwargs.get('Name', None)
        self.SecurityName = kwargs.get('SecurityName', None)
        self.MPModel = EnumMsgProcModel.enum(kwargs.get('MPModel', None))
        self.SecurityModel = EnumSecurityModel.enum(kwargs.get('SecurityModel', None))
        self.SecurityLevel = EnumSecurityLevel.enum(kwargs.get('SecurityLevel', None))
        self.StorageType = kwargs.get('StorageType', None)
        self.RowStatus = kwargs.get('RowStatus', None)

    def get_indexes(self):
        return self.Name,
    
    @classmethod
    def get_index_names(cls):
        return 'Name',

