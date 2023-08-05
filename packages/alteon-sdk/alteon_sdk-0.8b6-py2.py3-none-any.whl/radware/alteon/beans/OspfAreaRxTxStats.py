
from radware.sdk.beans_common import *


class OspfAreaRxTxStats(DeviceBean):
    def __init__(self, **kwargs):
        self.Index = kwargs.get('Index', None)
        self.Pkts = kwargs.get('Pkts', None)
        self.TxPkts = kwargs.get('TxPkts', None)
        self.Hello = kwargs.get('Hello', None)
        self.TxHello = kwargs.get('TxHello', None)
        self.Database = kwargs.get('Database', None)
        self.TxDatabase = kwargs.get('TxDatabase', None)
        self.RxlsReqs = kwargs.get('RxlsReqs', None)
        self.TxlsReqs = kwargs.get('TxlsReqs', None)
        self.RxlsAcks = kwargs.get('RxlsAcks', None)
        self.TxlsAcks = kwargs.get('TxlsAcks', None)
        self.RxlsUpdates = kwargs.get('RxlsUpdates', None)
        self.TxlsUpdates = kwargs.get('TxlsUpdates', None)

    def get_indexes(self):
        return self.Index,
    
    @classmethod
    def get_index_names(cls):
        return 'Index',

