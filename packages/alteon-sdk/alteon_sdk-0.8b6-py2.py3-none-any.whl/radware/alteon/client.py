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
from radware.sdk.api import BaseAPI
from radware.alteon.api.config import AlteonConfiguration
from radware.alteon.api.mgmt import AlteonManagement
from radware.alteon.api import AlteonDeviceConnection

log = logging.getLogger(__name__)


class AlteonAPI(object):
    def __init__(self, connection: AlteonDeviceConnection):
        self._device = connection
        self._mng = AlteonManagement(connection)
        self._conf = AlteonConfiguration(connection)

    @property
    def device(self):
        return self._device.rest

    @property
    def mgmt(self):
        return self._mng

    @property
    def conf(self):
        return self._conf


class AlteonClient(BaseAPI):
    def __init__(self, **kwargs):
        self._connection = AlteonDeviceConnection(**kwargs)
        self._api = AlteonAPI(self._connection)

    @property
    def api(self):
        return self._api

    def update_connection(self, **params):
        self._connection.connection_details_update(**params)

