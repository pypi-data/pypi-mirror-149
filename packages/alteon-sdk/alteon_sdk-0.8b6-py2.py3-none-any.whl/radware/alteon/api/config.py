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




import logging
from radware.sdk.api import BaseAPI
from radware.sdk.configurator import DeviceConfigurationManager, DeviceConfigurator
from radware.sdk.exceptions import ArgumentNotExpectedTypeError
from radware.alteon.sdk.configurators.appshape import AppshapeConfigurator
from radware.alteon.sdk.configurators.gslb_network import GSLBNetworkConfigurator
from radware.alteon.sdk.configurators.gslb_rule import GSLBRuleConfigurator
from radware.alteon.sdk.configurators.health_check_http import HealthCheckHTTPConfigurator
from radware.alteon.sdk.configurators.health_check_logexp import HealthCheckLogExpConfigurator
from radware.alteon.sdk.configurators.health_check_tcp import HealthCheckTCPConfigurator
from radware.alteon.sdk.configurators.server import ServerConfigurator
from radware.alteon.sdk.configurators.server_group import ServerGroupConfigurator
from radware.alteon.sdk.configurators.ssl_cert import SSLCertConfigurator
from radware.alteon.sdk.configurators.ssl_client_auth_policy import SSLClientAuthPolicyConfigurator
from radware.alteon.sdk.configurators.ssl_key import SSLKeyConfigurator
from radware.alteon.sdk.configurators.ssl_policy import SSLPolicyConfigurator
from radware.alteon.sdk.configurators.ssl_server_auth_policy import SSLServerAuthPolicyConfigurator
from radware.alteon.sdk.configurators.vadc_instance import VADCInstanceConfigurator
from radware.alteon.sdk.configurators.virtual_server import VirtualServerConfigurator
from radware.alteon.sdk.configurators.virtual_service import VirtualServiceConfigurator
from radware.alteon.sdk.configurators.l2_vlan import VLANConfigurator
from radware.alteon.sdk.configurators.system_local_user import LocalUserConfigurator
from radware.alteon.sdk.configurators.system_management_access import ManagementAccessConfigurator
from radware.alteon.sdk.configurators.system_predefined_local_users import PredefinedLocalUsersConfigurator
from radware.alteon.sdk.configurators.system_radius_authentication import SystemRadiusAuthenticationConfigurator
from radware.alteon.sdk.configurators.system_tacacs_authentication import SystemTacacsAuthenticationConfigurator
from radware.alteon.sdk.configurators.system_snmp import SystemSNMPConfigurator
from radware.alteon.sdk.configurators.system_logging import SystemLoggingConfigurator
from radware.alteon.sdk.configurators.system_vx_peer_syncronization import VXPeerSyncConfigurator
from radware.alteon.sdk.configurators.system_alerts import SystemAlertsConfigurator
from radware.alteon.sdk.configurators.system_dns_client import SystemDNSClientConfigurator
from radware.alteon.sdk.configurators.system_time_date import SystemTimeDateConfigurator
from radware.alteon.sdk.configurators.physical_port import PhysicalPortConfigurator
from radware.alteon.sdk.configurators.lacp_aggregation import LACPAggregationConfigurator
from radware.alteon.sdk.configurators.spanning_tree import SpanningTreeConfigurator
from radware.alteon.sdk.configurators.l2_lldp import LLDPConfigurator
from radware.alteon.sdk.configurators.l3_interface import L3InterfaceConfigurator
from radware.alteon.sdk.configurators.l3_gateway import GatewayConfigurator
from radware.alteon.sdk.configurators.l3_bootp_relay import BOOTPRelayConfigurator
from radware.alteon.sdk.configurators.l3_static_routes import StaticRoutesConfigurator
from radware.alteon.sdk.configurators.ha_floating_ip import FloatingIPConfigurator
from radware.alteon.sdk.configurators.ha_configuration_sync import ConfigurationSyncConfigurator
from radware.alteon.sdk.configurators.high_availability import HighAvailabilityConfigurator
from radware.alteon.sdk.configurators.global_traffic_redirection import GlobalRedirectionConfigurator
from radware.alteon.sdk.configurators.fqdn_server import FQDNServerConfigurator
from radware.alteon.sdk.configurators.network_class_ip import NetworkClassIPConfigurator
from radware.alteon.sdk.configurators.network_class_region import NetworkClassRegionConfigurator
from radware.alteon.sdk.configurators.dns_responders import DNSRespondersConfigurator
from radware.alteon.sdk.configurators.ssl_cert_group import SSLCertGroupConfigurator
from radware.alteon.sdk.configurators.slb_pip import SlbPipConfigurator
from radware.alteon.sdk.configurators.slb_pip6 import SlbPip6Configurator
from radware.alteon.sdk.configurators.ha_service import HaServiceConfigurator
from radware.alteon.sdk.configurators.snmpv3_target_params import SNMPv3TargetParamsConfigurator
from radware.alteon.sdk.configurators.snmpv3_target_addr_new_cfg import SNMPv3TargetAddrNewCfgConfigurator
from radware.alteon.sdk.configurators.bgp_global import BgpGlobalConfigurator
from radware.alteon.sdk.configurators.bgp_peer import BgpPeerConfigurator
from radware.alteon.sdk.configurators.group_real_server import GroupRealServerConfigurator
from radware.alteon.sdk.configurators.bgp_aggr import BgpAggrConfigurator
from radware.alteon.sdk.configurators.alteon_cli_command import AlteonCliCommandConfigurator
from radware.alteon.sdk.configurators.snmpv3_usm_user import SNMPv3UsmUserConfigurator
from radware.alteon.sdk.configurators.snmpv3_group import SNMPv3GroupConfigurator
from radware.alteon.sdk.configurators.snmpv3_community import SNMPv3CommunityConfigurator
from radware.alteon.sdk.configurators.snmpv3_view_tree_family import SNMPv3ViewTreeFamilyConfigurator
from radware.alteon.sdk.configurators.snmpv3_notify import SNMPv3NotifyConfigurator
from radware.alteon.sdk.configurators.snmp_general import SnmpGeneralConfigurator
from radware.alteon.sdk.configurators.gel import GelConfigurator
from radware.alteon.sdk.configurators.slb_port import SlbPortConfigurator
from radware.alteon.sdk.configurators.snmpv3_access import SNMPv3AcessConfigurator
from typing import get_type_hints

