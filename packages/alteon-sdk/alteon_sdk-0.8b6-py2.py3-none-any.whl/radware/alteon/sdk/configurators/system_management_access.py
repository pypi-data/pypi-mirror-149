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


from radware.sdk.configurator import DryRunDeleteProcedure
from radware.alteon.sdk.alteon_managment import AlteonMngInfo
from radware.sdk.common import RadwareParametersStruct, RadwareParametersExtension
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, MSG_DELETE, AlteonConfigurator
from radware.sdk.exceptions import DeviceConfiguratorError
from radware.alteon.beans.Global import *
from radware.alteon.beans.AgNewCfgMgmtNetTable import *
from radware.alteon.beans.AgNewCfgMgmtNet6Table import *
from radware.alteon.beans.AgNewCfgPortAccessTable import *
from typing import List, Optional, ClassVar

#TODO - Root - agMgmtNewCfgDHCPMode missing in MIB, currently this feature unavailable


class CertType(RadwareParametersExtension):
    group = 'group'
    cert = 'cert'
    none = 'none'


class EnumGatewayHC(BaseBeanEnum):
    arp = 1
    icmp = 2


class ParametersMgmtNet4Struct(RadwareParametersStruct):
    ip_address: Optional[str]
    ip_subnet: Optional[str]
    protocols: Optional[EnumAgMgmtNetProtocol]

    def __init__(self):
        self.ip_address = None
        self.ip_subnet = None
        self.protocols = None


class ParametersMgmtNet6Struct(RadwareParametersStruct):
    ip_address: Optional[str]
    ip_prefix: Optional[int]
    protocols: Optional[EnumAgMgmtNet6Protocol]

    def __init__(self):
        self.ip_address = None
        self.ip_prefix = None
        self.protocols = None


