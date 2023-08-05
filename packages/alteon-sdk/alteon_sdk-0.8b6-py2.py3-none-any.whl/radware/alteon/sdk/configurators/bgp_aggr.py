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


from radware.sdk.common import RadwareParametersStruct, PasswordArgument
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, AlteonConfigurator
from radware.alteon.beans.BgpNewCfgAggrTable import *
from typing import List, Optional, ClassVar, Dict
from radware.alteon.exceptions import AlteonRequestError
from radware.alteon.sdk.alteon_managment import AlteonMngInfo
from radware.sdk.exceptions import DeviceConfiguratorError


class BgpAggrParameters(RadwareParametersStruct):
    index: int
    aggr_addr: Optional[str]
    mask: Optional[str]
    status: Optional[EnumBgpAggrState]


    def __init__(self, index: int = None):
        self.index = index
        self.aggr_addr = None
        self.mask = None
        self.status = None

bean_map = {
    BgpNewCfgAggrTable: dict(
        struct=BgpAggrParameters,
        direct=True,
        attrs=dict(
            Index='index',
            Addr='aggr_addr',
            Mask='mask',
            State='status',
        )
    )
}


class BgpAggrConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[BgpAggrParameters]

    def __init__(self, alteon_connection):
        super(BgpAggrConfigurator, self).__init__(bean_map, alteon_connection)        
        self._mng_info = AlteonMngInfo(alteon_connection)

    def _read(self, parameters: BgpAggrParameters) -> BgpAggrParameters:
        self._read_device_beans(parameters)
        if self._beans:
            return parameters

    def _update(self, parameters: BgpAggrParameters, dry_run: bool) -> str:
        self._write_device_beans(parameters, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(BgpNewCfgAggrTable, parameters)


