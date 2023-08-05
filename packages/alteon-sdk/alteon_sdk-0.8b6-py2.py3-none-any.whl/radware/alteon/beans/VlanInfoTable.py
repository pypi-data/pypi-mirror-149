
from radware.sdk.beans_common import *


class EnumVlanInfoStatus(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVlanInfoJumbo(BaseBeanEnum):
    enabled = 2
    disabled = 3


class EnumVlanInfoLearn(BaseBeanEnum):
    enabled = 2
    disabled = 3


class VlanInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Id = kwargs.get('Id', None)
        self.Name = kwargs.get('Name', None)
        self.Status = EnumVlanInfoStatus.enum(kwargs.get('Status', None))
        self.Jumbo = EnumVlanInfoJumbo.enum(kwargs.get('Jumbo', None))
        self.BwmContract = kwargs.get('BwmContract', None)
        self.Learn = EnumVlanInfoLearn.enum(kwargs.get('Learn', None))
        self.Ports = kwargs.get('Ports', None)

    def get_indexes(self):
        return self.Id,
    
    @classmethod
    def get_index_names(cls):
        return 'Id',

