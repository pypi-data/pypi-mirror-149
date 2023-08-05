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
from radware.alteon.beans.SlbNewSslCfgSSLPolTable import *
from typing import Optional, ClassVar


class CertType(RadwareParametersExtension):
    group = 'group'
    cert = 'cert'


class SSLPolicyParameters(RadwareParametersStruct):
    index: str
    description: Optional[str]
    state: Optional[EnumSlbSslSSLPolAdminStatus]
    secure_renegotiation: Optional[int]
    dh_key_size: Optional[EnumSlbSslSSLPolDHkey]
    fe_ssl_encryption: Optional[EnumSlbSslSSLPolFessl]
    fe_ssl_v3: Optional[EnumSlbSslSSLPolFESslv3Version]
    fe_ssl_tls1_0: Optional[EnumSlbSslSSLPolFETls10Version]
    fe_ssl_tls1_1: Optional[EnumSlbSslSSLPolFETls11Version]
    fe_ssl_tls1_2: Optional[EnumSlbSslSSLPolFETls12Version]
    fe_cipher_suite: Optional[EnumSlbSslSSLPolCipherName]
    fe_user_defined_cipher: Optional[str]
    fe_intermediate_ca_chain_name: Optional[str]
    fe_intermediate_ca_chain_type: Optional[CertType]
    fe_auth_policy_name: Optional[str]
    fe_hw_ssl_offload: Optional[EnumSlbSslSSLPolHwoffldFeFeatures]
    fe_hw_offload_rsa: Optional[EnumSlbSslSSLPolHwoffldFeRsa]
    fe_hw_offload_dh: Optional[EnumSlbSslSSLPolHwoffldFeDh]
    fe_hw_offload_ec: Optional[EnumSlbSslSSLPolHwoffldFeEc]
    fe_hw_offload_bulk_encryption: Optional[EnumSlbSslSSLPolHwoffldFeBulk]
    be_ssl_encryption: Optional[EnumSlbSslSSLPolBessl]
    be_ssl_v3: Optional[EnumSlbSslSSLPolBESslv3Version]
    be_ssl_tls1_0: Optional[EnumSlbSslSSLPolBETls10Version]
    be_ssl_tls1_1: Optional[EnumSlbSslSSLPolBETls11Version]
    be_ssl_tls1_2: Optional[EnumSlbSslSSLPolBETls12Version]
    be_cipher: Optional[EnumSlbSslSSLPolBecipher]
    be_user_defined_cipher: Optional[str]
    be_client_cert_name: Optional[str]
    be_auth_policy_name: Optional[str]
    be_include_sni: Optional[EnumSlbSslSSLPolBesni]
    be_hw_offload_rsa: Optional[EnumSlbSslSSLPolHwoffldBeRsa]
    be_hw_offload_dh: Optional[EnumSlbSslSSLPolHwoffldBeDh]
    be_hw_offload_ec: Optional[EnumSlbSslSSLPolHwoffldBeEc]
    be_hw_offload_bulk_encryption: Optional[EnumSlbSslSSLPolHwoffldBeBulk]
    be_hw_ssl_offload: Optional[EnumSlbSslSSLPolHwoffldBeFeatures]
    pass_ssl_info_cipher_header_name: Optional[str]
    pass_ssl_info_cipher_header: Optional[EnumSlbSslSSLPolPassInfoCipherFlag]
    pass_ssl_info_ssl_ver_header_name: Optional[str]
    pass_ssl_info_ssl_ver: Optional[EnumSlbSslSSLPolPassInfoVersionFlag]
    pass_ssl_info_cipher_bits_header_name: Optional[str]
    pass_ssl_info_cipher_bits_header: Optional[EnumSlbSslSSLPolPassInfoHeadBitsFlag]
    pass_ssl_info_add_front_end_https_header: Optional[EnumSlbSslSSLPolPassInfoFrontend]
    pass_ssl_info_compliant_x_ssl_header: Optional[EnumSlbSslSSLPolPassInfoComply]
    http_redirection_conversion: Optional[EnumSlbSslSSLPolConvert]

    def __init__(self, index: str = None):
        self.index = index
        self.description = None
        self.state = None
        self.secure_renegotiation = None
        self.dh_key_size = None
        self.fe_ssl_encryption = None
        self.fe_ssl_v3 = None
        self.fe_ssl_tls1_0 = None
        self.fe_ssl_tls1_1 = None
        self.fe_ssl_tls1_2 = None
        self.fe_cipher_suite = None
        self.fe_user_defined_cipher = None
        self.fe_intermediate_ca_chain_name = None
        self.fe_intermediate_ca_chain_type = None
        self.fe_auth_policy_name = None
        self.fe_hw_ssl_offload = None
        self.fe_hw_offload_rsa = None
        self.fe_hw_offload_dh = None
        self.fe_hw_offload_ec = None
        self.fe_hw_offload_bulk_encryption = None
        self.be_ssl_encryption = None
        self.be_ssl_v3 = None
        self.be_ssl_tls1_0 = None
        self.be_ssl_tls1_1 = None
        self.be_ssl_tls1_2 = None
        self.be_cipher = None
        self.be_user_defined_cipher = None
        self.be_client_cert_name = None
        self.be_auth_policy_name = None
        self.be_include_sni = None
        self.be_hw_offload_rsa = None
        self.be_hw_offload_dh = None
        self.be_hw_offload_ec = None
        self.be_hw_offload_bulk_encryption = None
        self.be_hw_ssl_offload = None
        self.pass_ssl_info_cipher_header_name = None
        self.pass_ssl_info_cipher_header = None
        self.pass_ssl_info_ssl_ver_header_name = None
        self.pass_ssl_info_ssl_ver = None
        self.pass_ssl_info_cipher_bits_header_name = None
        self.pass_ssl_info_cipher_bits_header = None
        self.pass_ssl_info_add_front_end_https_header = None
        self.pass_ssl_info_compliant_x_ssl_header = None
        self.http_redirection_conversion = None


