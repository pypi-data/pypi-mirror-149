
from radware.sdk.beans_common import *


class EnumHaTrunkTrunkRemove(BaseBeanEnum):
    other = 1
    delete = 2


class HaTrunkNewCfgTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.TrunkUpCriteria = kwargs.get('TrunkUpCriteria', None)
        self.TrunkRemove = EnumHaTrunkTrunkRemove.enum(kwargs.get('TrunkRemove', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

