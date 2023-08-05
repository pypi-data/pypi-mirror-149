#!/usr/bin/env python
# Copyright (c) 2019 Radware LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# @author: Leon Meguira, Radware


from radware.sdk.common import RadwareParametersStruct, RadwareParametersExtension
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, AlteonConfigurator
from radware.alteon.beans.SlbNewSslCfgAuthPolTable import *
from radware.sdk.beans_common import *
from typing import Optional, ClassVar


class CertType(RadwareParametersExtension):
    group = 'group'
    cert = 'cert'


class EnumSlbSslAuthPolValidityMethod(BaseBeanEnum):
    none = 0
    ocsp = 1


class SSLServerAuthPolicyParameters(RadwareParametersStruct):
    index: str
    description: Optional[str]
    state: Optional[EnumSlbSslAuthPolAdminStatus]
    ca_chain_lookup_depth: Optional[int]
    cert_validation_method: Optional[EnumSlbSslAuthPolValidityMethod]
    ocsp_validation_static_uri: Optional[str]
    ocsp_uri_priority: Optional[EnumSlbSslAuthPolValidityUriprior]
    ocsp_response_cache_time_second: Optional[int]
    ocsp_response_deviation_time_second: Optional[int]
    ocsp_cert_chain_validation: Optional[EnumSlbSslAuthPolValidityVchain]
    ocsp_response_secure: Optional[EnumSlbSslAuthPolValiditySecure]
    trusted_ca_chain_name: Optional[str]
    trusted_ca_chain_type: Optional[CertType]
    server_expired_cert_action: Optional[EnumSlbSslAuthPolSerCertExp]
    server_host_mismatch_action: Optional[EnumSlbSslAuthPolSerCertMis]
    server_untrusted_cert_action: Optional[EnumSlbSslAuthPolSerCertUntrust]

    def __init__(self, index: str = None):
        self.index = index
        self.description = None
        self.state = None
        self.ca_chain_lookup_depth = None
        self.cert_validation_method = None
        self.ocsp_validation_static_uri = None
        self.ocsp_uri_priority = None
        self.ocsp_response_cache_time_second = None
        self.ocsp_response_deviation_time_second = None
        self.ocsp_cert_chain_validation = None
        self.ocsp_response_secure = None
        self.trusted_ca_chain_name = None
        self.trusted_ca_chain_type = None
        self.server_expired_cert_action = None
        self.server_host_mismatch_action = None
        self.server_untrusted_cert_action = None


bean_map = {
    SlbNewSslCfgAuthPolTable: dict(
        struct=SSLServerAuthPolicyParameters,
        direct=True,
        attrs=dict(
            NameIdIndex='index',
            Name='description',
            AdminStatus='state',
            Cadepth='ca_chain_lookup_depth',
            ValidityMethod='cert_validation_method',
            ValidityStaturi='ocsp_validation_static_uri',
            ValidityUriprior='ocsp_uri_priority',
            ValidityCachtime='ocsp_response_cache_time_second',
            ValidityTimedev='ocsp_response_deviation_time_second',
            ValidityVchain='ocsp_cert_chain_validation',
            ValiditySecure='ocsp_response_secure',
            TrustcaChainName='trusted_ca_chain_name',
            TrustcaChainType='trusted_ca_chain_type',
            SerCertExp='server_expired_cert_action',
            SerCertMis='server_host_mismatch_action',
            SerCertUntrust='server_untrusted_cert_action'
        )
    )
}


class SSLServerAuthPolicyConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[SSLServerAuthPolicyParameters]

    def __init__(self, alteon_connection):
        super(SSLServerAuthPolicyConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: SSLServerAuthPolicyParameters) -> SSLServerAuthPolicyParameters:
        self._read_device_beans(parameters)
        if self._beans:
            parameters.cert_validation_method = EnumSlbSslAuthPolValidityMethod.enum(parameters.cert_validation_method)
            if self._beans[SlbNewSslCfgAuthPolTable].Type == EnumSlbSslAuthPolType.backend:
                return parameters

    def _update(self, parameters: SSLServerAuthPolicyParameters, dry_run: bool) -> str:
        parameters.cert_validation_method = self._enum_to_int(EnumSlbSslAuthPolValidityMethod,
                                                              parameters.cert_validation_method)
        self._write_device_beans(parameters, dry_run=dry_run)
        ssl_auth_pol = self._get_bean_instance(SlbNewSslCfgAuthPolTable, parameters)
        ssl_auth_pol.Type = EnumSlbSslAuthPolType.backend
        self._device_api.update(ssl_auth_pol, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(SlbNewSslCfgAuthPolTable, parameters)