bean_map = {
    SlbNewSslCfgSSLPolTable: dict(
        struct=SSLPolicyParameters,
        direct=True,
        attrs=dict(
            NameIdIndex='index',
            Name='description',
            AdminStatus='state',
            Secreneg='secure_renegotiation',
            DHkey='dh_key_size',
            Fessl='fe_ssl_encryption',
            FESslv3Version='fe_ssl_v3',
            FETls10Version='fe_ssl_tls1_0',
            FETls11Version='fe_ssl_tls1_1',
            FETls12Version='fe_ssl_tls1_2',
            CipherName='fe_cipher_suite',
            IntermcaChainName='fe_intermediate_ca_chain_name',
            IntermcaChainType='fe_intermediate_ca_chain_type',
            Authpol='fe_auth_policy_name',
            HwoffldFeFeatures='fe_hw_ssl_offload',
            HwoffldFeRsa='fe_hw_offload_rsa',
            HwoffldFeDh='fe_hw_offload_dh',
            HwoffldFeEc='fe_hw_offload_ec',
            HwoffldFeBulk='fe_hw_offload_bulk_encryption',
            Bessl='be_ssl_encryption',
            BESslv3Version='be_ssl_v3',
            BETls10Version='be_ssl_tls1_0',
            BETls11Version='be_ssl_tls1_1',
            BETls12Version='be_ssl_tls1_2',
            Becipher='be_cipher',
            BEClientCertName='be_client_cert_name',
            BEAuthpol='be_auth_policy_name',
            Besni='be_include_sni',
            HwoffldBeFeatures='be_hw_ssl_offload',
            HwoffldBeRsa='be_hw_offload_rsa',
            HwoffldBeDh='be_hw_offload_dh',
            HwoffldBeEc='be_hw_offload_ec',
            HwoffldBeBulk='be_hw_offload_bulk_encryption',
            PassInfoCipherName='pass_ssl_info_cipher_header_name',
            PassInfoCipherFlag='pass_ssl_info_cipher_header',
            PassInfoVersionName='pass_ssl_info_ssl_ver_header_name',
            PassInfoVersionFlag='pass_ssl_info_ssl_ver',
            PassInfoHeadBitsName='pass_ssl_info_cipher_bits_header_name',
            PassInfoHeadBitsFlag='pass_ssl_info_cipher_bits_header',
            PassInfoFrontend='pass_ssl_info_add_front_end_https_header',
            PassInfoComply='pass_ssl_info_compliant_x_ssl_header',
            Convert='http_redirection_conversion'
        )
    )
}


class SSLPolicyConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[SSLPolicyParameters]

    def __init__(self, alteon_connection):
        super(SSLPolicyConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: SSLPolicyParameters) -> SSLPolicyParameters:
        self._read_device_beans(parameters)
        if self._beans:
            #TODO - remove secure_renegotiation conversion when Alteon type is int
            if parameters.secure_renegotiation is not None:
                parameters.secure_renegotiation = int(parameters.secure_renegotiation)
            ###
            if parameters.fe_cipher_suite == EnumSlbSslSSLPolCipherName.user_defined:
                parameters.fe_user_defined_cipher = self._beans[SlbNewSslCfgSSLPolTable].CipherUserdef
            elif parameters.fe_cipher_suite == EnumSlbSslSSLPolCipherName.user_defined_expert:
                parameters.fe_user_defined_cipher = self._beans[SlbNewSslCfgSSLPolTable].CipherExpertUserdef
            return parameters

    def _update(self, parameters: SSLPolicyParameters, dry_run: bool) -> str:
        def _update_user_defined_cipher(bean_attr_name, cipher_str):
            ssl_pol = self._get_bean_instance(SlbNewSslCfgSSLPolTable, parameters)
            setattr(ssl_pol, bean_attr_name, cipher_str)
            self._device_api.update(ssl_pol, dry_run=dry_run)

        self._write_device_beans(parameters, dry_run=dry_run)

        if EnumSlbSslSSLPolCipherName.user_defined == parameters.fe_cipher_suite:
            _update_user_defined_cipher('CipherUserdef', parameters.fe_user_defined_cipher)
        elif EnumSlbSslSSLPolCipherName.user_defined_expert == parameters.fe_cipher_suite:
            _update_user_defined_cipher('CipherExpertUserdef', parameters.fe_user_defined_cipher)
        if EnumSlbSslSSLPolBecipher.user_defined == parameters.be_cipher:
            _update_user_defined_cipher('BeCipherUserdef', parameters.be_user_defined_cipher)
        elif EnumSlbSslSSLPolBecipher.user_defined_expert == parameters.be_cipher:
            _update_user_defined_cipher('BeCipherExpertUserdef', parameters.be_user_defined_cipher)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(SlbNewSslCfgSSLPolTable, parameters)
