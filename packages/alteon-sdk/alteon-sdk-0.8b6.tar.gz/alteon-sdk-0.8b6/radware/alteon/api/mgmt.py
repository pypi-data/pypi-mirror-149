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


import logging
from radware.sdk.management import DeviceManagement
from radware.alteon.sdk.alteon_managment import AlteonMngOper, AlteonMngConfig, AlteonMngInfo

log = logging.getLogger(__name__)


class AlteonManagement(DeviceManagement):
    # link to device management classes

    def __init__(self, alteon_connection):
        self.config = AlteonMngConfig(alteon_connection)
        self.oper = AlteonMngOper(alteon_connection)
        self.info = AlteonMngInfo(alteon_connection)
        log.info(' Alteon Management Module initialized, server: {0}'.format(alteon_connection.id))

    @property
    def _device_mng_info(self):
        return self.info

    @property
    def _device_mng_oper(self):
        return self.oper

    @property
    def _device_mng_config(self):
        return self.config
