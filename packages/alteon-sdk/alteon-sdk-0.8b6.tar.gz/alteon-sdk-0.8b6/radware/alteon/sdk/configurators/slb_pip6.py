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
# @author: Nofar Livkind, Radware


from radware.sdk.common import RadwareParametersStruct
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, AlteonConfigurator
from radware.alteon.beans.Pip6NewCfgTable import *
from radware.alteon.beans.Global import *
from radware.sdk.exceptions import DeviceConfiguratorError
from typing import List, Optional, ClassVar


class SlbPip6Parameters(RadwareParametersStruct):
    pip6_addr: str
    base_type: EnumPipNewCfgBaseType
    ports: Optional[List[int]]
    vlans: Optional[List[int]]

    def __init__(self, addr: str = None):
        self.pip6_addr = addr
        self.base_type = EnumPipNewCfgBaseType.port
        self.ports = list()
        self.vlans = list()


bean_map = {
    Pip6NewCfgTable: dict(
        struct=SlbPip6Parameters,
        direct=True,
        attrs=dict(
            Pip='pip6_addr'
        )
    ),
    Root: dict(
        struct=SlbPip6Parameters,
        direct=True,
        attrs=dict(
            pipNewCfgBaseType='base_type'
        )
    )
}


class SlbPip6Configurator(AlteonConfigurator):
    parameters_class: ClassVar[SlbPip6Parameters]

    def __init__(self, alteon_connection):
        super(SlbPip6Configurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: SlbPip6Parameters) -> SlbPip6Parameters:
        self._read_device_beans(parameters)
        if self._beans:
            if self._beans[Pip6NewCfgTable] is None:
                return None

            parameters.ports = BeanUtils.decode_bmp_sub_one(self._beans[Pip6NewCfgTable].PortMap)
            parameters.vlans = BeanUtils.decode_bmp_sub_one(self._beans[Pip6NewCfgTable].VlanMap)
            parameters.base_type = EnumPipNewCfgBaseType.port
            if not parameters.ports:
                parameters.base_type = EnumPipNewCfgBaseType.vlan

            return parameters

    def _update(self, parameters: SlbPip6Parameters, dry_run: bool) -> str:

        self._write_device_beans(parameters, dry_run=dry_run)
        instance = self._get_bean_instance(Pip6NewCfgTable, parameters)
        instance_btype = self._get_bean_instance(Root, parameters.base_type)

        if parameters.base_type == EnumPipNewCfgBaseType.port:
            instance_btype.pipNewCfgBaseType = EnumPipNewCfgBaseType.port
            self._device_api.update(instance_btype, dry_run=dry_run)
            if parameters.ports:
                for port in parameters.ports:
                    instance.AddPort = port
                    self._device_api.update(instance, dry_run=dry_run)
        elif parameters.base_type == EnumPipNewCfgBaseType.vlan:
            instance_btype.pipNewCfgBaseType = EnumPipNewCfgBaseType.vlan
            self._device_api.update(instance_btype, dry_run=dry_run)
            if parameters.vlans:
                for vlan in parameters.vlans:
                    instance.AddVlan = vlan
                    self._device_api.update(instance, dry_run=dry_run)
        else:
            raise DeviceConfiguratorError(self.__class__, 'base type parse error - unexpected string {0}'
                                          .format(parameters.base_type))

        return self._get_object_id(parameters) + MSG_UPDATE

    def _update_remove(self, parameters: SlbPip6Parameters, dry_run: bool) -> str:

        instance = self._get_bean_instance(Pip6NewCfgTable, parameters)
        if parameters.base_type == EnumPipNewCfgBaseType.port:
            for port in parameters.ports:
                instance.RemovePort = port
                self._device_api.update(instance, dry_run=dry_run)
        elif parameters.base_type == EnumPipNewCfgBaseType.vlan:
            for vlan in parameters.vlans:
                instance.RemoveVlan = vlan
                self._device_api.update(instance, dry_run=dry_run)
        else:
            raise DeviceConfiguratorError(self.__class__, 'base type parse error - unexpected string {0}'
                                          .format(parameters.base_type))

        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(Pip6NewCfgTable, parameters)