
from radware.sdk.beans_common import *


class EnumOspfv3AreaInfoImportAsExtern(BaseBeanEnum):
    importExternal = 0
    importNoExternal = 1
    importNssa = 2


class Ospfv3AreaInfoTable(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.ID = kwargs.get('ID', None)
        self.ImportAsExtern = EnumOspfv3AreaInfoImportAsExtern.enum(kwargs.get('ImportAsExtern', None))
        self.SPF = kwargs.get('SPF', None)
        self.ABRs = kwargs.get('ABRs', None)
        self.ASBRs = kwargs.get('ASBRs', None)
        self.LSAS = kwargs.get('LSAS', None)
        self.Summary = kwargs.get('Summary', None)
        self.StubMetric = kwargs.get('StubMetric', None)
        self.AreaTableCounter = kwargs.get('AreaTableCounter', None)
        self.AreaLSDBTabletCounter = kwargs.get('AreaLSDBTabletCounter', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

