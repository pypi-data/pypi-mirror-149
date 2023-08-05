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
from radware.alteon.sdk.alteon_managment import AlteonMngInfo
from radware.alteon.beans.Global import *
from typing import Optional, ClassVar


class EnumSnmpEnableAuthenTraps(BaseBeanEnum):
    enabled = 1
    disabled = 2


class SystemSNMPParameters(RadwareParametersStruct):
    snmp_access_level: Optional[EnumAgAccessNewCfgSnmpAccess]
    snmp_v1_v2_state: Optional[EnumAgAccessNewCfgSnmpV1V2Access]
    read_community: Optional[str]
    write_community: Optional[str]
    trap_source_interface: Optional[int]
    trap_ip4_host1: Optional[str]
    trap_ip4_host2: Optional[str]
    trap_ip6_host1: Optional[str]
    trap_ip6_host2: Optional[str]
    authentication_failure_traps: Optional[EnumSnmpEnableAuthenTraps]
    system_name: Optional[str]
    system_location: Optional[str]
    system_contact: Optional[str]

    def __init__(self):
        self.snmp_access_level = None
        self.snmp_v1_v2_state = None
        self.read_community = None
        self.write_community = None
        self.trap_source_interface = None
        self.trap_ip4_host1 = None
        self.trap_ip4_host2 = None
        self.trap_ip6_host1 = None
        self.trap_ip6_host2 = None
        self.authentication_failure_traps = None
        self.system_name = None
        self.system_location = None
        self.system_contact = None


bean_map = {
    Root: dict(
        struct=SystemSNMPParameters,
        direct=True,
        attrs=dict(
            sysName='system_name',
            sysLocation='system_location',
            sysContact='system_contact',
            snmpEnableAuthenTraps='authentication_failure_traps',

            agAccessNewCfgSnmpAccess='snmp_access_level',
            agAccessNewCfgSnmpV1V2Access='snmp_v1_v2_state',
            agAccessNewCfgSnmpReadComm='read_community',
            agAccessNewCfgSnmpWriteComm='write_community',
            #agNewCfgTrapSrcIf='trap_source_interface',
            agAccessNewCfgSnmpTrap1='trap_ip4_host1',
            agAccessNewCfgSnmpTrap2='trap_ip4_host2',
            agAccessNewCfgSnmpTrap1Ipv6Addr='trap_ip6_host1',
            agAccessNewCfgSnmpTrap2Ipv6Addr='trap_ip6_host2',
        )
    )
}


class SystemSNMPConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[SystemSNMPParameters]

    def __init__(self, alteon_connection):
        super(SystemSNMPConfigurator, self).__init__(bean_map, alteon_connection)
        self._mng_info = AlteonMngInfo(alteon_connection)

    def _read(self, parameters: SystemSNMPParameters) -> SystemSNMPParameters:
        self._read_device_beans(parameters)

        if not self._mng_info.is_vx:
            root = Root()
            root.agNewCfgTrapSrcIf = READ_PROP
            parameters.trap_source_interface = self._device_api.read(root).agNewCfgTrapSrcIf
            #TODO - remove when MIB is consistent, uncomment bean_map / agNewCfgTrapSrcIf

        if self._beans:
            return parameters

    def _update(self, parameters: SystemSNMPParameters, dry_run: bool) -> str:
        if self._mng_info.is_vx:
            parameters.trap_source_interface = None
            #TODO - remove when MIB is consistent

        self._write_device_beans(parameters, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def delete(self, parameters: SystemSNMPParameters, dry_run=False, **kw) -> str:
        snmp_params = SystemSNMPParameters()
        snmp_params.read_community = 'public'
        snmp_params.write_community = 'private'
        snmp_params.snmp_access_level = EnumAgAccessNewCfgSnmpAccess.disabled
        snmp_params.trap_ip4_host1 = '0.0.0.0'
        snmp_params.trap_ip4_host2 = '0.0.0.0'
        #snmp_params.trap_ip6_host1 = ''
        #snmp_params.trap_ip6_host2 = ''
        snmp_params.system_name = ''
        snmp_params.system_contact = ''
        snmp_params.system_location = ''
        snmp_params.authentication_failure_traps = EnumSnmpEnableAuthenTraps.disabled
        self.update(snmp_params, dry_run=dry_run)
        return 'SNMP configuration' + MSG_DELETE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(Root, parameters)

    def dry_run_delete_procedure(self, diff):
        delete_values = dict(
            read_community='public',
            write_community='private',
            snmp_access_level='disabled',
            trap_ip4_host1='0.0.0.0',
            trap_ip4_host2='0.0.0.0',
            authentication_failure_traps='disabled',
            system_name='',
            system_contact='',
            system_location=''
        )
        dry_run_procedure = DryRunDeleteProcedure()
        dry_run_procedure.non_removable_bean_map_attrs_list.append(bean_map[Root]['attrs'])
        dry_run_procedure.ignore_prop_by_value = delete_values
        return dry_run_procedure

