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
from typing import List, Optional, ClassVar
from radware.sdk.exceptions import DeviceConfiguratorError


class SnmpGeneralParameters(RadwareParametersStruct):
    snmp_access: Optional[EnumAgAccessNewCfgSnmpAccess]
    snmp_v1v2_access: Optional[EnumAgAccessNewCfgSnmpV1V2Access]
    sys_name: Optional[str]
    sys_location: Optional[str]
    sys_contact: Optional[str]
    snmp_read_comm: Optional[str]
    snmp_write_comm: Optional[str]
    trap_src_if: Optional[int]
    snmp_timeout: Optional[int]
    snmp_trap1_ipv6_addr: Optional[str]
    snmp_trap1: Optional[str]
    snmp_trap2_ipv6_addr: Optional[str]
    snmp_trap2: Optional[str]
    auth_ena_traps: Optional[EnumSnmpEnableAuthenTraps]


    def __init__(self):
        self.snmp_access = None
        self.snmp_v1v2_access = None
        self.sys_name = None
        self.sys_location = None
        self.sys_contact = None
        self.snmp_read_comm = None
        self.snmp_write_comm = None
        self.trap_src_if = None
        self.snmp_timeout = None
        self.snmp_trap1_ipv6_addr = None
        self.snmp_trap1 = None
        self.snmp_trap2_ipv6_addr = None
        self.snmp_trap2 = None
        self.auth_ena_traps = None


bean_map = {
    Root: dict(
        struct=SnmpGeneralParameters,
        direct=True,
        attrs=dict(
            agAccessNewCfgSnmpAccess='snmp_access',
            agAccessNewCfgSnmpV1V2Access='snmp_v1v2_access',
            sysName='sys_name',
            sysLocation='sys_location',
            sysContact='sys_contact',
            agAccessNewCfgSnmpReadComm='snmp_read_comm',
            agAccessNewCfgSnmpWriteComm='snmp_write_comm',
            agNewCfgTrapSrcIf='trap_src_if',
            agNewCfgSnmpTimeout='snmp_timeout',
            agAccessNewCfgSnmpTrap1Ipv6Addr='snmp_trap1_ipv6_addr',	
            agAccessNewCfgSnmpTrap1='snmp_trap1',
            agAccessNewCfgSnmpTrap2Ipv6Addr='snmp_trap2_ipv6_addr',
            agAccessNewCfgSnmpTrap2='snmp_trap2',
            snmpEnableAuthenTraps='auth_ena_traps',
        )
    )
}


class SnmpGeneralConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[SnmpGeneralParameters]

    def __init__(self, alteon_connection):
        super(SnmpGeneralConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: SnmpGeneralParameters) -> SnmpGeneralParameters:
        self._read_device_beans(parameters)
        if self._beans:
            return parameters

    def _update(self, parameters: SnmpGeneralParameters, dry_run: bool) -> str:
        if parameters.trap_src_if is not None:
            if parameters.trap_src_if > 256:
                raise DeviceConfiguratorError(self.__class__, 'SNMP trap source interface must be between 1 and 256')
        if parameters.snmp_timeout is not None:
            if parameters.snmp_timeout > 30:
                raise DeviceConfiguratorError(self.__class__, 'timeout for the SNMP state machine must be between 1 and 30')
        self._write_device_beans(parameters, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(Root, parameters)

