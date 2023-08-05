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
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, MSG_DELETE, AlteonConfigurator
from radware.alteon.beans.VacmAccessTable import *
from typing import Optional, ClassVar, Dict
from radware.alteon.exceptions import AlteonRequestError


class SNMPv3AcessParameters(RadwareParametersStruct):
    group_name: str
    context_prefix: str
    security_model: EnumSecurityModel
    security_level: EnumSecurityLevel
    match_type: Optional[EnumContextMatch]
    read_view_name: Optional[str]
    write_view_name: Optional[str]
    notify_view_name: Optional[str]

    def __init__(self, gname: str = None, prefix: str = None, secModel: int = None, secLvl: str = None):
        self.group_name = gname
        self.context_prefix = prefix
        self.security_model = secModel
        self.security_level = secLvl
        self.match_type = None
        self.read_view_name = None
        self.write_view_name = None
        self.notify_view_name = None

bean_map = {
    VacmAccessTable: dict(
        struct=SNMPv3AcessParameters,
        direct=True,
        attrs=dict(
            GroupName='group_name',
            ContextPrefix='context_prefix',
            SecurityModel='security_model',
            SecurityLevel='security_level',
            ContextMatch='match_type',
            ReadViewName='read_view_name',
            WriteViewName='write_view_name',
            NotifyViewName='notify_view_name'
        )
    )
}


class SNMPv3AcessConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[SNMPv3AcessParameters]

    def __init__(self, alteon_connection):
        super(SNMPv3AcessConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: SNMPv3AcessParameters) -> SNMPv3AcessParameters:
        if parameters.context_prefix == "":
            parameters.context_prefix = " "
        self._read_device_beans(parameters)
        if self._beans:
            return parameters

    def _update(self, parameters: SNMPv3AcessParameters, dry_run: bool) -> str:
        if parameters.context_prefix is None:
            parameters.context_prefix = " "
        self._write_device_beans(parameters, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE


    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(VacmAccessTable, parameters)


