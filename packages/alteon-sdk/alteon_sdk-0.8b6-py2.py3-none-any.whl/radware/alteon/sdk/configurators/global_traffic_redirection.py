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
from radware.sdk.common import RadwareParametersStruct
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, MSG_DELETE, AlteonConfigurator
from radware.alteon.beans.Global import *
from radware.alteon.beans.GslbNewCfgRemSiteTable import *
from radware.alteon.beans.GslbInfoRemSiteTable import GslbInfoRemSiteTable
from typing import List, Optional, ClassVar, Dict


class EnumDnsNoRespCode(BaseBeanEnum):
    format_error = 1
    server_fail = 2
    not_exist_domain = 3
    not_implemented = 4
    server_refuse = 5


class GlobalSiteParameters(RadwareParametersStruct):
    state: Optional[EnumGslbRemSiteState]
    ha_peer_device: Optional[EnumGslbRemSitePeer]
    description: Optional[str]
    site_update_state: Optional[EnumGslbRemSiteUpdate]
    primary_ip4_address: Optional[str]
    primary_ip6_address: Optional[str]
    secondary_ip4_address: Optional[str]
    secondary_ip6_address: Optional[str]
    primary_ip_ver: Optional[EnumGslbRemSitePrimaryIPVer]
    secondary_ip_ver: Optional[EnumGslbRemSiteSecondaryIPVer]

    def __init__(self):
        self.state = None
        self.ha_peer_device = None
        self.description = None
        self.site_update_state = None
        self.primary_ip4_address = None
        self.primary_ip6_address = None
        self.secondary_ip4_address = None
        self.secondary_ip6_address = None
        self.primary_ip_ver = None
        self.secondary_ip_ver = None


class GlobalRedirectionParameters(RadwareParametersStruct):
    state: Optional[EnumGslbNewCfgGenState]
    global_http_redirection: Optional[EnumGslbNewCfgGenHttpRedirect]
    global_proxy_redirection: Optional[EnumGslbNewCfgGenNoremote]
    redirect_to_server_name: Optional[EnumGslbNewCfgGenUsern]
    session_utilization_threshold_percent: Optional[int]
    cpu_utilization_threshold_percent: Optional[int]
    dssp_version: Optional[int]
    dssp_tcp_update_port: Optional[int]
    site_update_interval_second: Optional[int]
    site_update_encryption: Optional[EnumGslbNewCfgGenEncrypt]
    no_server_dns_response_code: Optional[EnumDnsNoRespCode]
    service_down_response: Optional[EnumGslbNewCfgGenServcDownDnsRsp]
    dns_redirection_state: Optional[EnumGslbNewCfgGenDnsDirect]
    dns_persistence_cache_sync: Optional[EnumGslbNewCfgGenDsync]
    hostname_matching: Optional[EnumGslbNewCfgGenHostname]
    dns_persist_ip4_subnet: Optional[str]
    dns_persist_ip6_prefix: Optional[int]
    dns_persist_timeout_minute: Optional[int]
    sites: Optional[List[GlobalSiteParameters]]

    def __init__(self):
        self.state = None
        self.global_http_redirection = None
        self.global_proxy_redirection = None
        self.redirect_to_server_name = None
        self.session_utilization_threshold_percent = None
        self.cpu_utilization_threshold_percent = None
        self.dssp_version = None
        self.dssp_tcp_update_port = None
        self.site_update_interval_second = None
        self.site_update_encryption = None
        self.no_server_dns_response_code = None
        self.service_down_response = None
        self.dns_redirection_state = None
        self.dns_persistence_cache_sync = None
        self.hostname_matching = None
        self.dns_persist_ip4_subnet = None
        self.dns_persist_ip6_prefix = None
        self.dns_persist_timeout_minute = None
        self.sites = list()


