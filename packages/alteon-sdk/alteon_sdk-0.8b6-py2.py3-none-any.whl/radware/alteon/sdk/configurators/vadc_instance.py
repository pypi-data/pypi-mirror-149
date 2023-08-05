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


from radware.sdk.common import RadwareParametersStruct, PasswordArgument
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, AlteonConfigurator
from radware.alteon.sdk.alteon_managment import AlteonMngInfo
from radware.sdk.exceptions import DeviceConfiguratorError
from radware.alteon.beans.VADCNewCfgTable import *
from radware.alteon.beans.VADCNewCfgSysTable import *
from radware.alteon.beans.VADCNewCfgNetTable import *
from radware.alteon.beans.VADCUsersPswdTable import *
from radware.alteon.beans.VADCInfoTable import *
from radware.sdk.beans_common import BeanUtils
from typing import List, Optional, ClassVar, Dict


class ParametersMgmtNetStruct(RadwareParametersStruct):
    vlan: int
    ip_ver: Optional[EnumVADCNetIPver]
    ip4_net_address: Optional[str]
    ip4_subnet: Optional[str]
    ip6_net_address: Optional[str]
    ip6_prefix: Optional[int]

    def __init__(self, vlan: int = None):
        self.vlan = vlan
        self.ip_ver = None
        self.ip4_net_address = None
        self.ip4_subnet = None
        self.ip6_net_address = None
        self.ip6_prefix = None


class VADCInstanceParameters(RadwareParametersStruct):
    index: int
    vadc_system_name: Optional[str]
    state: Optional[EnumVADCState]
    capacity_units: Optional[int]
    throughput_limit_mbps: Optional[int]
    appwall_capacity_units: Optional[int]
    fastview_capacity_units: Optional[int]
    ssl_cps_limit: Optional[int]
    compression_limit_mbps: Optional[int]
    apm_pages_per_minute_limit: Optional[int]
    waf_limit_mbps: Optional[int]
    authentication_user_limit: Optional[int]
    feature_global: Optional[EnumVADCFeatGlobal]
    feature_bwm: Optional[EnumVADCFeatBWM]
    feature_ados: Optional[EnumVADCFeatADOS]
    fastview_pages_per_minute_limit: Optional[int]
    feature_linkproof: Optional[EnumVADCFeatLP]
    feature_ip_reputation: Optional[EnumVADCFeatIPRep]
    feature_url_filtering: Optional[EnumVADCFeatURLFilter]
    vadc_ha_id: Optional[int]
    management_ip4_address: Optional[str]
    management_ip4_mask: Optional[str]
    management_ip4_gateway: Optional[str]
    management_ip6_address: Optional[str]
    management_ip6_prefix: Optional[int]
    management_ip6_gateway: Optional[str]
    vadc_https_access: Optional[EnumVADCSysHttpsState]
    vadc_ssh_access: Optional[EnumVADCSysSshState]
    vadc_snmp_access: Optional[EnumVADCSysSnmpState]
    delegation_vx_management: Optional[EnumVADCSysMmgmtDelegation]
    delegation_vx_syslog: Optional[EnumVADCSyslogDelegation]
    delegation_vx_radius: Optional[EnumVADCRadiusDelegation]
    delegation_vx_tacacs: Optional[EnumVADCTacacsDelegation]
    delegation_vx_smtp: Optional[EnumVADCSmtpDelegation]
    lock_vadc_management: Optional[EnumVADCSysMmgmtState]
    lock_vadc_syslog: Optional[EnumVADCSysSyslogState]
    lock_vadc_radius: Optional[EnumVADCSysRadiusState]
    lock_vadc_tacacs: Optional[EnumVADCSysTacacsState]
    lock_vadc_smtp: Optional[EnumVADCSysSmtpState]
    vx_admin_password: Optional[PasswordArgument]
    vadc_admin_password: Optional[PasswordArgument]
    vlans: Optional[List[int]]
    vadc_peer_id: Optional[int]
    vadc_peer_name: Optional[str]
    vadc_peer_ip4: Optional[str]
    vadc_peer_ip4_gateway: Optional[str]
    vadc_peer_subnet: Optional[str]
    vadc_peer_ip6: Optional[str]
    vadc_peer_prefix: Optional[int]
    vadc_peer_ip6_gateway: Optional[str]
    management_nets: Optional[List[ParametersMgmtNetStruct]]

    def __init__(self, index: int = None):
        self.index = index
        self.vadc_system_name = None
        self.state = None
        self.capacity_units = None
        self.throughput_limit_mbps = None
        self.appwall_capacity_units = None
        self.fastview_capacity_units = None
        self.ssl_cps_limit = None
        self.compression_limit_mbps = None
        self.apm_pages_per_minute_limit = None
        self.waf_limit_mbps = None
        self.authentication_user_limit = None
        self.feature_global = None
        self.feature_bwm = None
        self.feature_ados = None
        self.fastview_pages_per_minute_limit = None
        self.feature_linkproof = None
        self.feature_ip_reputation = None
        self.feature_url_filtering = None
        self.vadc_ha_id = None
        self.management_ip4_address = None
        self.management_ip4_mask = None
        self.management_ip4_gateway = None
        self.management_ip6_address = None
        self.management_ip6_prefix = None
        self.management_ip6_gateway = None
        self.vadc_https_access = None
        self.vadc_ssh_access = None
        self.vadc_snmp_access = None
        self.delegation_vx_management = None
        self.delegation_vx_syslog = None
        self.delegation_vx_radius = None
        self.delegation_vx_tacacs = None
        self.delegation_vx_smtp = None
        self.lock_vadc_management = None
        self.lock_vadc_syslog = None
        self.lock_vadc_radius = None
        self.lock_vadc_tacacs = None
        self.lock_vadc_smtp = None
        self.vx_admin_password = None
        self.vadc_admin_password = None
        self.vlans = None
        self.vadc_peer_id = None
        self.vadc_peer_name = None
        self.vadc_peer_ip4 = None
        self.vadc_peer_ip4_gateway = None
        self.vadc_peer_subnet = None
        self.vadc_peer_ip6 = None
        self.vadc_peer_prefix = None
        self.vadc_peer_ip6_gateway = None
        self.management_nets = list()


