
from radware.sdk.beans_common import *


class HwFanSpeedTable(DeviceBean):
    def __init__(self, **kwargs):
        self.SlotIndex = kwargs.get('SlotIndex', None)
        self.SensorIndex = kwargs.get('SensorIndex', None)
        self.Val = kwargs.get('Val', None)

    def get_indexes(self):
        return self.SlotIndex, self.SensorIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'SlotIndex', 'SensorIndex',