class ManagementAccessParameters(RadwareParametersStruct):
    management_port_state: Optional[EnumAgMgmtNewCfgState]
    management_ip4_address: Optional[str]
    management_ip6_address: Optional[str]
    management_ip4_subnet: Optional[str]
    management_ip6_prefix: Optional[int]
    management_ip4_gateway: Optional[str]
    management_ip6_gateway: Optional[str]
    single_ip_cloud_mode: Optional[EnumAgCurCfgSingleip]
    #management_ip_dhcp: Optional[]
    gateway_health_check: Optional[EnumGatewayHC]
    gateway_health_check_interval: Optional[int]
    gateway_health_check_retries: Optional[int]
    management_port_autonegotiation: Optional[EnumAgMgmtPortNewCfgAuto]
    management_port_speed: Optional[EnumAgMgmtPortNewCfgSpeed]
    management_port_duplex: Optional[EnumAgMgmtPortNewCfgMode]
    idle_timeout_minute: Optional[int]
    language_display: Optional[EnumAgNewCfgGlobalLanguage]
    ssh_state: Optional[EnumAgAccessNewCfgSshState]
    ssh_port: Optional[int]
    ssh_version1: Optional[EnumAgAccessNewCfgSshV1]
    ssh_scp_apply_save: Optional[EnumAgAccessNewCfgSshScp]
    telnet_state: Optional[EnumAgAccessTelnet]
    telnet_port: Optional[int]
    https_state: Optional[EnumAgAccessNewCfgHttpsState]
    https_port: Optional[int]
    https_cert_name: Optional[str]
    https_intermediate_chain_type: Optional[CertType]
    https_intermediate_chain_name: Optional[str]
    https_ssl_tls1_0: Optional[EnumAgAccessNewTls10State]
    https_ssl_tls1_1: Optional[EnumAgAccessNewTls11State]
    https_ssl_tls1_2: Optional[EnumAgAccessNewTls12State]
    https_ssl_tls1_3: Optional[EnumAgAccessNewTls13State]
    cli_login_banner: Optional[str]
    cli_login_notice: Optional[str]
    cli_hostname_prompt: Optional[EnumAgNewCfgPrompt]
    radius_traffic_port: Optional[EnumAgMgmtNewCfgRadius]
    tacacs_traffic_port: Optional[EnumAgMgmtNewCfgTacacs]
    syslog_traffic_port: Optional[EnumAgMgmtNewCfgSyslog]
    snmp_traffic_port: Optional[EnumAgMgmtNewCfgSnmp]
    tftp_traffic_port: Optional[EnumAgMgmtNewCfgTftp]
    dns_traffic_port: Optional[EnumAgMgmtNewCfgDns]
    ocsp_traffic_port: Optional[EnumAgMgmtNewCfgOcsp]
    cdp_traffic_port: Optional[EnumAgMgmtNewCfgCdp]
    wlm_sasp_traffic_port: Optional[EnumAgMgmtNewCfgWlm]
    smtp_traffic_port: Optional[EnumAgMgmtNewCfgSmtp]
    webapp_radius_traffic_port: Optional[EnumAgMgmtNewCfgWsRadius]
    webapp_ldap_traffic_port: Optional[EnumAgMgmtNewCfgWsLdap]
    dp_signaling_traffic_port: Optional[EnumAgMgmtNewCfgDefensePro]
    ntp_traffic_port: Optional[EnumAgMgmtNewCfgNtp]
    management4_nets: Optional[List[ParametersMgmtNet4Struct]]
    management6_nets: Optional[List[ParametersMgmtNet6Struct]]
    data_ports_allow_mng: Optional[List[int]]

    def __init__(self):
        self.management_port_state = None
        self.management_ip4_address = None
        self.management_ip6_address = None
        self.management_ip4_subnet = None
        self.management_ip6_prefix = None
        self.management_ip4_gateway = None
        self.management_ip6_gateway = None
        self.single_ip_cloud_mode = None
        #self.management_ip_dhcp = None
        self.gateway_health_check = None
        self.gateway_health_check_interval = None
        self.gateway_health_check_retries = None
        self.management_port_autonegotiation = None
        self.management_port_speed = None
        self.management_port_duplex = None
        self.idle_timeout_minute = None
        self.language_display = None
        self.ssh_state = None
        self.ssh_port = None
        self.ssh_version1 = None
        self.ssh_scp_apply_save = None
        self.telnet_state = None
        self.telnet_port = None
        self.https_state = None
        self.https_port = None
        self.https_cert_name = None
        self.https_intermediate_chain_type = None
        self.https_intermediate_chain_name = None
        self.https_ssl_tls1_0 = None
        self.https_ssl_tls1_1 = None
        self.https_ssl_tls1_2 = None
        self.https_ssl_tls1_3 = None
        self.cli_login_banner = None
        self.cli_login_notice = None
        self.cli_hostname_prompt = None
        self.radius_traffic_port = None
        self.tacacs_traffic_port = None
        self.syslog_traffic_port = None
        self.snmp_traffic_port = None
        self.tftp_traffic_port = None
        self.dns_traffic_port = None
        self.ocsp_traffic_port = None
        self.cdp_traffic_port = None
        self.wlm_sasp_traffic_port = None
        self.smtp_traffic_port = None
        self.webapp_radius_traffic_port = None
        self.webapp_ldap_traffic_port = None
        self.dp_signaling_traffic_port = None
        self.ntp_traffic_port = None
        self.management4_nets = list()
        self.management6_nets = list()
        self.data_ports_allow_mng = list()


