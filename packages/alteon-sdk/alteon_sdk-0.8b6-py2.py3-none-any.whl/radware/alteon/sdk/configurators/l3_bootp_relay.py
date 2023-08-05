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


class BOOTPRelayParameters(RadwareParametersStruct):
    state: Optional[EnumIpNewCfgBootpState]
    primary_ip_address: Optional[str]
    secondary_ip_address: Optional[str]
    preserve_source_port: Optional[EnumIpNewCfgBootpPrsvPort]

    def __init__(self):
        self.state = None
        self.primary_ip_address = None
        self.secondary_ip_address = None
        self.preserve_source_port = None


bean_map = {
    Root: dict(
        struct=BOOTPRelayParameters,
        direct=True,
        attrs=dict(
            ipNewCfgBootpState='state',
            ipNewCfgBootpAddr='primary_ip_address',
            ipNewCfgBootpAddr2='secondary_ip_address',
            ipNewCfgBootpPrsvPort='preserve_source_port'
        )
    )
}


class BOOTPRelayConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[BOOTPRelayParameters]

    def __init__(self, alteon_connection):
        super(BOOTPRelayConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: BOOTPRelayParameters) -> BOOTPRelayParameters:
        self._read_device_beans(parameters)
        if self._beans:
            return parameters

    def _update(self, parameters: BOOTPRelayParameters, dry_run: bool) -> str:
        self._write_device_beans(parameters, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def delete(self, parameters: BOOTPRelayParameters, dry_run=False, **kw) -> str:
        bootp_params = BOOTPRelayParameters()
        bootp_params.state = EnumIpNewCfgBootpState.disabled
        bootp_params.primary_ip_address = '0.0.0.0'
        bootp_params.secondary_ip_address = '0.0.0.0'
        bootp_params.preserve_source_port = EnumIpNewCfgBootpPrsvPort.enabled
        self.update(bootp_params, dry_run=dry_run)
        return 'BOOTP Configuration' + MSG_DELETE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(Root, parameters)

    def dry_run_delete_procedure(self, diff):
        delete_values = dict(
            state='disabled',
            primary_ip_address='0.0.0.0',
            secondary_ip_address='0.0.0.0',
            preserve_source_port='enabled'
        )
        dry_run_procedure = DryRunDeleteProcedure()
        dry_run_procedure.ignore_prop_by_value = delete_values
        return dry_run_procedure

