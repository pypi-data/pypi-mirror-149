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
from typing import Optional, ClassVar


class SyslogHostEntry(RadwareParametersStruct):
    ip4_address: Optional[str]
    ip6_address: Optional[str]
    port: Optional[int]
    severity: Optional[EnumAgNewCfgSyslogSev]
    facility: Optional[EnumAgNewCfgSyslogFac]
    module: Optional[EnumAgNewCfgSyslogFeature]

    def __init__(self):
        self.ip4_address = None
        self.ip6_address = None
        self.port = None
        self.severity = None
        self.facility = None
        self.module = None

    def struct_normalization(self):
        self.clear_zero_ip_address()
        if self.facility.value == EnumAgNewCfgSyslogFac.local0.value:
            self.facility = None
        if self.module.value == EnumAgNewCfgSyslogFeature.all.value:
            self.module = None
        if self.port == 514:
            self.port = None
        if self.severity.value == EnumAgNewCfgSyslogSev.debug7.value:
            self.severity = None


class SyslogHosts(RadwareParametersStruct):
    host1: Optional[SyslogHostEntry]
    host2: Optional[SyslogHostEntry]
    host3: Optional[SyslogHostEntry]
    host4: Optional[SyslogHostEntry]
    host5: Optional[SyslogHostEntry]

    def __init__(self):
        self.host1 = SyslogHostEntry()
        self.host2 = SyslogHostEntry()
        self.host3 = SyslogHostEntry()
        self.host4 = SyslogHostEntry()
        self.host5 = SyslogHostEntry()


class SystemLoggingParameters(RadwareParametersStruct):
    show_syslog_on_console: Optional[EnumAgNewCfgConsole]
    configuration_audit: Optional[EnumAgNewCfgAuditTrail]
    extended_log_format: Optional[EnumAgNewCfgSyslogExtdlog]
    session_log_state: Optional[EnumAgNewCfgSyslogSessLog]
    session_log_server_data: Optional[EnumAgNewCfgSyslogSessLogFieldReal]
    session_log_nat_data: Optional[EnumAgNewCfgSyslogSessLogFieldNat]
    session_log_mode: Optional[EnumAgNewCfgSyslogSessLogMode]
    log_trap_system: Optional[EnumAgNewCfgSyslogTrapSystem]
    log_trap_spanning_tree: Optional[EnumAgNewCfgSyslogTrapStp]
    log_trap_vlan: Optional[EnumAgNewCfgSyslogTrapVlan]
    log_trap_virtual_services: Optional[EnumAgNewCfgSyslogTrapSlb]
    log_trap_security: Optional[EnumAgNewCfgSyslogTrapSecurity]
    log_trap_management: Optional[EnumAgNewCfgSyslogTrapMgmt]
    log_trap_vrrp: Optional[EnumAgNewCfgSyslogTrapVrrp]
    log_trap_filter: Optional[EnumAgNewCfgSyslogTrapFilter]
    log_trap_ip_reputation: Optional[EnumAgNewCfgSyslogTrapIprep]
    log_trap_cli: Optional[EnumAgNewCfgSyslogTrapCli]
    log_trap_ip: Optional[EnumAgNewCfgSyslogTrapIp]
    log_trap_global_lb: Optional[EnumAgNewCfgSyslogTrapGslb]
    log_trap_ssh: Optional[EnumAgNewCfgSyslogTrapSsh]
    log_trap_ipv6: Optional[EnumAgNewCfgSyslogTrapIpv6]
    log_trap_syn_attack: Optional[EnumAgNewCfgSyslogTrapSynAtk]
    log_trap_ntp: Optional[EnumAgNewCfgSyslogTrapNtp]
    log_trap_ospf: Optional[EnumAgNewCfgSyslogTrapOspf]
    log_trap_app_services: Optional[EnumAgNewCfgSyslogTrapAppSvc]
    log_trap_web: Optional[EnumAgNewCfgSyslogTrapWeb]
    log_trap_ospf_v3: Optional[EnumAgNewCfgSyslogTrapOspfv3]
    log_trap_slb_attack: Optional[EnumAgNewCfgSyslogTrapSlbAtk]
    log_trap_audit: Optional[EnumAgNewCfgSyslogTrapAudit]
    log_trap_bgp: Optional[EnumAgNewCfgSyslogTrapBgp]
    log_trap_fastview: Optional[EnumAgNewCfgSyslogTrapFastView]
    log_trap_rate_limit: Optional[EnumAgNewCfgSyslogTrapTcpLim]
    log_trap_high_availability: Optional[EnumAgNewCfgSyslogTrapHA]
    log_trap_rmon: Optional[EnumAgNewCfgSyslogTrapRmon]
    log_trap_console: Optional[EnumAgNewCfgSyslogTrapConsole]
    syslog_servers: Optional[SyslogHosts]

    def __init__(self):
        self.show_syslog_on_console = None
        self.configuration_audit = None
        self.extended_log_format = None
        self.session_log_state = None
        self.session_log_server_data = None
        self.session_log_nat_data = None
        self.session_log_mode = None
        self.log_trap_system = None
        self.log_trap_spanning_tree = None
        self.log_trap_vlan = None
        self.log_trap_virtual_services = None
        self.log_trap_security = None
        self.log_trap_management = None
        self.log_trap_vrrp = None
        self.log_trap_filter = None
        self.log_trap_ip_reputation = None
        self.log_trap_cli = None
        self.log_trap_ip = None
        self.log_trap_global_lb = None
        self.log_trap_ssh = None
        self.log_trap_ipv6 = None
        self.log_trap_syn_attack = None
        self.log_trap_ntp = None
        self.log_trap_ospf = None
        self.log_trap_app_services = None
        self.log_trap_web = None
        self.log_trap_ospf_v3 = None
        self.log_trap_slb_attack = None
        self.log_trap_audit = None
        self.log_trap_bgp = None
        self.log_trap_fastview = None
        self.log_trap_rate_limit = None
        self.log_trap_high_availability = None
        self.log_trap_rmon = None
        self.log_trap_console = None
        self.syslog_servers = SyslogHosts()


