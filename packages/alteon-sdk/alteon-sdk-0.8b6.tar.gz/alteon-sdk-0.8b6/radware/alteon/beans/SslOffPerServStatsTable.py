
from radware.sdk.beans_common import *


class SslOffPerServStatsTable(DeviceBean):
    def __init__(self, **kwargs):
        self.VirtServIndex = kwargs.get('VirtServIndex', None)
        self.VirtServiceIndex = kwargs.get('VirtServiceIndex', None)
        self.VirtServPort = kwargs.get('VirtServPort', None)
        self.SslPolId = kwargs.get('SslPolId', None)
        self.NewhandShake = kwargs.get('NewhandShake', None)
        self.ReusedhandShake = kwargs.get('ReusedhandShake', None)
        self.PercReusedhandShake = kwargs.get('PercReusedhandShake', None)
        self.SessUsingSSLv2 = kwargs.get('SessUsingSSLv2', None)
        self.SessUsingSSLv3 = kwargs.get('SessUsingSSLv3', None)
        self.SessUsingTLS = kwargs.get('SessUsingTLS', None)
        self.SessUsingTLS11 = kwargs.get('SessUsingTLS11', None)
        self.SessUsingTLS12 = kwargs.get('SessUsingTLS12', None)
        self.RejectedhandShake = kwargs.get('RejectedhandShake', None)
        self.ByCipherHandShake = kwargs.get('ByCipherHandShake', None)
        self.RejectedCertificates = kwargs.get('RejectedCertificates', None)
        self.IgnoredCertificates = kwargs.get('IgnoredCertificates', None)
        self.ExpiredCertificates = kwargs.get('ExpiredCertificates', None)
        self.UntrustedCertificates = kwargs.get('UntrustedCertificates', None)
        self.CertificateHostnameMismatches = kwargs.get('CertificateHostnameMismatches', None)

    def get_indexes(self):
        return self.VirtServIndex, self.VirtServiceIndex,
    
    @classmethod
    def get_index_names(cls):
        return 'VirtServIndex', 'VirtServiceIndex',

