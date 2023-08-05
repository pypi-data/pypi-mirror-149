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
from radware.sdk.common import RadwareParametersStruct, PasswordArgument
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, MSG_NO_DELETE, AlteonConfigurator
from radware.alteon.beans.Global import *
from typing import Optional, ClassVar


class SystemTacacsAuthenticationParameters(RadwareParametersStruct):
    state: Optional[EnumTacNewCfgState]
    port: Optional[int]
    primary_ip4_address: Optional[str]
    secondary_ip4_address: Optional[str]
    primary_ip6_address: Optional[str]
    secondary_ip6_address: Optional[str]
    timeout_second: Optional[int]
    retries: Optional[int]
    primary_secret: Optional[PasswordArgument]
    secondary_secret: Optional[PasswordArgument]
    local_user_priority: Optional[EnumTacNewCfgLocalAuth]
    local_user_fallback: Optional[EnumTacNewCfgSecBd]
    command_authorization: Optional[EnumTacNewCfgCmdAuthor]
    command_logging: Optional[EnumTacNewCfgCmdLogging]
    privilege_level_mapping: Optional[EnumTacNewCfgCmap]
    command_logging_type: Optional[EnumTacNewCfgClogname]
    otp: Optional[EnumTacNewCfgOtp]

    def __init__(self):
        self.state = None
        self.port = None
        self.primary_ip4_address = None
        self.secondary_ip4_address = None
        self.primary_ip6_address = None
        self.secondary_ip6_address = None
        self.timeout_second = None
        self.retries = None
        self.primary_secret = None
        self.secondary_secret = None
        self.local_user_priority = None
        self.local_user_fallback = None
        self.command_authorization = None
        self.command_logging = None
        self.privilege_level_mapping = None
        self.command_logging_type = None
        self.otp = None


bean_map = {
    Root: dict(
        struct=SystemTacacsAuthenticationParameters,
        direct=True,
        attrs=dict(
            tacNewCfgState='state',
            tacNewCfgPort='port',
            tacNewCfgPrimaryIpAddr='primary_ip4_address',
            tacNewCfgSecondaryIpAddr='secondary_ip4_address',
            tacNewCfgPrimaryIpv6Addr='primary_ip6_address',
            tacNewCfgSecondaryIpv6Addr='secondary_ip6_address',
            tacNewCfgTimeout='timeout_second',
            tacNewCfgRetries='retries',
            tacNewCfgAuthenString='primary_secret',
            tacNewCfgAuthenSecondString='secondary_secret',
            tacNewCfgLocalAuth='local_user_priority',
            tacNewCfgSecBd='local_user_fallback',
            tacNewCfgCmdAuthor='command_authorization',
            tacNewCfgCmdLogging='command_logging',
            tacNewCfgCmap='privilege_level_mapping',
            tacNewCfgClogname='command_logging_type',
            tacNewCfgOtp='otp'
        )
    )
}


class SystemTacacsAuthenticationConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[SystemTacacsAuthenticationParameters]

    def __init__(self, alteon_connection):
        super(SystemTacacsAuthenticationConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: SystemTacacsAuthenticationParameters) -> SystemTacacsAuthenticationParameters:
        self._read_device_beans(parameters)
        if self._beans:
            return parameters

    def _update(self, parameters: SystemTacacsAuthenticationParameters, dry_run: bool) -> str:
        self._write_device_beans(parameters, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def delete(self, parameters: SystemTacacsAuthenticationParameters, dry_run=False, **kw) -> str:
        return MSG_NO_DELETE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(Root, parameters)

    def dry_run_delete_procedure(self, diff):
        dry_run_procedure = DryRunDeleteProcedure()
        dry_run_procedure.ignore_all_props = True
        return dry_run_procedure

