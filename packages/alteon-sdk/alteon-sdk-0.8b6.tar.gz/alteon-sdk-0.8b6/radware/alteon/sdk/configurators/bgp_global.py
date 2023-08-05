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
from radware.alteon.sdk.alteon_managment import AlteonMngInfo
from radware.sdk.common import RadwareParametersStruct, RadwareParametersExtension
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, MSG_DELETE, AlteonConfigurator
from radware.sdk.exceptions import DeviceConfiguratorError
from radware.alteon.beans.Global import *
from typing import List, Optional, ClassVar
from radware.sdk.exceptions import DeviceConfiguratorError


class BgpGlobalParameters(RadwareParametersStruct):
    router_id: Optional[str]
    bgp_status: Optional[EnumBgpNewCfgState]
    local_preference: Optional[int]
    max_as_path_length: Optional[int]
    as_number: Optional[int]
    vip_advertisement: Optional[EnumBgpNewCfgStopVipAdv]
    floating_ip_advertisement: Optional[EnumBgpNewCfgAdvFip]
    bgp_mode: Optional[EnumBgpNewCfgMode]
    ecmp_mode: Optional[EnumBgpNewCfgEcmp]


    def __init__(self):
        self.router_id = None
        self.bgp_status = None
        self.local_preference = None
        self.max_as_path_length = None
        self.as_number = None
        self.vip_advertisement = None
        self.floating_ip_advertisement = None
        self.bgp_mode = None
        self.ecmp_mode = None


bean_map = {
    Root: dict(
        struct=BgpGlobalParameters,
        direct=True,
        attrs=dict(
            ipNewCfgRouterID='router_id',
            bgpNewCfgState='bgp_status',
            bgpNewCfgLocalPref='local_preference',
            bgpNewCfgMaxASPath='max_as_path_length',
            bgpNewCfgASNumber='as_number',
            bgpNewCfgStopVipAdv='vip_advertisement',
            bgpNewCfgAdvFip='floating_ip_advertisement',
            bgpNewCfgMode='bgp_mode',
            bgpNewCfgEcmp='ecmp_mode',
        )
    )
}


class BgpGlobalConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[BgpGlobalParameters]

    def __init__(self, alteon_connection):
        super(BgpGlobalConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: BgpGlobalParameters) -> BgpGlobalParameters:
        self._read_device_beans(parameters)
        if self._beans:
            return parameters

    def _update(self, parameters: BgpGlobalParameters, dry_run: bool) -> str:
        if parameters.max_as_path_length is not None:
            if parameters.max_as_path_length > 127:
                raise DeviceConfiguratorError(self.__class__, 'max AS path length must be between 1 and 127')
            if parameters.as_number > 4294967295:
                raise DeviceConfiguratorError(self.__class__, 'AS number must be between 0 and 4294967295')
            if parameters.local_preference > 4294967295:
                raise DeviceConfiguratorError(self.__class__, 'Local preference must be between 0 and 4294967295')
        self._write_device_beans(parameters, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(Root, parameters)

