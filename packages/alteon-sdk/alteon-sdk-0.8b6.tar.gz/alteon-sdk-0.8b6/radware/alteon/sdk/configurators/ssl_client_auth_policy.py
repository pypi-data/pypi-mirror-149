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


class AdvertisedCACertType(RadwareParametersExtension):
    group = 'group'
    cert = 'cert'
    default = 'default'
    none = 'none'


class EnumSlbSslAuthPolValidityMethod(BaseBeanEnum):
    none = 0
    ocsp = 1


class EnumSlbSslAuthPolCaverify(BaseBeanEnum):
    none = 0
    optional = 1
    require = 2


class SSLClientAuthPolicyParameters(RadwareParametersStruct):
    index: str
    description: Optional[str]
    state: Optional[EnumSlbSslAuthPolAdminStatus]
    ca_chain_lookup_depth: Optional[int]
    ca_verification: Optional[EnumSlbSslAuthPolCaverify]
    failure_redirection_url: Optional[str]
    trusted_ca_chain_name: Optional[str]
    trusted_ca_chain_type: Optional[CertType]
    advertised_ca_chain_name: Optional[str]
    advertised_ca_chain_type: Optional[AdvertisedCACertType]
    cert_validation_method: Optional[EnumSlbSslAuthPolValidityMethod]
    ocsp_validation_static_uri: Optional[str]
    ocsp_uri_priority: Optional[EnumSlbSslAuthPolValidityUriprior]
    ocsp_response_cache_time_second: Optional[int]
    ocsp_response_deviation_time_second: Optional[int]
    ocsp_cert_chain_validation: Optional[EnumSlbSslAuthPolValidityVchain]
    ocsp_response_secure: Optional[EnumSlbSslAuthPolValiditySecure]
    pass_cert_info_version_header_name: Optional[str]
    pass_cert_info_version_header: Optional[EnumSlbSslAuthPolPassinfoVersionFlag]
    pass_cert_info_serial_number_header_name: Optional[str]
    pass_cert_info_serial_number_header: Optional[EnumSlbSslAuthPolPassinfoSerialFlag]
    pass_cert_info_sign_algorithm_header_name: Optional[str]
    pass_cert_info_sign_algorithm_header: Optional[EnumSlbSslAuthPolPassinfoAlgoFlag]
    pass_cert_info_issuer_header_name: Optional[str]
    pass_cert_info_issuer_header: Optional[EnumSlbSslAuthPolPassinfoIssuerFlag]
    pass_cert_info_not_before_header_name: Optional[str]
    pass_cert_info_not_before_header: Optional[EnumSlbSslAuthPolPassinfoNbeforeFlag]
    pass_cert_info_not_after_header_name: Optional[str]
    pass_cert_info_not_after_header: Optional[EnumSlbSslAuthPolPassinfoNafterFlag]
    pass_cert_info_subject_header_name: Optional[str]
    pass_cert_info_subject_header: Optional[EnumSlbSslAuthPolPassinfoSubjectFlag]
    pass_cert_info_public_key_type_header_name: Optional[str]
    pass_cert_info_public_key_type_header: Optional[EnumSlbSslAuthPolPassinfoKeytypeFlag]
    pass_cert_info_md5_header_name: Optional[str]
    pass_cert_info_md5_header: Optional[EnumSlbSslAuthPolPassinfoMd5Flag]
    pass_cert_info_cert_header_name: Optional[str]
    pass_cert_info_cert_header: Optional[EnumSlbSslAuthPolPassinfoCertFlag]
    pass_cert_info_2424ssl_compliance_header: Optional[EnumSlbSslAuthPolPassinfoComp2424]

    def __init__(self, index: str = None):
        self.index = index
        self.description = None
        self.state = None
        self.ca_chain_lookup_depth = None
        self.ca_verification = None
        self.failure_redirection_url = None
        self.trusted_ca_chain_name = None
        self.trusted_ca_chain_type = None
        self.advertised_ca_chain_name = None
        self.advertised_ca_chain_type = None
        self.cert_validation_method = None
        self.ocsp_validation_static_uri = None
        self.ocsp_uri_priority = None
        self.ocsp_response_cache_time_second = None
        self.ocsp_response_deviation_time_second = None
        self.ocsp_cert_chain_validation = None
        self.ocsp_response_secure = None
        self.pass_cert_info_version_header_name = None
        self.pass_cert_info_version_header = None
        self.pass_cert_info_serial_number_header_name = None
        self.pass_cert_info_serial_number_header = None
        self.pass_cert_info_sign_algorithm_header_name = None
        self.pass_cert_info_sign_algorithm_header = None
        self.pass_cert_info_issuer_header_name = None
        self.pass_cert_info_issuer_header = None
        self.pass_cert_info_not_before_header_name = None
        self.pass_cert_info_not_before_header = None
        self.pass_cert_info_not_after_header_name = None
        self.pass_cert_info_not_after_header = None
        self.pass_cert_info_subject_header_name = None
        self.pass_cert_info_subject_header = None
        self.pass_cert_info_public_key_type_header_name = None
        self.pass_cert_info_public_key_type_header = None
        self.pass_cert_info_md5_header_name = None
        self.pass_cert_info_md5_header = None
        self.pass_cert_info_cert_header_name = None
        self.pass_cert_info_cert_header = None
        self.pass_cert_info_2424ssl_compliance_header = None


