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
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, MSG_DELETE, AlteonConfigurator
from radware.sdk.exceptions import DeviceConfiguratorError
from radware.alteon.beans.Global import *
from radware.alteon.beans.LacpNewPortCfgTable import *
from radware.alteon.beans.LacpInfoPortTable import LacpInfoPortTable
from typing import List, Optional, ClassVar, Dict


class AggregationGroup(RadwareParametersStruct):
    id: int
    state: EnumLacpPortState
    ports: List[int]

    def __init__(self, group_id: int = None, state: EnumLacpPortState = None):
        self.id = group_id
        self.state = state
        self.ports = list()


class LACPAggregationParameters(RadwareParametersStruct):
    lacp_system_name: Optional[str]
    timeout_mode: Optional[EnumLacpNewSystemTimeoutTime]
    block_port_outside_of_aggr: Optional[EnumLacpNewBlockPort]
    system_priority: Optional[int]
    groups: Optional[List[AggregationGroup]]

    def __init__(self):
        self.lacp_system_name = None
        self.timeout_mode = None
        self.block_port_outside_of_aggr = None
        self.system_priority = None
        self.groups = list()


bean_map = {
    Root: dict(
        struct=LACPAggregationParameters,
        direct=True,
        attrs=dict(
            lacpNewSystemName='lacp_system_name',
            lacpNewSystemTimeoutTime='timeout_mode',
            lacpNewBlockPort='block_port_outside_of_aggr',
            lacpNewSystemPriority='system_priority'
        )
    )
}

bean_state_map = {
    LacpInfoPortTable: dict()
}


class LACPAggregationConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[LACPAggregationParameters]
    state_beans: ClassVar[Dict[DeviceBean, Dict]] = bean_state_map

    def __init__(self, alteon_connection):
        super(LACPAggregationConfigurator, self).__init__(bean_map, alteon_connection)
        self._mng_info = AlteonMngInfo(alteon_connection)

    def _read(self, parameters: LACPAggregationParameters) -> LACPAggregationParameters:
        if not self._mng_info.is_container:
            raise DeviceConfiguratorError(self.__class__, 'not a container')
        self._read_device_beans(parameters)
        if self._beans:
            group_map = dict()
            for lacp_port_entry in self._device_api.read_all(LacpNewPortCfgTable()):
                if lacp_port_entry.State != EnumLacpPortState.off:
                    if lacp_port_entry.ActorAdminKey in group_map:
                        group_data = group_map[lacp_port_entry.ActorAdminKey]
                        if group_data['state'] != lacp_port_entry.State:
                            raise DeviceConfiguratorError(self.__class__, 'lacp group {0} mixed lacp port state'.format(
                                lacp_port_entry.ActorAdminKey))
                        group_data['ports'].append(lacp_port_entry.Id)
                    else:
                        group_map.update({lacp_port_entry.ActorAdminKey: dict(
                                state=lacp_port_entry.State,
                                ports=[lacp_port_entry.Id]
                            )}
                        )
            parameters.groups = list()
            for k, v in group_map.items():
                new_aggr = AggregationGroup()
                new_aggr.id = k
                new_aggr.state = v['state']
                new_aggr.ports = v['ports']
                parameters.groups.append(new_aggr)
            return parameters

    def _update(self, parameters: LACPAggregationParameters, dry_run: bool) -> str:
        if not self._mng_info.is_container:
            raise DeviceConfiguratorError(self.__class__, 'not a container')
        self._write_device_beans(parameters, dry_run=dry_run)
        for group in parameters.groups:
            for port in group.ports:
                instance = LacpNewPortCfgTable()
                instance.Id = port
                instance.State = EnumLacpPortState.enum(group.state)
                instance.ActorAdminKey = group.id
                self._device_api.update(instance, dry_run=dry_run)

        return self._get_object_id(parameters) + MSG_UPDATE

    def delete(self, parameters: LACPAggregationParameters, dry_run=False, **kw) -> str:
        if not self._mng_info.is_container:
            raise DeviceConfiguratorError(self.__class__, 'not a container')
        log.debug(' {0}: {1}, server: {2}, params: {3}'.format(self.__class__.__name__, self.DELETE.upper(), self.id,
                                                               parameters))
        for lacp_port_entry in self._device_api.read_all(LacpNewPortCfgTable()):
            instance = LacpNewPortCfgTable()
            instance.Id = lacp_port_entry.Id
            instance.State = EnumLacpPortState.off
            instance.ActorAdminKey = instance.Id
            self._device_api.update(instance, dry_run=dry_run)
        return 'LACP aggregation groups' + MSG_DELETE

    def _update_remove(self, parameters: LACPAggregationParameters, dry_run: bool) -> str:
        if parameters.groups:
            for group in parameters.groups:
                if group.ports:
                    for port in group.ports:
                        instance = LacpNewPortCfgTable()
                        instance.Id = port
                        instance.State = EnumLacpPortState.off
                        instance.ActorAdminKey = port
                        self._device_api.update(instance, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(Root, parameters)

    def dry_run_delete_procedure(self, diff):
        dry_run_procedure = DryRunDeleteProcedure()
        dry_run_procedure.non_removable_bean_map_attrs_list.append(bean_map[Root]['attrs'])
        return dry_run_procedure


