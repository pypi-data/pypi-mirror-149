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
from radware.alteon.beans.SlbNewSslCfgGroupsTable import *
from radware.alteon.beans.SlbNewSslCfgCertsTable import *
from typing import List, Optional, ClassVar


class SSLCertGroupParameters(RadwareParametersStruct):
    index: str
    certificate_type: Optional[EnumSlbSslGroupsType]
    description: Optional[str]
    default_server_certificate: Optional[str]
    certificate_chaining_mode: Optional[EnumSlbSslGroupsChainingMode]
    certificate_names: Optional[List[str]]

    def __init__(self, index: str = None):
        self.index = index
        self.certificate_type = None
        self.description = None
        self.default_server_certificate = None
        self.certificate_chaining_mode = None
        self.certificate_names = list()


bean_map = {
    SlbNewSslCfgGroupsTable: dict(
        struct=SSLCertGroupParameters,
        direct=True,
        attrs=dict(
            ID='index',
            Name='description',
            Type='certificate_type',
            DefaultCert='default_server_certificate',
            ChainingMode='certificate_chaining_mode',
        )
    )
}


class SSLCertGroupConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[SSLCertGroupParameters]

    def __init__(self, alteon_connection):
        super(SSLCertGroupConfigurator, self).__init__(bean_map, alteon_connection)
        self._mng_info = AlteonMngInfo(alteon_connection)

    def _read(self, parameters: SSLCertGroupParameters) -> SSLCertGroupParameters:
        self._read_device_beans(parameters)
        if self._beans:
            cert_numeric_indexes = BeanUtils.decode_bmp(self._beans[SlbNewSslCfgGroupsTable].CertBmap)
            cert_type_lookup = EnumSlbSslCertsType.enum(parameters.certificate_type.value)

            cert_names = sorted([entry.ID for entry in self._device_api.read_all(SlbNewSslCfgCertsTable())
                                 if entry.Type == cert_type_lookup])
            parameters.certificate_names = [cert_names[idx - 2] for idx in cert_numeric_indexes]
            return parameters

    def _update(self, parameters: SSLCertGroupParameters, dry_run: bool) -> str:
        self._write_device_beans(parameters, dry_run=dry_run)

        if parameters.certificate_names:
            for cert in parameters.certificate_names:
                instance = self._get_bean_instance(SlbNewSslCfgGroupsTable, parameters)
                instance.AddCert = cert
                self._device_api.update(instance, dry_run=dry_run)

        return self._get_object_id(parameters) + MSG_UPDATE

    def _update_remove(self, parameters: SSLCertGroupParameters, dry_run: bool) -> str:
        if parameters.certificate_names:
            instance = self._get_bean_instance(SlbNewSslCfgGroupsTable, parameters)
            for cert in parameters.certificate_names:
                instance.RemCert = cert
                self._device_api.update(instance, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(SlbNewSslCfgGroupsTable, parameters)


