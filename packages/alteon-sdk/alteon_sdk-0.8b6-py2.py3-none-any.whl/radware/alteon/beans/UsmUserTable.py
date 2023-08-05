
from radware.sdk.beans_common import *

class EnumAuthProtocol(BaseBeanEnum):
    NONE = 1
    MD5 = 2
    SHA = 3
    SHA256 = 4


class EnumPrivProtocol(BaseBeanEnum):
    NONE = 1
    DES = 2
    AES128 = 3
    AES256 = 4


class UsmUserTable(DeviceBean):
    def __init__(self, **kwargs):
        self.EngineID = kwargs.get('EngineID', None)
        self.Name = kwargs.get('Name', None)
        self.SecurityName = kwargs.get('SecurityName', None)
        self.CloneFrom = kwargs.get('CloneFrom', None)
        self.AuthProtocol = EnumAuthProtocol.enum(kwargs.get('AuthProtocol', None))
        self.AuthKeyChange = kwargs.get('AuthKeyChange', None)
        self.OwnAuthKeyChange = kwargs.get('OwnAuthKeyChange', None)
        self.PrivProtocol = EnumPrivProtocol.enum(kwargs.get('PrivProtocol', None))
        self.PrivKeyChange = kwargs.get('PrivKeyChange', None)
        self.OwnPrivKeyChange = kwargs.get('OwnPrivKeyChange', None)
        self.Public = kwargs.get('Public', None)
        self.StorageType = kwargs.get('StorageType', None)
        self.Status = kwargs.get('Status', None)   #RowStatus


    def get_indexes(self):
        return self.EngineID, self.Name,

    @classmethod
    def get_index_names(cls):
        return 'EngineID', 'Name',

