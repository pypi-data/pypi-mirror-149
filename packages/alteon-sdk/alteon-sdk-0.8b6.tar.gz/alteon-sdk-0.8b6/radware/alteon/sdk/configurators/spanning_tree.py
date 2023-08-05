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
from radware.sdk.exceptions import DeviceConfiguratorError
from radware.alteon.sdk.alteon_managment import AlteonMngInfo
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, MSG_DELETE, AlteonConfigurator
from radware.alteon.beans.Global import *
from radware.alteon.beans.StgNewCfgTable import *
from typing import List, Optional, ClassVar


class STPGroupParameters(RadwareParametersStruct):
    id: int
    state: Optional[EnumStgState]
    bridge_priority: Optional[int]
    bridge_hello_time_second: Optional[int]
    bridge_max_age_second: Optional[int]
    bridge_forward_delay_second: Optional[int]
    bridge_aging_time_second: Optional[int]
    pvst_frames_on_untagged_ports: Optional[EnumStgUntagPvst]
    vlans: Optional[List[int]]

    def __init__(self, group_id: int = None):
        self.id = group_id
        self.state = None
        self.bridge_priority = None
        self.bridge_hello_time_second = None
        self.bridge_max_age_second = None
        self.bridge_forward_delay_second = None
        self.bridge_aging_time_second = None
        self.pvst_frames_on_untagged_ports = None
        self.vlans = list()


class SpanningTreeParameters(RadwareParametersStruct):
    state: EnumStgState
    mstp: Optional[EnumMstNewCfgState]
    mstp_mode: Optional[EnumMstNewCfgStpMode]
    mstp_region_name: Optional[str]
    mstp_region_version: Optional[int]
    mstp_maximum_hops: Optional[int]
    mstp_bridge_priority: Optional[int]
    mstp_bridge_max_age_second: Optional[int]
    mstp_bridge_forward_delay_second: Optional[int]
    stp_groups: Optional[List[STPGroupParameters]]

    def __init__(self, state: EnumStgState = None):
        self.state = state
        self.mstp = None
        self.mstp_mode = None
        self.mstp_region_name = None
        self.mstp_region_version = None
        self.mstp_maximum_hops = None
        self.mstp_bridge_priority = None
        self.mstp_bridge_max_age_second = None
        self.mstp_bridge_forward_delay_second = None
        self.stp_groups = list()


bean_map = {
    Root: dict(
        struct=SpanningTreeParameters,
        direct=True,
        attrs=dict(
            mstNewCfgState='mstp',
            mstNewCfgStpMode='mstp_mode',
            mstNewCfgRegionName='mstp_region_name',
            mstNewCfgRegionVersion='mstp_region_version',
            mstNewCfgMaxHopCount='mstp_maximum_hops',
            mstCistNewCfgBridgePriority='mstp_bridge_priority',
            mstCistNewCfgBridgeMaxAge='mstp_bridge_max_age_second',
            mstCistNewCfgBridgeForwardDelay='mstp_bridge_forward_delay_second',
        )
    ),
    StgNewCfgTable: dict(
        struct=List[STPGroupParameters],
        direct=True,
        attrs=dict(
            Index='id',
            State='state',
            Priority='bridge_priority',
            BrgHelloTime='bridge_hello_time_second',
            BrgMaxAge='bridge_max_age_second',
            BrgForwardDelay='bridge_forward_delay_second',
            AgingTime='bridge_aging_time_second',
            UntagPvst='pvst_frames_on_untagged_ports',
            VlanBmap='vlans'
        )
    )
}


class SpanningTreeConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[SpanningTreeParameters]

    def __init__(self, alteon_connection):
        super(SpanningTreeConfigurator, self).__init__(bean_map, alteon_connection)
        self._mng_info = AlteonMngInfo(alteon_connection)

    def _read(self, parameters: SpanningTreeParameters) -> SpanningTreeParameters:
        if not self._mng_info.is_container:
            raise DeviceConfiguratorError(self.__class__, 'not a container')
        self._read_device_beans(parameters)
        if self._beans:
            parameters.state = EnumStgState.off
            for stp_group in parameters.stp_groups:
                if stp_group.state == EnumStgState.on:
                    parameters.state = EnumStgState.on
                stp_group.vlans = BeanUtils.decode_bmp(stp_group.vlans)
            return parameters

    def _update(self, parameters: SpanningTreeParameters, dry_run: bool) -> str:
        if not self._mng_info.is_container:
            raise DeviceConfiguratorError(self.__class__, 'not a container')

        def _update_stg_global_state(state):
            for stg in self._device_api.read_all(StgNewCfgTable()):
                if state != stg.State:
                    instance = self._get_bean_instance(StgNewCfgTable, None)
                    instance.Index = stg.Index
                    instance.State = state
                    self._device_api.update(instance, dry_run=dry_run)

        parameters.state = EnumStgState.enum(parameters.state)

        for stp_group in parameters.stp_groups:
            if stp_group.vlans is not None:
                for vlan in stp_group.vlans:
                    stg_entry = self._get_bean_instance(StgNewCfgTable, stp_group)
                    stg_entry.AddVlan = vlan
                    self._device_api.update(stg_entry, dry_run=dry_run)
            stp_group.vlans = None

        if parameters.state == EnumStgState.on:
            _update_stg_global_state(EnumStgState.on)

        self._write_device_beans(parameters, dry_run=dry_run)

        if parameters.state == EnumStgState.off:
            _update_stg_global_state(EnumStgState.off)

        return self._get_object_id(parameters) + MSG_UPDATE

    def delete(self, parameters: SpanningTreeParameters, dry_run=False, **kw) -> str:
        if not self._mng_info.is_container:
            raise DeviceConfiguratorError(self.__class__, 'not a container')
        log.debug(' {0}: {1}, server: {2}, params: {3}'.format(self.__class__.__name__, self.DELETE.upper(), self.id,
                                                               parameters))
        for stg in self._device_api.read_all(StgNewCfgTable()):
            for vlan in BeanUtils.decode_bmp(stg.VlanBmap):
                instance = self._get_bean_instance(StgNewCfgTable, None)
                instance.Index = stg.Index
                instance.RemoveVlan = vlan
                self._device_api.update(instance, dry_run=dry_run)

        return 'Vlans association to STG' + MSG_DELETE

    def _update_remove(self, parameters: SpanningTreeParameters, dry_run: bool) -> str:
        if parameters.stp_groups:
            for group in parameters.stp_groups:
                instance = StgNewCfgTable()
                instance.Index = group.id
                cfg_group = self._device_api.read(instance)
                for vlan in BeanUtils.decode_bmp(cfg_group.VlanBmap):
                    instance = self._get_bean_instance(StgNewCfgTable, None)
                    instance.Index = group.id
                    instance.RemoveVlan = vlan
                    self._device_api.update(instance, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(Root, parameters)

    def dry_run_delete_procedure(self, diff):
        dry_run_procedure = DryRunDeleteProcedure()
        dry_run_procedure.non_removable_bean_map_attrs_list.append(bean_map[Root]['attrs'])
        dry_run_procedure.ignore_prop_names.append('state')
        if 'stp_groups' in diff:
            groups = list()
            for item in diff['stp_groups']:
                if item['vlans']:
                    groups.append(item)
            if groups:
                diff['stp_groups'] = groups
            else:
                diff.pop('stp_groups')
        return dry_run_procedure
