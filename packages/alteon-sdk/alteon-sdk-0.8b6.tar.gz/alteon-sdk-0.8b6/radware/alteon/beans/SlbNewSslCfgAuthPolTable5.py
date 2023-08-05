
from radware.sdk.beans_common import *


class EnumSlbSslAuthPolTable5AdminStatus(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbSslAuthPolTable5Delete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumSlbSslAuthPolTable5PassinfoComp2424(BaseBeanEnum):
    enabled = 1
    disabled = 2


class SlbNewSslCfgAuthPolTable5(DeviceBean):
    def __init__(self, **kwargs):
        self.NameIdIndex = kwargs.get('NameIdIndex', None)
        self.Cadepth = kwargs.get('Cadepth', None)
        self.Caverify = kwargs.get('Caverify', None)
        self.Failurl = kwargs.get('Failurl', None)
        self.AdminStatus = EnumSlbSslAuthPolTable5AdminStatus.enum(kwargs.get('AdminStatus', None))
        self.Delete = EnumSlbSslAuthPolTable5Delete.enum(kwargs.get('Delete', None))
        self.PassinfoComp2424 = EnumSlbSslAuthPolTable5PassinfoComp2424.enum(kwargs.get('PassinfoComp2424', None))

    def get_indexes(self):
        return self.NameIdIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'NameIdIndex',

