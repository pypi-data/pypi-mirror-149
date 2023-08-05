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
from radware.alteon.sdk.alteon_managment import AlteonMngInfo
from radware.sdk.exceptions import DeviceConfiguratorError
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, MSG_DELETE, AlteonConfigurator
from radware.alteon.beans.Global import *
from typing import Optional, ClassVar


class LLDPParameters(RadwareParametersStruct):
    state: Optional[EnumLldpNewTxState]
    vendor_specific_tlv: Optional[EnumLldpNewVendtlv]
    tx_interval_second: Optional[int]
    tx_hold_multiplier: Optional[int]

    def __init__(self):
        self.state = None
        self.vendor_specific_tlv = None
        self.tx_interval_second = None
        self.tx_hold_multiplier = None


bean_map = {
    Root: dict(
        struct=LLDPParameters,
        direct=True,
        attrs=dict(
            lldpNewTxState='state',
            lldpNewVendtlv='vendor_specific_tlv',
            lldpNewTxInterval='tx_interval_second',
            lldpNewTxHold='tx_hold_multiplier',
        )
    )
}


class LLDPConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[LLDPParameters]

    def __init__(self, alteon_connection):
        super(LLDPConfigurator, self).__init__(bean_map, alteon_connection)
        self._mng_info = AlteonMngInfo(alteon_connection)

    def _read(self, parameters: LLDPParameters) -> LLDPParameters:
        if not self._mng_info.is_container:
            raise DeviceConfiguratorError(self.__class__, 'not a container')
        self._read_device_beans(parameters)
        if self._beans:
            return parameters

    def _update(self, parameters: LLDPParameters, dry_run: bool) -> str:
        if not self._mng_info.is_container:
            raise DeviceConfiguratorError(self.__class__, 'not a container')
        self._write_device_beans(parameters, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def delete(self, parameters: LLDPParameters, dry_run=False, **kw) -> str:
        if not self._mng_info.is_container:
            raise DeviceConfiguratorError(self.__class__, 'not a container')
        log.debug(' {0}: {1}, server: {2}, params: {3}'.format(self.__class__.__name__, self.DELETE.upper(), self.id,
                                                               parameters))
        lldp_params = LLDPParameters()
        lldp_params.state = EnumLldpNewTxState.disabled
        lldp_params.vendor_specific_tlv = EnumLldpNewVendtlv.enabled
        lldp_params.tx_interval_second = 30
        lldp_params.tx_hold_multiplier = 4
        self.update(lldp_params, dry_run=dry_run)
        return 'LLDP Configuration' + MSG_DELETE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(Root, parameters)

    def dry_run_delete_procedure(self, diff):
        delete_values = dict(
            state='disabled',
            vendor_specific_tlv='enabled',
            tx_interval_second=30,
            tx_hold_multiplier=4
        )
        dry_run_procedure = DryRunDeleteProcedure()
        dry_run_procedure.ignore_prop_by_value = delete_values
        return dry_run_procedure

