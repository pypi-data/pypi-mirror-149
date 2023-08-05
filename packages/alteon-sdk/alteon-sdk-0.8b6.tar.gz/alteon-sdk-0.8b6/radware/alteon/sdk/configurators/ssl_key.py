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
from radware.alteon.beans.SlbNewSslCfgCertsTable import *
from radware.alteon.exceptions import AlteonRequestError
from typing import Optional, List, ClassVar


class SSLKeyParameters(RadwareParametersStruct):
    index: str
    description: Optional[str]
    passphrase: Optional[PasswordArgument]
    content: Optional[str]

    def __init__(self, index: str = None):
        self.index = index
        self.description = None
        self.passphrase = None
        self.content = None


class SSLKeyInfo(RadwareParametersStruct):
    def __init__(self):
        self.index = None
        self.description = None
        self.key_size = None


bean_map = {
    SlbNewSslCfgCertsTable: dict(
        struct=SSLKeyParameters,
        direct=True,
        attrs=dict(
            ID='index',
            Name='description',
        )
    )
}

key_info_map = dict(
    KeySizeCommon='key_size',
)
key_info_map.update(bean_map[SlbNewSslCfgCertsTable]['attrs'])


class SSLKeyConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[SSLKeyParameters]

    def __init__(self, alteon_connection):
        super(SSLKeyConfigurator, self).__init__(bean_map, alteon_connection)

    @staticmethod
    def _prepare_query(parameters):
        query = '?id=' + parameters.index + '&renew=1&src=txt&type=key'
        if parameters.passphrase is not None:
            query += '&passphrase=' + parameters.passphrase
        return query

    def _read(self, parameters: SSLKeyParameters) -> SSLKeyParameters:
        instance = self._entry_bean_instance(parameters)
        instance.Type = EnumSlbSslCertsType.key
        key = self._device_api.read(instance)
        ssl_params = SSLKeyParameters()
        if key:
            ssl_params.index = key.ID
            ssl_params.description = key.Name
            ssl_params.content = self._rest.read_data_object('getcert' + self._prepare_query(parameters))
            return ssl_params

    def _update(self, parameters: SSLKeyParameters, dry_run: bool) -> str:
        if parameters.content is not None:
            try:
                self._rest.update_data_object('sslcertimport' + self._prepare_query(parameters),
                                              parameters.content, dry_run=dry_run)
            except AlteonRequestError as err:
                err.response.url = err.response.url.replace('passphrase={0}'.format(parameters.passphrase),
                                                            'passphrase=*****')
        if parameters.description:
            instance = self._entry_bean_instance(parameters)
            instance.Type = EnumSlbSslCertsType.key
            instance.Name = parameters.description
            self._device_api.update(instance, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_UPDATE

    def delete(self, parameters: SSLKeyParameters, dry_run=False, **kw) -> str:
        log.debug(' {0}: {1}, server: {2}, params: {3}'.format(self.__class__.__name__, self.DELETE.upper(), self.id,
                                                               parameters))
        self_obj = self._entry_bean_instance(parameters)
        self_obj.Type = EnumSlbSslCertsType.key
        self._device_api.delete(self_obj, dry_run=dry_run)
        return self._get_object_id(parameters) + MSG_DELETE

    def read_all(self, parameters: SSLKeyParameters = None, **kw) -> List[RadwareParametersStruct]:
        log.debug(' {0}: {1}, server: {2}, params: {3}'.format(self.__class__.__name__, self.READ_ALL.upper(), self.id,
                                                               parameters))
        result = list()
        if parameters is None or parameters.passphrase is None:
            if 'passphrase' in kw:
                passphrase = kw.get('passphrase')
            else:
                return result
        else:
            passphrase = parameters.passphrase
        instance = self._entry_bean_instance(parameters)
        attrs = self._bean_map[SlbNewSslCfgCertsTable]['attrs']
        beans = self._device_api.read_all(instance)
        if beans:
            for bean in beans:
                if bean.Type == EnumSlbSslCertsType.key:
                    parameters = SSLKeyParameters()
                    parameters.passphrase = passphrase
                    self._update_param_struct_attrs_from_object(parameters, attrs, bean)
                    result.append(self.read(parameters))
        return result

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(SlbNewSslCfgCertsTable, parameters)

    def read_key_info(self, parameters: SSLKeyParameters):
        log.debug(' {0}: {1}, server: {2}, params: {3}'.format(self.__class__.__name__, 'read_key_info'.upper(), self.id,
                                                               parameters))
        instance = self._entry_bean_instance(parameters)
        instance.Type = EnumSlbSslCertsType.key
        key = self._device_api.read(instance)
        if key:
            ssl_key_info = SSLKeyInfo()
            self._update_param_struct_attrs_from_object(ssl_key_info, key_info_map, key)
            return ssl_key_info

    def read_all_key_info(self, parameters: SSLKeyParameters = None):
        log.debug(' {0}: {1}, server: {2}, params: {3}'.format(self.__class__.__name__,
                                                               'read_all_key_info'.upper(), self.id, parameters))

        result = list()
        attrs = self._bean_map[SlbNewSslCfgCertsTable]['attrs']
        instance = self._entry_bean_instance(parameters)
        beans = self._device_api.read_all(instance)
        if beans:
            for bean in beans:
                if bean.Type == EnumSlbSslCertsType.key:
                    parameters = SSLKeyParameters()
                    self._update_param_struct_attrs_from_object(parameters, attrs, bean)
                    result.append(self.read_key_info(parameters))
        return result