bean_map = {
    VADCNewCfgTable: dict(
        struct=VADCInstanceParameters,
        direct=True,
        attrs=dict(
            VADCId='index',
            Name='vadc_system_name',
            State='state',
            CU='capacity_units',
            Limit='throughput_limit_mbps',
            AwCU='appwall_capacity_units',
            FastviewCu='fastview_capacity_units',
            SslLimit='ssl_cps_limit',
            CompLimit='compression_limit_mbps',
            ApmLimit='apm_pages_per_minute_limit',
            WafLimit='waf_limit_mbps',
            AuthLimit='authentication_user_limit',
            FastviewLimit='fastview_pages_per_minute_limit',
            FeatGlobal='feature_global',
            FeatBWM='feature_bwm',
            FeatADOS='feature_ados',
            FeatLP='feature_linkproof',
            FeatIPRep='feature_ip_reputation',
            FeatURLFilter='feature_url_filtering'
        )
    ),
    VADCNewCfgSysTable: dict(
        struct=VADCInstanceParameters,
        direct=True,
        attrs=dict(
            VADCId='index',
            HaId='vadc_ha_id',
            MmgmtAddr='management_ip4_address',
            MmgmtMask='management_ip4_mask',
            MmgmtGw='management_ip4_gateway',
            MmgmtIpv6Addr='management_ip6_address',
            MmgmtIpv6PrefixLen='management_ip6_prefix',
            MmgmtIpv6Gateway='management_ip6_gateway',
            HttpsState='vadc_https_access',
            SshState='vadc_ssh_access',
            SnmpState='vadc_snmp_access',
            MmgmtDelegation='delegation_vx_management',
            SyslogDelegation='delegation_vx_syslog',
            RadiusDelegation='delegation_vx_radius',
            TacacsDelegation='delegation_vx_tacacs',
            SmtpDelegation='delegation_vx_smtp',
            MmgmtState='lock_vadc_management',
            SyslogState='lock_vadc_syslog',
            RadiusState='lock_vadc_radius',
            TacacsState='lock_vadc_tacacs',
            SmtpState='lock_vadc_smtp',
            PeerId='vadc_peer_id',
            PeerName='vadc_peer_name',
            PeerAddr='vadc_peer_ip4',
            PeerGw='vadc_peer_ip4_gateway',
            PeerMask='vadc_peer_subnet',
            PeerIpv6Addr='vadc_peer_ip6',
            PeerIpv6PrefixLen='vadc_peer_prefix',
            PeerIpv6Gateway='vadc_peer_ip6_gateway'
        )
    ),
    VADCNewCfgNetTable: dict(
        struct=List[ParametersMgmtNetStruct],
        direct=True,
        attrs=dict(
            VADCId='index',
            VlanId='vlan',
            IPver='ip_ver',
            IPBegin='ip4_net_address',
            Mask='ip4_subnet',
            IPv6Begin='ip6_net_address',
            Prefix='ip6_prefix'
        )
    )
}

