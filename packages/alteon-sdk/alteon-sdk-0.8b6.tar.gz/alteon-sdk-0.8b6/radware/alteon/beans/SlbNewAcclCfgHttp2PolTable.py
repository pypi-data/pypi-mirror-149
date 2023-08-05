
from radware.sdk.beans_common import *


class EnumSlbAcclHttp2PolAdminStatus(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclHttp2PolEnaInsert(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclHttp2PolEnaServerPush(BaseBeanEnum):
    enabled = 1
    disabled = 2


class EnumSlbAcclHttp2PolDelete(BaseBeanEnum):
    other = 1
    delete = 2


class EnumSlbAcclHttp2PolBackendStatus(BaseBeanEnum):
    enabled = 1
    disabled = 2


class SlbNewAcclCfgHttp2PolTable(DeviceBean):
    def __init__(self, **kwargs):
        self.NameIdIndex = kwargs.get('NameIdIndex', None)
        self.Name = kwargs.get('Name', None)
        self.AdminStatus = EnumSlbAcclHttp2PolAdminStatus.enum(kwargs.get('AdminStatus', None))
        self.Streams = kwargs.get('Streams', None)
        self.Idle = kwargs.get('Idle', None)
        self.EnaInsert = EnumSlbAcclHttp2PolEnaInsert.enum(kwargs.get('EnaInsert', None))
        self.Header = kwargs.get('Header', None)
        self.EnaServerPush = EnumSlbAcclHttp2PolEnaServerPush.enum(kwargs.get('EnaServerPush', None))
        self.HpackSize = kwargs.get('HpackSize', None)
        self.Delete = EnumSlbAcclHttp2PolDelete.enum(kwargs.get('Delete', None))
        self.BackendStatus = EnumSlbAcclHttp2PolBackendStatus.enum(kwargs.get('BackendStatus', None))
        self.BackendStreams = kwargs.get('BackendStreams', None)
        self.BackendHpackSize = kwargs.get('BackendHpackSize', None)
        self.BackendServerPush = kwargs.get('BackendServerPush', None)

    def get_indexes(self):
        return self.NameIdIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'NameIdIndex',

