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


class SystemTimeDateParameters(RadwareParametersStruct):
    date_mm_dd_yyyy: Optional[str]
    time_hh_mm_ss: Optional[str]
    time_zone: Optional[EnumAgNewDaylightSavings]
    ntp_state: Optional[EnumAgNewCfgNTPService]
    ntp_primary_ip4: Optional[str]
    ntp_secondary_ip4: Optional[str]
    ntp_primary_ip6: Optional[str]
    ntp_secondary_ip6: Optional[str]
    ntp_sync_interval_minute: Optional[int]
    gmt_timezone_offset_hh_mm: Optional[str]

    def __init__(self):
        self.date_mm_dd_yyyy = None
        self.time_hh_mm_ss = None
        self.time_zone = None
        self.ntp_state = None
        self.ntp_primary_ip4 = None
        self.ntp_secondary_ip4 = None
        self.ntp_primary_ip6 = None
        self.ntp_secondary_ip6 = None
        self.ntp_sync_interval_minute = None
        self.gmt_timezone_offset_hh_mm = None


bean_map = {
    Root: dict(
        struct=SystemTimeDateParameters,
        direct=True,
        attrs=dict(
            agRtcDate='date_mm_dd_yyyy',
            agRtcTime='time_hh_mm_ss',
            agNewDaylightSavings='time_zone',
            agNewCfgNTPService='ntp_state',
            agNewCfgNTPServer='ntp_primary_ip4',
            agNewCfgNTPSecServer='ntp_secondary_ip4',
            agNewCfgNTPServerIpv6Addr='ntp_primary_ip6',
            agNewCfgNTPSecServerIpv6Addr='ntp_secondary_ip6',
            agNewCfgNTPResyncInterval='ntp_sync_interval_minute',
            agNewCfgNTPTzoneHHMM='gmt_timezone_offset_hh_mm'
        )
    )
}


class SystemTimeDateConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[SystemTimeDateParameters]

    def __init__(self, alteon_connection):
        super(SystemTimeDateConfigurator, self).__init__(bean_map, alteon_connection)
        self._mng_info = AlteonMngInfo(alteon_connection)

    def _read(self, parameters: SystemTimeDateParameters) -> SystemTimeDateParameters:
        if not self._mng_info.is_container:
            raise DeviceConfiguratorError(self.__class__, 'not a container')
        self._read_device_beans(parameters)
        if self._beans:
            return parameters

    def _update(self, parameters: SystemTimeDateParameters, dry_run: bool) -> str:
        if not self._mng_info.is_container:
            raise DeviceConfiguratorError(self.__class__, 'not a container')
        self._write_device_beans(parameters, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def delete(self, parameters: SystemTimeDateParameters, dry_run=False, **kw) -> str:
        if not self._mng_info.is_container:
            raise DeviceConfiguratorError(self.__class__, 'not a container')
        ntp_params = SystemTimeDateParameters()
        ntp_params.ntp_state = EnumAgNewCfgNTPService.disabled
        ntp_params.ntp_primary_ip4 = '0.0.0.0'
        ntp_params.ntp_secondary_ip4 = '0.0.0.0'
        ntp_params.ntp_sync_interval_minute = 1440
        ntp_params.gmt_timezone_offset_hh_mm = '-08:00'
        self.update(ntp_params, dry_run=dry_run)
        return 'NTP configuration' + MSG_DELETE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(Root, parameters)

    def dry_run_delete_procedure(self, diff):
        delete_values = dict(
            ntp_state='disabled',
            ntp_primary_ip4='0.0.0.0',
            ntp_secondary_ip4='0.0.0.0',
            ntp_sync_interval_minute=1440,
            gmt_timezone_offset_hh_mm='-08:00'
        )
        dry_run_procedure = DryRunDeleteProcedure()
        dry_run_procedure.non_removable_bean_map_attrs_list.append(bean_map[Root]['attrs'])
        dry_run_procedure.ignore_prop_by_value = delete_values
        return dry_run_procedure

