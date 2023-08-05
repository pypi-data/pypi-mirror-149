
from radware.sdk.beans_common import *


class EnumOspfv3IfInfoAdminStat(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumOspfv3IfInfoIfState(BaseBeanEnum):
    unkn = 0
    down = 1
    lpbk = 2
    wtng = 3
    ppp = 4
    dr = 5
    bdr = 6
    other = 7


class Ospfv3IfInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Vlan = kwargs.get('Vlan', None)
        self.AreaID = kwargs.get('AreaID', None)
        self.AdminStat = EnumOspfv3IfInfoAdminStat.enum(kwargs.get('AdminStat', None))
        self.Prio = kwargs.get('Prio', None)
        self.TransitDelay = kwargs.get('TransitDelay', None)
        self.RetransInterval = kwargs.get('RetransInterval', None)
        self.RtrDeadInterval = kwargs.get('RtrDeadInterval', None)
        self.HelloInterval = kwargs.get('HelloInterval', None)
        self.PollInterval = kwargs.get('PollInterval', None)
        self.Cost = kwargs.get('Cost', None)
        self.Drid = kwargs.get('Drid', None)
        self.Bdrid = kwargs.get('Bdrid', None)
        self.IfState = EnumOspfv3IfInfoIfState.enum(kwargs.get('IfState', None))

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