bean_map = {
    Root: dict(
        struct=GlobalRedirectionParameters,
        direct=True,
        attrs=dict(
            gslbNewCfgGenState='state',
            gslbNewCfgGenHttpRedirect='global_http_redirection',
            gslbNewCfgGenNoremote='global_proxy_redirection',
            gslbNewCfgGenUsern='redirect_to_server_name',
            gslbNewCfgGenSessUtilCap='session_utilization_threshold_percent',
            gslbNewCfgGenCpuUtilCap='cpu_utilization_threshold_percent',
            gslbNewCfgGenRemSiteUpdateVersion='dssp_version',
            gslbNewCfgGenRemSiteUpdatePort='dssp_tcp_update_port',
            gslbNewCfgGenRemSiteUpdateIntervalSeconds='site_update_interval_second',
            gslbNewCfgGenEncrypt='site_update_encryption',
            gslbNewCfgGenNoResp='no_server_dns_response_code',
            gslbNewCfgGenServcDownDnsRsp='service_down_response',
            gslbNewCfgGenDnsDirect='dns_redirection_state',
            gslbNewCfgGenDsync='dns_persistence_cache_sync',
            gslbNewCfgGenHostname='hostname_matching',
            gslbNewCfgGenSourceIpNetmask='dns_persist_ip4_subnet',
            gslbNewCfgGenSourceIpv6Prefix='dns_persist_ip6_prefix',
            gslbNewCfgGenTimeout='dns_persist_timeout_minute'
        )
    ),
    GslbNewCfgRemSiteTable: dict(
        struct=List[GlobalSiteParameters],
        direct=True,
        attrs=dict(
            State='state',
            Peer='ha_peer_device',
            Name='description',
            Update='site_update_state',
            PrimaryIp='primary_ip4_address',
            PrimaryIp6='primary_ip6_address',
            SecondaryIp='secondary_ip4_address',
            SecondaryIp6='secondary_ip6_address',
            PrimaryIPVer='primary_ip_ver',
            SecondaryIPVer='secondary_ip_ver'
        )
    )
}

auto_write_exception = [GslbNewCfgRemSiteTable]

bean_state_map = {
    GslbInfoRemSiteTable: dict()
}


class GlobalRedirectionConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[GlobalRedirectionParameters]
    state_beans: ClassVar[Dict[DeviceBean, Dict]] = bean_state_map

    def __init__(self, alteon_connection):
        super(GlobalRedirectionConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: GlobalRedirectionParameters) -> GlobalRedirectionParameters:
        self._read_device_beans(parameters)
        if self._beans:
            parameters.no_server_dns_response_code = EnumDnsNoRespCode.enum(parameters.no_server_dns_response_code)
            return parameters

    def _update(self, parameters: GlobalRedirectionParameters, dry_run: bool) -> str:
        parameters.no_server_dns_response_code = self._enum_to_int(EnumDnsNoRespCode,
                                                                   parameters.no_server_dns_response_code)
        self._write_device_beans(parameters, dry_run=dry_run, direct_exclude=auto_write_exception)
        self._assign_write_numeric_index_beans(GslbNewCfgRemSiteTable, parameters.sites, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def delete(self, parameters: GlobalRedirectionParameters, dry_run=False, **kw) -> str:
        log.debug(' {0}: {1}, server: {2}, params: {3}'.format(self.__class__.__name__, self.DELETE.upper(), self.id,
                                                               parameters))
        sites = self._device_api.read_all(GslbNewCfgRemSiteTable())
        for site in sites:
            self._device_api.delete(site, dry_run=dry_run)
        gslb = GlobalRedirectionParameters()
        gslb.state = EnumGslbNewCfgGenState.off
        self.update(gslb, dry_run=dry_run)
        return 'Global redirection configuration' + MSG_DELETE

    def _update_remove(self, parameters: GlobalRedirectionParameters, dry_run: bool) -> str:
        self._remove_device_beans_by_struct_collection(parameters.sites, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(Root, parameters)

    def dry_run_delete_procedure(self, diff):
        dry_run_procedure = DryRunDeleteProcedure()
        dry_run_procedure.non_removable_bean_map_attrs_list.append(bean_map[Root]['attrs'])
        dry_run_procedure.ignore_prop_by_value.update(dict(state='off'))
        return dry_run_procedure

