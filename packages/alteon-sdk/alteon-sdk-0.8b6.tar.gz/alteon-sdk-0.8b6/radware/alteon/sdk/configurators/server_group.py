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


from radware.sdk.common import RadwareParametersStruct
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, AlteonConfigurator
from radware.alteon.beans.SlbNewCfgEnhGroupTable import *
from radware.alteon.beans.SlbNewCfgEnhGroupRealServerTable import *
from typing import List, Optional, ClassVar


class ServerGroupParameters(RadwareParametersStruct):
    index: str
    slb_metric: Optional[EnumSlbGroupMetric]
    slb_rport_metric: Optional[EnumSlbGroupRmetric]
    backup_server_name: Optional[str]
    backup_group_name: Optional[str]
    secondary_backup_group_name: Optional[str]
    backup_type: Optional[EnumSlbGroupBackupType]
    vip_health_check_mode: Optional[EnumSlbGroupVipHealthCheck]
    persist_hash_mask: Optional[str]
    slow_start_time_second: Optional[int]
    ip_ver: Optional[EnumSlbGroupIpVer]
    health_check_id: Optional[str]
    group_server_type: Optional[EnumSlbGroupType]
    persist_overload_max_conn_server: Optional[EnumSlbGroupMaxConEx]
    server_names: Optional[List[str]]
    name: Optional[str]

    def __init__(self, index: str = None):
        self.index = index
        self.slb_metric = None
        self.slb_rport_metric = None
        self.backup_server_name = None
        self.backup_group_name = None
        self.secondary_backup_group_name = None
        self.backup_type = None
        self.vip_health_check_mode = None
        self.persist_hash_mask = None
        self.slow_start_time_second = None
        self.ip_ver = None
        self.health_check_id = None
        self.group_server_type = None
        self.persist_overload_max_conn_server = None
        self.server_names = None
        self.name = None


bean_map = {
    SlbNewCfgEnhGroupTable: dict(
        struct=ServerGroupParameters,
        direct=True,
        attrs=dict(
            Index='index',
            Metric='slb_metric',
            Rmetric='slb_rport_metric',
            BackupServer='backup_server_name',
            BackupGroup='backup_group_name',
            SecBackupGroup='secondary_backup_group_name',
            BackupType='backup_type',
            VipHealthCheck='vip_health_check_mode',
            PhashMask='persist_hash_mask',
            Slowstart='slow_start_time_second',
            IpVer='ip_ver',
            HealthID='health_check_id',
            Type='group_server_type',
            MaxConEx='persist_overload_max_conn_server',
            Name="name"
        )
    ),
    SlbNewCfgEnhGroupRealServerTable: dict(
        struct=List[ServerGroupParameters],
        direct=False,
        attrs=dict(
            RealServGroupIndex='index'
        )
    )
}


class ServerGroupConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[ServerGroupParameters]

    def __init__(self, alteon_connection):
        super(ServerGroupConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: ServerGroupParameters) -> ServerGroupParameters:
        self._read_device_beans(parameters)
        if self._beans:
            parameters.server_names = list()
            for server_entry in self._beans[SlbNewCfgEnhGroupRealServerTable]:
                parameters.server_names.append(server_entry.ServIndex)
            return parameters

    def _update(self, parameters: ServerGroupParameters, dry_run: bool) -> str:
        self._write_device_beans(parameters, dry_run=dry_run)
        if parameters.server_names:
            for server in parameters.server_names:
                server_entry = self._get_bean_instance(SlbNewCfgEnhGroupTable, parameters)
                server_entry.AddServer = server
                self._device_api.update(server_entry, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _update_remove(self, parameters: ServerGroupParameters, dry_run: bool) -> str:
        if parameters.server_names:
            for server in parameters.server_names:
                server_entry = self._get_bean_instance(SlbNewCfgEnhGroupTable, parameters)
                server_entry.RemoveServer = server
                self._device_api.update(server_entry, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(SlbNewCfgEnhGroupTable, parameters)