log = logging.getLogger(__name__)


class AlteonConfigurators(object):
    """
    all Configurator aggregation - exposed in `AlteonClient`
    each new configurator should be linked here

    """

    appshape: AppshapeConfigurator
    gslb_network: GSLBNetworkConfigurator
    gslb_rule: GSLBRuleConfigurator
    hc_http: HealthCheckHTTPConfigurator
    hc_logexp: HealthCheckLogExpConfigurator
    hc_tcp: HealthCheckTCPConfigurator
    server: ServerConfigurator
    server_group: ServerGroupConfigurator
    ssl_cert: SSLCertConfigurator
    ssl_client_auth_policy: SSLClientAuthPolicyConfigurator
    ssl_key: SSLKeyConfigurator
    ssl_policy: SSLPolicyConfigurator
    ssl_server_auth_policy: SSLServerAuthPolicyConfigurator
    vadc_instance: VADCInstanceConfigurator
    virtual_server: VirtualServerConfigurator
    virtual_service: VirtualServiceConfigurator
    l2_vlan: VLANConfigurator
    sys_local_user: LocalUserConfigurator
    sys_management_access: ManagementAccessConfigurator
    sys_predefined_local_users: PredefinedLocalUsersConfigurator
    sys_radius_auth: SystemRadiusAuthenticationConfigurator
    sys_tacacs_auth: SystemTacacsAuthenticationConfigurator
    sys_snmp: SystemSNMPConfigurator
    sys_logging: SystemLoggingConfigurator
    sys_vx_peer_sync: VXPeerSyncConfigurator
    sys_alerts: SystemAlertsConfigurator
    sys_dns_client: SystemDNSClientConfigurator
    sys_time_date: SystemTimeDateConfigurator
    physical_port: PhysicalPortConfigurator
    lacp_aggregation: LACPAggregationConfigurator
    spanning_tree: SpanningTreeConfigurator
    l2_lldp: LLDPConfigurator
    l3_interface: L3InterfaceConfigurator
    l3_gateway: GatewayConfigurator
    l3_bootp_relay: BOOTPRelayConfigurator
    l3_static_routes: StaticRoutesConfigurator
    ha_floating_ip: FloatingIPConfigurator
    ha_config_sync: ConfigurationSyncConfigurator
    high_availability: HighAvailabilityConfigurator
    global_redirection: GlobalRedirectionConfigurator
    fdn_server: FQDNServerConfigurator
    network_class_ip: NetworkClassIPConfigurator
    network_class_region: NetworkClassRegionConfigurator
    dns_responders: DNSRespondersConfigurator
    ssl_cert_group: SSLCertGroupConfigurator
    slb_pip: SlbPipConfigurator
    slb_pip6: SlbPip6Configurator
    ha_service: HaServiceConfigurator
    snmpv3_target_params: SNMPv3TargetParamsConfigurator
    snmpv3_target_addr_new_cfg: SNMPv3TargetAddrNewCfgConfigurator
    bgp_global: BgpGlobalConfigurator
    bgp_peer: BgpPeerConfigurator
    group_real_server: GroupRealServerConfigurator
    bgp_aggr: BgpAggrConfigurator
    alteon_cli_command: AlteonCliCommandConfigurator
    snmpv3_usm_user: SNMPv3UsmUserConfigurator
    snmpv3_group: SNMPv3GroupConfigurator
    snmpv3_community: SNMPv3CommunityConfigurator
    snmpv3_view_tree_family: SNMPv3ViewTreeFamilyConfigurator
    snmpv3_notify: SNMPv3NotifyConfigurator
    snmp_general: SnmpGeneralConfigurator
    gel: GelConfigurator
    slb_port: SlbPortConfigurator
    snmpv3_access: SNMPv3AcessConfigurator

    def __init__(self, connection):
        configurator_types = get_type_hints(type(self))
        self.appshape = configurator_types['appshape'](connection)
        self.gslb_network = configurator_types['gslb_network'](connection)
        self.gslb_rule = configurator_types['gslb_rule'](connection)
        self.hc_http = configurator_types['hc_http'](connection)
        self.hc_logexp = configurator_types['hc_logexp'](connection)
        self.hc_tcp = configurator_types['hc_tcp'](connection)
        self.server = configurator_types['server'](connection)
        self.server_group = configurator_types['server_group'](connection)
        self.ssl_cert = configurator_types['ssl_cert'](connection)
        self.ssl_client_auth_policy = configurator_types['ssl_client_auth_policy'](connection)
        self.ssl_key = configurator_types['ssl_key'](connection)
        self.ssl_policy = configurator_types['ssl_policy'](connection)
        self.ssl_server_auth_policy = configurator_types['ssl_server_auth_policy'](connection)
        self.vadc_instance = configurator_types['vadc_instance'](connection)
        self.virtual_server = configurator_types['virtual_server'](connection)
        self.virtual_service = configurator_types['virtual_service'](connection)
        self.l2_vlan = configurator_types['l2_vlan'](connection)
        self.sys_local_user = configurator_types['sys_local_user'](connection)
        self.sys_management_access = configurator_types['sys_management_access'](connection)
        self.sys_predefined_local_users = configurator_types['sys_predefined_local_users'](connection)
        self.sys_radius_auth = configurator_types['sys_radius_auth'](connection)
        self.sys_tacacs_auth = configurator_types['sys_tacacs_auth'](connection)
        self.sys_snmp = configurator_types['sys_snmp'](connection)
        self.sys_logging = configurator_types['sys_logging'](connection)
        self.sys_vx_peer_sync = configurator_types['sys_vx_peer_sync'](connection)
        self.sys_alerts = configurator_types['sys_alerts'](connection)
        self.sys_dns_client = configurator_types['sys_dns_client'](connection)
        self.sys_time_date = configurator_types['sys_time_date'](connection)
        self.physical_port = configurator_types['physical_port'](connection)
        self.lacp_aggregation = configurator_types['lacp_aggregation'](connection)
        self.spanning_tree = configurator_types['spanning_tree'](connection)
        self.l2_lldp = configurator_types['l2_lldp'](connection)
        self.l3_interface = configurator_types['l3_interface'](connection)
        self.l3_gateway = configurator_types['l3_gateway'](connection)
        self.l3_bootp_relay = configurator_types['l3_bootp_relay'](connection)
        self.l3_static_routes = configurator_types['l3_static_routes'](connection)
        self.ha_floating_ip = configurator_types['ha_floating_ip'](connection)
        self.ha_config_sync = configurator_types['ha_config_sync'](connection)
        self.high_availability = configurator_types['high_availability'](connection)
        self.global_redirection = configurator_types['global_redirection'](connection)
        self.fdn_server = configurator_types['fdn_server'](connection)
        self.network_class_ip = configurator_types['network_class_ip'](connection)
        self.network_class_region = configurator_types['network_class_region'](connection)
        self.dns_responders = configurator_types['dns_responders'](connection)
        self.ssl_cert_group = configurator_types['ssl_cert_group'](connection)
        self.slb_pip = configurator_types['slb_pip'](connection)
        self.slb_pip6 = configurator_types['slb_pip6'](connection)
        self.ha_service = configurator_types['ha_service'](connection)
        self.snmpv3_target_params = configurator_types['snmpv3_target_params'](connection)
        self.snmpv3_target_addr_new_cfg = configurator_types['snmpv3_target_addr_new_cfg'](connection)
        self.bgp_global = configurator_types['bgp_global'](connection)
        self.bgp_peer = configurator_types['bgp_peer'](connection)
        self.group_real_server = configurator_types['group_real_server'](connection)
        self.bgp_aggr = configurator_types['bgp_aggr'](connection)
        self.alteon_cli_command = configurator_types['alteon_cli_command'](connection)
        self.snmpv3_usm_user = configurator_types['snmpv3_usm_user'](connection)
        self.snmpv3_group = configurator_types['snmpv3_group'](connection)
        self.snmpv3_community = configurator_types['snmpv3_community'](connection)
        self.snmpv3_view_tree_family = configurator_types['snmpv3_view_tree_family'](connection)
        self.snmpv3_notify = configurator_types['snmpv3_notify'](connection)
        self.snmp_general = configurator_types['snmp_general'](connection)
        self.gel = configurator_types['gel'](connection)
        self.slb_port = configurator_types['slb_port'](connection)
        self.snmpv3_access = configurator_types['snmpv3_access'](connection)

class AlteonConfiguration(BaseAPI):
    """
    API to execute command over a `parameter` set.
    this class will locate appropriate Configurator by `parameter` type
    """

    def __init__(self, connection):
        self._connection = connection
        self._configurators = AlteonConfigurators(connection)
        self._config_manager = DeviceConfigurationManager()
        log.info(' Alteon Configuration Module initialized, server: {0}'.format(self._connection.id))

    def execute(self, command, parameters, **kw):
        configurator = self._find_configurator(parameters)
        return self._config_manager.execute(configurator, command, parameters, **kw)

    def _find_configurator(self, parameters):
        for k, v in self._configurators.__dict__.items():
            if isinstance(v, DeviceConfigurator):
                if v.get_parameters_class() == type(parameters):
                    return v
        raise ArgumentNotExpectedTypeError(parameters, 'no Configurator found for argument type')

    @property
    def manager(self):
        return self._config_manager

    @property
    def type(self):
        return self._configurators
