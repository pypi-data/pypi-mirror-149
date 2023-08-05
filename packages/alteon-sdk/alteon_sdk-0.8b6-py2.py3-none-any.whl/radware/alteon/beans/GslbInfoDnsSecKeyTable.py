
from radware.sdk.beans_common import *


class EnumGslbInfoDnsSecKeyStatus(BaseBeanEnum):
    initRollProess = 1
    newKeyCreated = 2
    newZskKeyDeployed = 3
    oldKeyRemoval = 4
    retrDsFromParent = 5
    newKskKeyDeployed = 6
    waitDsChangeOnParent = 7
    rolloverNotRunning = 8
    invalid = 9
    expired = 10


class GslbInfoDnsSecKeyTable(DeviceBean):
    def __init__(self, **kwargs):
        self.ID = kwargs.get('ID', None)
        self.Status = EnumGslbInfoDnsSecKeyStatus.enum(kwargs.get('Status', None))

    def get_indexes(self):
        return self.ID,
    
    @classmethod
    def get_index_names(cls):
        return 'ID',

