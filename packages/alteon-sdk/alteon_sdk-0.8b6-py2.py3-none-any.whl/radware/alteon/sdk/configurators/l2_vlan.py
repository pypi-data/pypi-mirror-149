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
from radware.alteon.sdk.alteon_managment import AlteonMngInfo
from radware.alteon.beans.VlanNewCfgTable import *
from typing import List, Optional, ClassVar


class VLANParameters(RadwareParametersStruct):
    index: int
    name: Optional[str]
    state: Optional[EnumVlanState]
    shared: Optional[EnumVlanShared]
    source_mac_learning: Optional[EnumVlanLearn]
    jumbo_frame: Optional[EnumVlanJumbo]
    traffic_contract: Optional[int]
    ports: Optional[List[int]]

    def __init__(self, index: int = None):
        self.index = index
        self.name = None
        self.state = None
        self.shared = None
        self.source_mac_learning = None
        self.jumbo_frame = None
        self.traffic_contract = None
        self.ports = list()


bean_map = {
    VlanNewCfgTable: dict(
        struct=VLANParameters,
        direct=True,
        attrs=dict(
            VlanId='index',
            VlanName='name',
            State='state',
            Learn='source_mac_learning',
            Jumbo='jumbo_frame',
            BwmContract='traffic_contract',
        )
    )
}


class VLANConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[VLANParameters]

    def __init__(self, alteon_connection):
        super(VLANConfigurator, self).__init__(bean_map, alteon_connection)
        self._mng_info = AlteonMngInfo(alteon_connection)

    def _read(self, parameters: VLANParameters) -> VLANParameters:
        self._read_device_beans(parameters)
        if self._beans:
            parameters.ports = BeanUtils.decode_bmp_sub_one(self._beans[VlanNewCfgTable].Ports)
            if self._mng_info.is_vx:
                parameters.shared = self._beans[VlanNewCfgTable].Shared

            return parameters

    def _update(self, parameters: VLANParameters, dry_run: bool) -> str:
        self._write_device_beans(parameters, dry_run=dry_run)
        if parameters.ports:
            for port in parameters.ports:
                if port!=0:
                    instance = self._get_bean_instance(VlanNewCfgTable, parameters)
                    instance.AddPort = port
                    self._device_api.update(instance, dry_run=dry_run)

            if self._mng_info.is_vx:
                if parameters.shared:
                    instance = self._get_bean_instance(VlanNewCfgTable, parameters)
                    instance.Shared = parameters.shared
                    self._device_api.update(instance, dry_run=dry_run)

        return self._get_object_id(parameters) + MSG_UPDATE

    def _update_remove(self, parameters: VLANParameters, dry_run: bool) -> str:
        if parameters.ports:
            instance = self._get_bean_instance(VlanNewCfgTable, parameters)
            for port in parameters.ports:
                instance.RemovePort = port
                self._device_api.update(instance, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(VlanNewCfgTable, parameters)