bean_map = {
    SlbNewSslCfgAuthPolTable: dict(
        struct=SSLClientAuthPolicyParameters,
        direct=True,
        attrs=dict(
            NameIdIndex='index',
            Name='description',
            AdminStatus='state',
            Cadepth='ca_chain_lookup_depth',
            Caverify='ca_verification',
            Failurl='failure_redirection_url',
            TrustcaChainName='trusted_ca_chain_name',
            TrustcaChainType='trusted_ca_chain_type',
            ClientcaReqChainName='advertised_ca_chain_name',
            ClientcaReqChainType='advertised_ca_chain_type',
            ValidityMethod='cert_validation_method',
            ValidityStaturi='ocsp_validation_static_uri',
            ValidityUriprior='ocsp_uri_priority',
            ValidityCachtime='ocsp_response_cache_time_second',
            ValidityTimedev='ocsp_response_deviation_time_second',
            ValidityVchain='ocsp_cert_chain_validation',
            ValiditySecure='ocsp_response_secure',
            PassinfoVersionName='pass_cert_info_version_header_name',
            PassinfoVersionFlag='pass_cert_info_version_header',
            PassinfoSerialName='pass_cert_info_serial_number_header_name',
            PassinfoSerialFlag='pass_cert_info_serial_number_header',
            PassinfoAlgoName='pass_cert_info_sign_algorithm_header_name',
            PassinfoAlgoFlag='pass_cert_info_sign_algorithm_header',
            PassinfoIssuerName='pass_cert_info_issuer_header_name',
            PassinfoIssuerFlag='pass_cert_info_issuer_header',
            PassinfoNbeforeName='pass_cert_info_not_before_header_name',
            PassinfoNbeforeFlag='pass_cert_info_not_before_header',
            PassinfoNafterName='pass_cert_info_not_after_header_name',
            PassinfoNafterFlag='pass_cert_info_not_after_header',
            PassinfoSubjectName='pass_cert_info_subject_header_name',
            PassinfoSubjectFlag='pass_cert_info_subject_header',
            PassinfoKeytypeName='pass_cert_info_public_key_type_header_name',
            PassinfoKeytypeFlag='pass_cert_info_public_key_type_header',
            PassinfoMd5Name='pass_cert_info_md5_header_name',
            PassinfoMd5Flag='pass_cert_info_md5_header',
            PassinfoCertName='pass_cert_info_cert_header_name',
            PassinfoCertFlag='pass_cert_info_cert_header',
            PassinfoComp2424='pass_cert_info_2424ssl_compliance_header'
        )
    )
}


class SSLClientAuthPolicyConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[SSLClientAuthPolicyParameters]

    def __init__(self, alteon_connection):
        super(SSLClientAuthPolicyConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: SSLClientAuthPolicyParameters) -> SSLClientAuthPolicyParameters:
        self._read_device_beans(parameters)
        if self._beans:
            parameters.cert_validation_method = EnumSlbSslAuthPolValidityMethod.enum(parameters.cert_validation_method)
            parameters.ca_verification = EnumSlbSslAuthPolCaverify.enum(parameters.ca_verification)
            if self._beans[SlbNewSslCfgAuthPolTable].Type == EnumSlbSslAuthPolType.frontend:
                return parameters

    def _update(self, parameters: SSLClientAuthPolicyParameters, dry_run: bool) -> str:
        parameters.cert_validation_method = self._enum_to_int(EnumSlbSslAuthPolValidityMethod,
                                                              parameters.cert_validation_method)
        parameters.ca_verification = self._enum_to_int(EnumSlbSslAuthPolCaverify, parameters.ca_verification)
        self._write_device_beans(parameters, dry_run=dry_run)
        ssl_auth_pol = self._get_bean_instance(SlbNewSslCfgAuthPolTable, parameters)
        ssl_auth_pol.Type = EnumSlbSslAuthPolType.frontend
        self._device_api.update(ssl_auth_pol, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(SlbNewSslCfgAuthPolTable, parameters)

