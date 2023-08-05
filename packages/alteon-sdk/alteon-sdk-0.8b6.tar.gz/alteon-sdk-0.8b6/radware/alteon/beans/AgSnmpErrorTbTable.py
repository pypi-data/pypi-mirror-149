
from radware.sdk.beans_common import *


class EnumAgSnmpErrorTbType(BaseBeanEnum):
    ok = 0
    application = 1
    internalRange = 2
    internalGeneral = 3


class EnumAgSnmpErrorTbStatus(BaseBeanEnum):
    ok = 0
    tooBig = 1
    noSuchName = 2
    badValue = 3
    readOnly = 4
    genErr = 5
    noAccess = 6
    wrongType = 7
    wrongLength = 8
    wrongEncoding = 9
    wrongValue = 10
    noCreation = 11
    inconsitentValue = 12
    resourceUnavailable = 13
    commitFailed = 14
    undoFailed = 15
    authorizationErr = 16
    notWritable = 17
    inconsitentName = 18
    lastErr = 19


class AgSnmpErrorTbTable(DeviceBean):
    def __init__(self, **kwargs):
        self.RequestId = kwargs.get('RequestId', None)
        self.VarId = kwargs.get('VarId', None)
        self.Description = kwargs.get('Description', None)
        self.ErrorIndex = kwargs.get('ErrorIndex', None)
        self.Type = EnumAgSnmpErrorTbType.enum(kwargs.get('Type', None))
        self.Status = EnumAgSnmpErrorTbStatus.enum(kwargs.get('Status', None))
        self.FieldInEntry = kwargs.get('FieldInEntry', None)
        self.Time = kwargs.get('Time', None)
        self.Date = kwargs.get('Date', None)

    def get_indexes(self):
        return self.RequestId,
    
    @classmethod
    def get_index_names(cls):
        return 'RequestId',

