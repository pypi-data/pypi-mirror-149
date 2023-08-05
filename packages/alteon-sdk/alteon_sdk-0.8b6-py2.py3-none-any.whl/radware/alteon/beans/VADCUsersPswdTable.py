
from radware.sdk.beans_common import *


class VADCUsersPswdTable(DeviceBean):
    def __init__(self, **kwargs):
        self.VADCId = kwargs.get('VADCId', None)
        self.vADCAccessUsrPasswd = kwargs.get('vADCAccessUsrPasswd', None)
        self.vADCAccessSlbOperPasswd = kwargs.get('vADCAccessSlbOperPasswd', None)
        self.vADCAccessL4OperPasswd = kwargs.get('vADCAccessL4OperPasswd', None)
        self.vADCAccessOperPasswd = kwargs.get('vADCAccessOperPasswd', None)
        self.vADCAccessSlbAdminPasswd = kwargs.get('vADCAccessSlbAdminPasswd', None)
        self.vADCAccessL4AdminPasswd = kwargs.get('vADCAccessL4AdminPasswd', None)
        self.vADCAccessAdminPasswd = kwargs.get('vADCAccessAdminPasswd', None)
        self.vADCAccessAdminNewPasswd = kwargs.get('vADCAccessAdminNewPasswd', None)
        self.vADCAccessAdminConfNewPasswd = kwargs.get('vADCAccessAdminConfNewPasswd', None)
        self.vADCAccessSlbViewerPasswd = kwargs.get('vADCAccessSlbViewerPasswd', None)
        self.vADCAccessWsAdminPasswd = kwargs.get('vADCAccessWsAdminPasswd', None)

    def get_indexes(self):
        return self.VADCId,
    
    @classmethod
    def get_index_names(cls):
        return 'VADCId',

