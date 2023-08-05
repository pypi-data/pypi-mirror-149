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

from radware.sdk.api import BaseDeviceConnection
from radware.alteon.sdk.impl import AlteonRest
import logging
import copy

log = logging.getLogger(__name__)


class AlteonDeviceConnection(BaseDeviceConnection):
    """
    Alteon device connection is object which aggregate all device connectors.
    this class contain device `connection_details` that is required by connectors.
    each instance is associated to single device by hostname and can be used by multiple software components

    """
    def __init__(self, **kwargs):
        super(AlteonDeviceConnection, self).__init__()
        self.id = kwargs.get('server', None)
        self._alteon_rest = AlteonRest(**kwargs)
        self._connection_details = kwargs
        log.info(' Alteon Device Connection initialized, server: {0}'.format(self.id))

    def connection_details_update(self, **kwargs):
        log.info(' Updating Alteon Connection details, server: {0}'.format(self.id))
        if 'server' in kwargs:
            self.id = kwargs.get('server')
        self._alteon_rest = AlteonRest(**kwargs)
        self._connection_details = kwargs

    def get_connection_details(self):
        return copy.deepcopy(self._connection_details)

    @property
    def rest(self):
        return self._alteon_rest

