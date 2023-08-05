
from radware.sdk.beans_common import *


class EnumHwTempInfoSensorStatus(BaseBeanEnum):
    low = 1
    normal = 2
    high = 3
    critical = 4


class HwTemperatureInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.TempInfoSlotIndex = kwargs.get('TempInfoSlotIndex', None)
        self.TempInfoSensorIndex = kwargs.get('TempInfoSensorIndex', None)
        self.TempInfoSensorStatus = EnumHwTempInfoSensorStatus.enum(kwargs.get('TempInfoSensorStatus', None))
        self.TempInfoSensorTemp = kwargs.get('TempInfoSensorTemp', None)
        self.TempInfoSensorStr = kwargs.get('TempInfoSensorStr', None)

    def get_indexes(self):
        return self.TempInfoSlotIndex, self.TempInfoSensorIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'TempInfoSlotIndex', 'TempInfoSensorIndex',