bean_map = {
    Root: dict(
        struct=ManagementAccessParameters,
        direct=True,
        attrs=dict(
            agMgmtNewCfgState='management_port_state',
            agMgmtNewCfgIpAddr='management_ip4_address',
            agMgmtNewCfgIpv6Addr='management_ip6_address',
            agMgmtNewCfgMask='management_ip4_subnet',
            agMgmtNewCfgIpv6PrefixLen='management_ip6_prefix',
            agMgmtNewCfgGateway='management_ip4_gateway',
            agMgmtNewCfgIpv6Gateway='management_ip6_gateway',
            agCurCfgSingleip='single_ip_cloud_mode',
            #agMgmtNewCfgDHCPMode='management_ip_dhcp',
            agMgmtNewCfgArpState='gateway_health_check',
            agMgmtNewCfgIntr='gateway_health_check_interval',
            agMgmtNewCfgRetry='gateway_health_check_retries',
            agMgmtPortNewCfgAuto='management_port_autonegotiation',
            agMgmtPortNewCfgSpeed='management_port_speed',
            agMgmtPortNewCfgMode='management_port_duplex',
            agNewCfgIdleCLITimeout='idle_timeout_minute',
            agNewCfgGlobalLanguage='language_display',
            agAccessNewCfgSshState='ssh_state',
            agAccessNewCfgSshPort='ssh_port',
            agAccessNewCfgSshScp='ssh_scp_apply_save',
            agAccessNewCfgSshV1='ssh_version1',
            agAccessTelnet='telnet_state',
            agNewCfgTelnetServerPort='telnet_port',
            agAccessNewCfgHttpsState='https_state',
            agNewCfgHttpsServerPort='https_port',
            agAccessNewCfgHttpsCert='https_cert_name',
            agAccessNewCfgHttpsIntermcaChainType='https_intermediate_chain_type',
            agAccessNewCfgHttpsIntermcaChainName='https_intermediate_chain_name',
            agAccessNewTls10State='https_ssl_tls1_0',
            agAccessNewTls11State='https_ssl_tls1_1',
            agAccessNewTls12State='https_ssl_tls1_2',
            agAccessNewTls13State='https_ssl_tls1_3',
            agNewCfgLoginBanner='cli_login_banner',
            agNewCfgLoginNotice='cli_login_notice',
            agNewCfgPrompt='cli_hostname_prompt',
            agMgmtNewCfgRadius='radius_traffic_port',
            agMgmtNewCfgTacacs='tacacs_traffic_port',
            agMgmtNewCfgSyslog='syslog_traffic_port',
            agMgmtNewCfgSnmp='snmp_traffic_port',
            agMgmtNewCfgTftp='tftp_traffic_port',
            agMgmtNewCfgDns='dns_traffic_port',
            agMgmtNewCfgOcsp='ocsp_traffic_port',
            agMgmtNewCfgCdp='cdp_traffic_port',
            agMgmtNewCfgWlm='wlm_sasp_traffic_port',
            agMgmtNewCfgSmtp='smtp_traffic_port',
            agMgmtNewCfgWsRadius='webapp_radius_traffic_port',
            agMgmtNewCfgWsLdap='webapp_ldap_traffic_port',
            agMgmtNewCfgDefensePro='dp_signaling_traffic_port',
            agMgmtNewCfgNtp='ntp_traffic_port'
        )
    ),
    AgNewCfgMgmtNetTable: dict(
        struct=List[ParametersMgmtNet4Struct],
        direct=True,
        attrs=dict(
            Subnet='ip_address',
            Mask='ip_subnet',
            Protocol='protocols'
        )
    ),
    AgNewCfgMgmtNet6Table: dict(
        struct=List[ParametersMgmtNet6Struct],
        direct=True,
        attrs=dict(
            Subnet='ip_address',
            Prefix='ip_prefix',
            Protocol='protocols'
        )
    )
}

auto_write_exception = [AgNewCfgMgmtNetTable, AgNewCfgMgmtNet6Table]


class ManagementAccessConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[ManagementAccessParameters]

    def __init__(self, alteon_connection):
        super(ManagementAccessConfigurator, self).__init__(bean_map, alteon_connection)
        self._mng_info = AlteonMngInfo(alteon_connection)

    def _read(self, parameters: ManagementAccessParameters) -> ManagementAccessParameters:
        self._ntp_port_workaround()
        self._read_device_beans(parameters)
        bean_map[Root]['attrs'].update(dict(agMgmtNewCfgNtp='ntp_traffic_port'))
        if self._beans:
            if parameters.gateway_health_check == EnumAgMgmtNewCfgArpState.enabled:
                parameters.gateway_health_check = EnumGatewayHC.arp
            else:
                parameters.gateway_health_check = EnumGatewayHC.icmp

            if self._mng_info.is_standalone:
                for data_port in self._device_api.read_all(AgNewCfgPortAccessTable()):
                    if data_port.State == EnumAgPortAccessState.allow:
                        parameters.data_ports_allow_mng.append(data_port.Index)
            return parameters

    def _update(self, parameters: ManagementAccessParameters, dry_run: bool) -> str:
        if parameters.gateway_health_check:
            if EnumGatewayHC.arp == parameters.gateway_health_check:
                parameters.gateway_health_check = EnumAgMgmtNewCfgArpState.enabled
            else:
                parameters.gateway_health_check = EnumAgMgmtNewCfgArpState.disabled
        if parameters.single_ip_cloud_mode == EnumAgCurCfgSingleip.unsupported:
            parameters.single_ip_cloud_mode = None

        self._assign_write_numeric_index_beans(AgNewCfgMgmtNetTable, parameters.management4_nets, dry_run=dry_run)
        self._assign_write_numeric_index_beans(AgNewCfgMgmtNet6Table, parameters.management6_nets, dry_run=dry_run)

        if parameters.data_ports_allow_mng:
            if not self._mng_info.is_standalone:
                raise DeviceConfiguratorError(self.__class__, 'data_ports_allow_mng allowed only on Standalone mode')

            for data_port in self._device_api.read_all(AgNewCfgPortAccessTable()):
                if data_port.Index in parameters.data_ports_allow_mng:
                    data_port.State = EnumAgPortAccessState.allow
                else:
                    data_port.State = EnumAgPortAccessState.deny
                self._device_api.update(data_port, dry_run=dry_run)

        self._ntp_port_workaround()
        self._write_device_beans(parameters, dry_run=dry_run, direct_exclude=auto_write_exception)
        bean_map[Root]['attrs'].update(dict(agMgmtNewCfgNtp='ntp_traffic_port'))
        return self._get_object_id(parameters) + MSG_UPDATE

    def delete(self, parameters: ManagementAccessParameters, dry_run=False, **kw) -> str:
        def _remove_nets(nets):
            for net in nets:
                self._device_api.delete(net, dry_run=dry_run)

        net4 = self._device_api.read_all(AgNewCfgMgmtNetTable())
        net6 = self._device_api.read_all(AgNewCfgMgmtNet6Table())
        _remove_nets(net4)
        _remove_nets(net6)
        if self._mng_info.is_standalone:
            mgmt_ports = self._device_api.read_all(AgNewCfgPortAccessTable())
            if mgmt_ports:
                for port in mgmt_ports:
                    port.State = EnumAgPortAccessState.deny
                    self._device_api.update(port, dry_run=dry_run)

        return 'management networks and ports' + MSG_DELETE

    def _update_remove(self, parameters: ManagementAccessParameters, dry_run: bool) -> str:
        self._remove_device_beans_by_struct_collection(parameters.management4_nets, dry_run=dry_run)
        self._remove_device_beans_by_struct_collection(parameters.management6_nets, dry_run=dry_run)
        if parameters.data_ports_allow_mng:
            for port in parameters.data_ports_allow_mng:
                instance = AgNewCfgPortAccessTable()
                instance.Index = port
                instance.State = EnumAgPortAccessState.deny
                self._device_api.update(instance, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(Root, parameters)

    def dry_run_delete_procedure(self, diff):
        dry_run_procedure = DryRunDeleteProcedure()
        dry_run_procedure.non_removable_bean_map_attrs_list.append(bean_map[Root]['attrs'])
        return dry_run_procedure

    def _ntp_port_workaround(self):
        #TODO - remove this section when vadc report ntp port enum value mgmt/data
        if self._mng_info.is_vadc:
            bean_map[Root]['attrs'].pop('agMgmtNewCfgNtp')
