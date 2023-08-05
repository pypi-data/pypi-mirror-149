
from radware.sdk.beans_common import *


class EnumSlbVirtSpecificServicesInfoStatus(BaseBeanEnum):
    up = 0
    down = 1
    admindown = 2
    warning = 3
    shudown = 4


class SlbEnhVirtSpecificServicesInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.VirtServIndex = kwargs.get('VirtServIndex', None)
        self.SvcIndex = kwargs.get('SvcIndex', None)
        self.Status = EnumSlbVirtSpecificServicesInfoStatus.enum(kwargs.get('Status', None))

    def get_indexes(self):
        return self.ServicesInfoVirtServIndex, self.ServicesInfoSvcIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'ServicesInfoVirtServIndex', 'ServicesInfoSvcIndex',

