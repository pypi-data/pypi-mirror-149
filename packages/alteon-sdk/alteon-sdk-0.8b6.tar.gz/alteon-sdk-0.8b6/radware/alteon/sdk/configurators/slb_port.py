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
# @author: Ofer Epstein, Radware


from radware.sdk.common import RadwareParametersStruct, PasswordArgument
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, AlteonConfigurator
from radware.alteon.beans.SlbNewCfgPortTable import *
from typing import Optional, ClassVar, Dict
from radware.alteon.exceptions import AlteonRequestError


class SlbPortParameters(RadwareParametersStruct):
    index: int
    state: Optional[str]
    hot_standby: Optional[str]
    inter_switch: Optional[str]
    pip_state: Optional[str]
    rts_state: Optional[str]
    delete: Optional[str]
    idslb_state: Optional[str]    
    filter: Optional[str]
    add_filter: Optional[int]
    rem_filter: Optional[int]
    server_state: Optional[str]
    client_state: Optional[str]
    l3_filter: Optional[str]
    filter_bmap: Optional[str]
    inter_switch_vlan: Optional[int]
    vlan_bmap: Optional[str]

    def __init__(self, index: int = None):
        self.index = index
        self.state = None
        self.hot_standby = None
        self.inter_switch = None
        self.pip_state = None
        self.rts_state = None
        self.delete = None
        self.idslb_state = None
        self.filter = None
        self.add_filter = None
        self.rem_filter = None
        self.server_state = None
        self.client_state = None
        self.l3_filter = None
        self.filter_bmap = None
        self.inter_switch_vlan = None
        self.vlan_bmap = None


bean_map = {
    SlbNewCfgPortTable: dict(
        struct=SlbPortParameters,
        direct=True,
        attrs=dict(
            Index='index',
            SlbState='state',
            SlbHotStandby='hot_standby',
            SlbInterSwitch='inter_switch',
            SlbPipState='pip_state',
            SlbRtsState='rts_state',
            Delete='delete',
            SlbIdslbState='idslb_state',
            SlbFilter='filter',
            SlbAddFilter='add_filter',
            SlbRemFilter='rem_filter',
            SlbServState='server_state',
            SlbClntState='client_state',
            SlbL3Filter='l3_filter',
            SlbFilterBmap='filter_bmap',
            InterSwitchVlan='inter_switch_vlan',
            VlanBmap='vlan_bmap'
        )
    )
}


class SlbPortConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[SlbPortParameters]

    def __init__(self, alteon_connection):
        super(SlbPortConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: SlbPortParameters) -> SlbPortParameters:
        self._read_device_beans(parameters)
        if self._beans:
            parameters.filter_bmap = BeanUtils.decode_bmp(parameters.filter_bmap)
            filter_list = list()
            for v in parameters.filter_bmap:
                filter_list.append(v)
            parameters.filter_bmap = str(filter_list).strip('[]')
            parameters.vlan_bmap = BeanUtils.decode_bmp(parameters.vlan_bmap)
            vlan_list = list()
            for v in parameters.vlan_bmap:
                vlan_list.append(v)
            parameters.vlan_bmap = str(vlan_list).strip('[]')
            return parameters

    def _update(self, parameters: SlbPortParameters, dry_run: bool) -> str:
        if parameters.filter_bmap is not None:
                raise DeviceConfiguratorError(self.__class__, 'filter_bmap is read only')
        if parameters.vlan_bmap is not None:
                raise DeviceConfiguratorError(self.__class__, 'vlan_bmap is read only')
        if parameters.add_filter is not None:
            if parameters.add_filter > 2048:
                raise DeviceConfiguratorError(self.__class__, 'Filter index must be between 1 and 2048')
        if parameters.rem_filter is not None:
            if parameters.rem_filter > 2048:
                raise DeviceConfiguratorError(self.__class__, 'Filter index must be between 1 and 2048')
        if parameters.inter_switch_vlan is not None:
            if parameters.inter_switch_vlan > 4090:
                raise DeviceConfiguratorError(self.__class__, 'VLAN index must be between 1 and 4090')
        self._write_device_beans(parameters, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE


    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(SlbNewCfgPortTable, parameters)

