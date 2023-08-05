
from radware.sdk.beans_common import *


class EnumSlbSecSecPolAdminStatus(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSecSecPolDel(BaseBeanEnum):
    other = 1
    delete = 2
    delWithAssociations = 3


class SlbNewSecCfgSecPolTable(DeviceBean):
    def __init__(self, **kwargs):
        self.NameIdIndex = kwargs.get('NameIdIndex', None)
        self.Name = kwargs.get('Name', None)
        self.BW = kwargs.get('BW', None)
        self.BWmin = kwargs.get('BWmin', None)
        self.BWin = kwargs.get('BWin', None)
        self.PPS = kwargs.get('PPS', None)
        self.PPSmin = kwargs.get('PPSmin', None)
        self.PPSin = kwargs.get('PPSin', None)
        self.CPS = kwargs.get('CPS', None)
        self.CPSmin = kwargs.get('CPSmin', None)
        self.CPSin = kwargs.get('CPSin', None)
        self.CEC = kwargs.get('CEC', None)
        self.CECmin = kwargs.get('CECmin', None)
        self.CECin = kwargs.get('CECin', None)
        self.LearnPeriod = kwargs.get('LearnPeriod', None)
        self.AdminStatus = EnumSlbSecSecPolAdminStatus.enum(kwargs.get('AdminStatus', None))
        self.Del = EnumSlbSecSecPolDel.enum(kwargs.get('Del', None))
        self.LatencyAbs = kwargs.get('LatencyAbs', None)
        self.LatencyPercent = kwargs.get('LatencyPercent', None)
        self.LatencyMin = kwargs.get('LatencyMin', None)

    def get_indexes(self):
        return self.NameIdIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'NameIdIndex',