auto_write_exception = [VADCNewCfgNetTable]

bean_state_map = {
    VADCInfoTable: dict(include=['Id','Status', 'VRRPStatus', 'CU', 'Limit'])
}


class VADCInstanceConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[VADCInstanceParameters]
    state_beans: ClassVar[Dict[DeviceBean, Dict]] = bean_state_map

    def __init__(self, alteon_connection):
        super(VADCInstanceConfigurator, self).__init__(bean_map, alteon_connection)
        self._mng_info = AlteonMngInfo(alteon_connection)

    def _read(self, parameters: VADCInstanceParameters) -> VADCInstanceParameters:
        self._container_validation()
        self._read_device_beans(parameters)
        if self._beans:
            parameters.vlans = BeanUtils.decode_bmp_sub_one(self._beans[VADCNewCfgTable].VlanId)
            return parameters

    def _update(self, parameters: VADCInstanceParameters, dry_run: bool) -> str:
        self._container_validation()

        self._assign_write_numeric_index_beans(VADCNewCfgNetTable, parameters.management_nets,
                                               dict(VADCId=parameters.index), dry_run=dry_run)
        self._write_device_beans(parameters, dry_run=dry_run, direct_exclude=auto_write_exception)

        if parameters.vadc_admin_password and parameters.vx_admin_password:
            instance = VADCUsersPswdTable()
            instance.VADCId = parameters.index
            instance.vADCAccessAdminPasswd = parameters.vx_admin_password
            instance.vADCAccessAdminNewPasswd = parameters.vadc_admin_password
            instance.vADCAccessAdminConfNewPasswd = parameters.vadc_admin_password
            self._device_api.update(instance, dry_run=dry_run)

        if parameters.vlans:
            for vlan in parameters.vlans:
                new_vlan = self._entry_bean_instance(parameters)
                new_vlan.AddVlan = vlan
                self._device_api.update(new_vlan, dry_run=dry_run)

        return self._get_object_id(parameters) + MSG_UPDATE

    def _update_remove(self, parameters: VADCInstanceParameters, dry_run: bool) -> str:
        self._remove_device_beans_by_struct_collection(parameters.management_nets, dry_run=dry_run)
        if parameters.vlans:
            for vlan in parameters.vlans:
                instance = self._entry_bean_instance(parameters)
                instance.RemoveVlan = vlan
                self._device_api.update(instance, dry_run=dry_run)

        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(VADCNewCfgTable, parameters)

    def _container_validation(self):
        if not self._mng_info.is_vx:
            raise DeviceConfiguratorError(self.__class__, 'not a VX container')

