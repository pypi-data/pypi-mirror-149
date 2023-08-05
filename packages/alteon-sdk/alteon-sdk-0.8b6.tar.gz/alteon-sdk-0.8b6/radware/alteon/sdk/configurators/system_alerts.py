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
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, MSG_NO_DELETE, AlteonConfigurator
from radware.alteon.beans.Global import *
from typing import Optional, ClassVar


class SystemAlertsParameters(RadwareParametersStruct):
    threshold_detection_interval_minute: Optional[int]
    throughput_threshold_percent: Optional[int]
    ssl_cps_threshold_percent: Optional[int]
    compression_throughput_threshold_percent: Optional[int]
#    apm_pgpm_threshold_percent: Optional[int]
    session_table_critical_threshold_percent: Optional[int]
    session_table_high_threshold_percent: Optional[int]
    sp_high_utilization_threshold_percent: Optional[int]
    mp_high_utilization_threshold_percent: Optional[int]
    disk_critical_utilization_state: Optional[EnumAgSysDiskNewCfgCriEnable]
    disk_extremely_high_utilization_state: Optional[EnumAgSysDiskNewCfgExtEnable]
    disk_high_utilization_state: Optional[EnumAgSysDiskNewCfgHighEnable]
    disk_critical_utilization_threshold_percent: Optional[int]
    disk_extremely_high_utilization_threshold_percent: Optional[int]
    disk_high_utilization_threshold_percent: Optional[int]
    disk_critical_trap_interval_minute: Optional[int]
    disk_extremely_high_trap_interval_minute: Optional[int]
    disk_high_trap_interval_minute: Optional[int]

    def __init__(self):
        self.threshold_detection_interval_minute = None
        self.throughput_threshold_percent = None
        self.ssl_cps_threshold_percent = None
        self.compression_throughput_threshold_percent = None
#        self.apm_pgpm_threshold_percent = None
        self.session_table_critical_threshold_percent = None
        self.session_table_high_threshold_percent = None
        self.sp_high_utilization_threshold_percent = None
        self.mp_high_utilization_threshold_percent = None
        self.disk_critical_utilization_state = None
        self.disk_extremely_high_utilization_state = None
        self.disk_high_utilization_state = None
        self.disk_critical_utilization_threshold_percent = None
        self.disk_extremely_high_utilization_threshold_percent = None
        self.disk_high_utilization_threshold_percent = None
        self.disk_critical_trap_interval_minute = None
        self.disk_extremely_high_trap_interval_minute = None
        self.disk_high_trap_interval_minute = None


bean_map = {
    Root: dict(
        struct=SystemAlertsParameters,
        direct=True,
        attrs=dict(
            agNewCfgThresholdInterval='threshold_detection_interval_minute',
            agNewCfgThresholdThrput='throughput_threshold_percent',
            agNewCfgThresholdSSLCps='ssl_cps_threshold_percent',
            agNewCfgThresholdCompress='compression_throughput_threshold_percent',
#            agNewCfgThresholdApm='apm_pgpm_threshold_percent',
            agNewCfgThresholdSessTblCritical='session_table_critical_threshold_percent',
            agNewCfgThresholdSessTblHigh='session_table_high_threshold_percent',
            agNewCfgThresholdSPCpu='sp_high_utilization_threshold_percent',
            agNewCfgThresholdMPCpu='mp_high_utilization_threshold_percent',
            agSysDiskNewCfgCriEnable='disk_critical_utilization_state',
            agSysDiskNewCfgExtEnable='disk_extremely_high_utilization_state',
            agSysDiskNewCfgHighEnable='disk_high_utilization_state',
            agSysDiskNewCfgCriThreshold='disk_critical_utilization_threshold_percent',
            agSysDiskNewCfgExtThreshold='disk_extremely_high_utilization_threshold_percent',
            agSysDiskNewCfgHighThreshold='disk_high_utilization_threshold_percent',
            agSysDiskNewCfgCriInterval='disk_critical_trap_interval_minute',
            agSysDiskNewCfgExtInterval='disk_extremely_high_trap_interval_minute',
            agSysDiskNewCfgHighInterval='disk_high_trap_interval_minute',
        )
    )
}


class SystemAlertsConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[SystemAlertsParameters]

    def __init__(self, alteon_connection):
        super(SystemAlertsConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: SystemAlertsParameters) -> SystemAlertsParameters:
        self._read_device_beans(parameters)
        if self._beans:
            return parameters

    def _update(self, parameters: SystemAlertsParameters, dry_run: bool) -> str:
        self._write_device_beans(parameters, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def delete(self, parameters: SystemAlertsParameters, dry_run=False, **kw) -> str:
        return MSG_NO_DELETE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(Root, parameters)

    def dry_run_delete_procedure(self, diff):
        dry_run_procedure = DryRunDeleteProcedure()
        dry_run_procedure.ignore_all_props = True
        return dry_run_procedure