syslog_hosts = dict(
    host1=dict(
        agNewCfgSyslogHost='ip4_address',
        agNewCfgSyslogHostv6='ip6_address',
        agNewCfgSyslogPort='port',
        agNewCfgSyslogSev='severity',
        agNewCfgSyslogFac='facility',
        agNewCfgSyslogFeature='module'
    ),
    host2=dict(
        agNewCfgSyslog2Host='ip4_address',
        agNewCfgSyslog2Hostv6='ip6_address',
        agNewCfgSyslog2Port='port',
        agNewCfgSyslog2Sev='severity',
        agNewCfgSyslog2Fac='facility',
        agNewCfgSyslog2Feature='module'
    ),
    host3=dict(
        agNewCfgSyslog3Host='ip4_address',
        agNewCfgSyslog3Hostv6='ip6_address',
        agNewCfgSyslog3Port='port',
        agNewCfgSyslog3Sev='severity',
        agNewCfgSyslog3Fac='facility',
        agNewCfgSyslog3Feature='module'
    ),
    host4=dict(
        agNewCfgSyslog4Host='ip4_address',
        agNewCfgSyslog4Hostv6='ip6_address',
        agNewCfgSyslog4Port='port',
        agNewCfgSyslog4Sev='severity',
        agNewCfgSyslog4Fac='facility',
        agNewCfgSyslog4Feature='module'
    ),
    host5=dict(
        agNewCfgSyslog5Host='ip4_address',
        agNewCfgSyslog5Hostv6='ip6_address',
        agNewCfgSyslog5Port='port',
        agNewCfgSyslog5Sev='severity',
        agNewCfgSyslog5Fac='facility',
        agNewCfgSyslog5Feature='module'
    )

)


bean_map = {
    Root: dict(
        struct=SystemLoggingParameters,
        direct=True,
        attrs=dict(
            agNewCfgConsole='show_syslog_on_console',
            agNewCfgAuditTrail='configuration_audit',
            agNewCfgSyslogExtdlog='extended_log_format',
            agNewCfgSyslogSessLog='session_log_state',
            agNewCfgSyslogSessLogFieldReal='session_log_server_data',
            agNewCfgSyslogSessLogFieldNat='session_log_nat_data',
            agNewCfgSyslogSessLogMode='session_log_mode',
            agNewCfgSyslogTrapSystem='log_trap_system',
            agNewCfgSyslogTrapStp='log_trap_spanning_tree',
            agNewCfgSyslogTrapVlan='log_trap_vlan',
            agNewCfgSyslogTrapSlb='log_trap_virtual_services',
            agNewCfgSyslogTrapSecurity='log_trap_security',
            agNewCfgSyslogTrapMgmt='log_trap_management',
            agNewCfgSyslogTrapVrrp='log_trap_vrrp',
            agNewCfgSyslogTrapFilter='log_trap_filter',
            agNewCfgSyslogTrapIprep='log_trap_ip_reputation',
            agNewCfgSyslogTrapCli='log_trap_cli',
            agNewCfgSyslogTrapIp='log_trap_ip',
            agNewCfgSyslogTrapGslb='log_trap_global_lb',
            agNewCfgSyslogTrapSsh='log_trap_ssh',
            agNewCfgSyslogTrapIpv6='log_trap_ipv6',
            agNewCfgSyslogTrapSynAtk='log_trap_syn_attack',
            agNewCfgSyslogTrapNtp='log_trap_ntp',
            agNewCfgSyslogTrapOspf='log_trap_ospf',
            agNewCfgSyslogTrapAppSvc='log_trap_app_services',
            agNewCfgSyslogTrapWeb='log_trap_web',
            agNewCfgSyslogTrapOspfv3='log_trap_ospf_v3',
            agNewCfgSyslogTrapSlbAtk='log_trap_slb_attack',
            agNewCfgSyslogTrapAudit='log_trap_audit',
            agNewCfgSyslogTrapBgp='log_trap_bgp',
            agNewCfgSyslogTrapFastView='log_trap_fastview',
            agNewCfgSyslogTrapTcpLim='log_trap_rate_limit',
            agNewCfgSyslogTrapHA='log_trap_high_availability',
            agNewCfgSyslogTrapRmon='log_trap_rmon',
            agNewCfgSyslogTrapConsole='log_trap_console',
        )
    )
}


class SystemLoggingConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[SystemLoggingParameters]

    def __init__(self, alteon_connection):
        super(SystemLoggingConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: SystemLoggingParameters) -> SystemLoggingParameters:
        self._read_device_beans(parameters)
        if self._beans:
            parameters.syslog_servers = self._read_syslog_servers()
            return parameters

    def _update(self, parameters: SystemLoggingParameters, dry_run: bool) -> str:
        if parameters.syslog_servers:
            for k, v in parameters.syslog_servers.__dict__.items():
                if v:
                    v.clear_zero_ip_address()
        self._write_device_beans(parameters, dry_run=dry_run)
        self._write_syslog_servers(parameters.syslog_servers, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _read_syslog_servers(self):
        root_syslog = Root()
        for k, v in syslog_hosts.items():
            for k2, v2 in v.items():
                setattr(root_syslog, k2, READ_PROP)
        syslog_config = self._device_api.read(root_syslog)
        syslog_servers = SyslogHosts()
        for k, v in syslog_hosts.items():
            host_val = getattr(syslog_servers, k)
            for k2, v2 in v.items():
                setattr(host_val, v2, getattr(syslog_config, k2))
        return syslog_servers

    def _write_syslog_servers(self, syslog_servers, dry_run):
        if syslog_servers is not None:
            root_syslog = Root()
            attr_was_set = 0
            for k, v in syslog_servers.__dict__.items():
                 if v is not None:
                     for k2, v2 in v.__dict__.items():
                         if v2 is not None:
                             root_key = None
                             for k3, v3 in syslog_hosts[k].items():
                                 if v3 == k2:
                                     root_key = k3
                             setattr(root_syslog, root_key, v2)
                             attr_was_set = 1
            if attr_was_set == 1:
                self._device_api.update(root_syslog, dry_run=dry_run)

    def delete(self, parameters: SystemLoggingParameters, dry_run=False, **kw) -> str:
        log.debug(' {0}: {1}, server: {2}, params: {3}'.format(self.__class__.__name__, self.DELETE.upper(), self.id,
                                                               parameters))
        syslog_servers = self._read_syslog_servers()
        for k, v in syslog_servers.__dict__.items():
            v.ip4_address = "0.0.0.0"
            v.port = 514
            v.severity = EnumAgNewCfgSyslogSev.debug7
            v.facility = EnumAgNewCfgSyslogFac.local0
            v.module = EnumAgNewCfgSyslogFeature.all
        self._write_syslog_servers(syslog_servers, dry_run=dry_run)
        return 'Syslog servers' + MSG_DELETE

    def _update_remove(self, parameters: SystemLoggingParameters, dry_run: bool) -> str:
        if parameters.syslog_servers:
            for k, v in parameters.syslog_servers.__dict__.items():
                v.ip4_address = "0.0.0.0"
                v.port = 514
                v.severity = EnumAgNewCfgSyslogSev.debug7
                v.facility = EnumAgNewCfgSyslogFac.local0
                v.module = EnumAgNewCfgSyslogFeature.all
            self._write_syslog_servers(parameters.syslog_servers, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(Root, parameters)

    def dry_run_delete_procedure(self, diff):
        dry_run_procedure = DryRunDeleteProcedure()
        dry_run_procedure.non_removable_bean_map_attrs_list.append(bean_map[Root]['attrs'])
        if 'syslog_servers' in diff:
            syslogs = dict()
            for k, v in diff['syslog_servers'].items():
                if (v['ip4_address'] != '0.0.0.0'
                        or v['ip6_address'] != '0:0:0:0:0:0:0:0' or v['severity'] != EnumAgNewCfgSyslogSev.debug7.name
                        or v['facility'] != EnumAgNewCfgSyslogFac.local0.name or
                        v["module"] != EnumAgNewCfgSyslogFeature.all.name):
                    syslogs[k] = v
            if syslogs:
                diff['syslog_servers'] = syslogs
            else:
                diff.pop('syslog_servers')
        return dry_run_procedure
