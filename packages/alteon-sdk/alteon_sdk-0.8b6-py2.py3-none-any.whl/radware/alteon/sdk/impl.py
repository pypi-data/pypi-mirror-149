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

"""

Implementation of device communication.
this module provide communication services through various protocol.
currently only REST is implemented which is the preferred communication method.
the device-specific implementation should use communication drivers from common SDK package.

all communication to device must go thought this module.
the module provide functions as -> read, update, delete, file download/upload, response processing ,
request preparation and request-to-object translating and vice-versa.

all device-specific general communication should be implemented here. e.g - ordered json, device error
return, binary json.

"""


from radware.sdk.api import DeviceAPI
from radware.sdk.rest_driver import RestSession
from radware.alteon.beans.Global import Root
from radware.alteon.beans.AgAccessUserNewCfgTable import AgAccessUserNewCfgTable
from radware.alteon.beans.VADCUsersPswdTable import VADCUsersPswdTable
from radware.alteon.beans.SlbNewNwclssCfgNetworkElementsTable import SlbNewNwclssCfgNetworkElementsTable
from radware.alteon.beans.SlbNewSslCfgSSLPolTable import SlbNewSslCfgSSLPolTable
from radware.sdk.beans_common import *
from collections import OrderedDict
from radware.alteon.exceptions import AlteonRequestError
import logging
from typing import IO


log = logging.getLogger(__name__)

# priority map define field precedence per endpoint when necessary
priority_bean_attrs = {
    Root: ['agAccessAdminPasswd', 'agAccessAdminNewPasswd', 'agAccessAdminConfNewPasswd'],
    AgAccessUserNewCfgTable: ['AdminPswd', 'Pswd'],
    VADCUsersPswdTable: ['vADCAccessAdminPasswd', 'vADCAccessAdminNewPasswd'],
    SlbNewNwclssCfgNetworkElementsTable: ['RegCont', 'RegCountry', 'RegState'],
    SlbNewSslCfgSSLPolTable: ['Bessl', 'Becipher']
}


class AlteonRest(DeviceAPI):
    def __init__(self, server=None, user=None, password=None, https_port=443, timeout=10,
                 validate_certs=True, **params):
        self._server = server
        self._user = user
        self._password = password
        self._https_port = https_port
        self._timeout = timeout
        self._validate_certs = validate_certs
        self._load_params(**params)
        self._rest_client = RestSession(self._validate_certs, max_connection=10)
        log.info(' Alteon REST initialized {0}:{1}, user: {2} '.format(self._server, self._https_port, self._user))

    def _load_params(self, **params):
        for k, v in params.items():
            if hasattr(self, k):
                setattr(self, k, v)

    @property
    def timeout(self):
        return self._timeout

    @property
    def user(self):
        return self._user

    @property
    def server(self):
        return self._server

    @property
    def https_port(self):
        return self._https_port

    def set_password(self, password):
        log.info('Alteon REST user: {0} password changed '.format(self._user))
        self._password = password

    def read_no_translation(self, bean, retries=3):
        all_result = self.read_all_no_translation(bean, retries)
        return self._return_read(bean, all_result)

    def read_all_no_translation(self, bean, retries=3):
        response_data = self._read_all(bean, retries)
        if bean.__class__ != Root and response_data:
            return response_data[bean.__class__.__name__]
        else:
            return response_data

    def read(self, bean, retries=3, timeout=None):
        all_result = self.read_all(bean, retries, timeout)
        return self._return_read(bean, all_result)

    def read_all(self, bean, retries=3, timeout=None):

        def _translate_bean_all(res):
            translated = list()
            if res:
                for item in res:
                    if item:
                        translated.append(bean.translate_json(**item))
            return translated

        response_data = self._read_all(bean, retries, timeout)
        if bean.__class__ != Root and response_data:
            return _translate_bean_all(response_data[bean.__class__.__name__])
        else:
            if response_data:
                return bean.translate_json(**response_data)

    # def update(self, bean, retries=3):
    #     result = None
    #
    #     for x in range(0, retries):
    #         result = self._rest_client.put(self._rest_url(bean, update=True), json=bean.to_json_int(), **self._rest_params)
    #         if result.ok:
    #             break
    #     self._alteon_response_processor(result, bean)
    #     return True

    def update(self, bean, retries=3, dry_run=False, timeout=None):
        if not dry_run:
            log.debug('update bean on {0}, {1}'.format(self.server, bean))
        result = None
        if bean.__class__ in priority_bean_attrs:
            bean_json = self._reorder_json(bean)
        else:
            bean_json = bean.to_json_int()

        data = '{\n'
        for k, v in bean_json.items():
            if v is not None:
                data += '"' + str(k) + '":"' + str(v) + '",\n'
        data += '}'

        url = self._rest_url(bean, update=True)
        if not dry_run:
            rest_params = self._rest_params
            if timeout:
                rest_params['timeout'] = timeout
            for x in range(0, retries):
                result = self._rest_client.put(url, data=data, **rest_params)
                if result.ok:
                    break
            self._alteon_response_processor(result, bean)
        return True

    def delete(self, bean, retries=3, dry_run=False):
        log.debug('delete bean from {0}, {1}'.format(self.server, bean))
        result = None
        url = self._rest_url(bean)
        if not dry_run:
            for x in range(0, retries):
                result = self._rest_client.delete(url, **self._rest_params)
                if result.ok:
                    break
            self._alteon_response_processor(result, bean)
        return True

    def read_data_object(self, object_path):
        log.debug('read data from {0}, {1}'.format(self.server, object_path))
        url = self._rest_base_url + object_path
        response_data = self._rest_client.get(url, **self._rest_params)
        if not response_data.ok:
            raise AlteonRequestError(response_data)

        return response_data.content

    def download_file_object(self, object_path):
        log.debug('read data from {0}, {1}'.format(self.server, object_path))
        url = self._rest_base_url + object_path
        rest_params = self._rest_params
        rest_params.update(preload_content=False)
        response_data = self._rest_client.get(url, **rest_params)
        if not response_data.ok:
            raise AlteonRequestError(response_data)
        return response_data

    def update_data_object(self, object_path, data, dry_run=False):
        if not dry_run:
            log.debug('update data on {0}, path: {1}, data: {2}'.format(self.server, object_path, data))
        url = self._rest_base_url + object_path
        if not dry_run:
            response_data = self._rest_client.put(url, data=data, **self._rest_params)
            if not response_data.ok:
                raise AlteonRequestError(response_data)

            return response_data.content
        return True

    def upload_file_object(self, object_path, stream: IO = None, dry_run=False, **kw):
        if not dry_run:
            log.debug('upload data on {0}, path: {1}, file_name: {2}'.format(self.server, object_path, stream.name))
        url = self._rest_base_url + object_path

        if not dry_run:
            rest_params = self._rest_params
            rest_params.update(kw)
            response_data = RestSession(self._validate_certs).post(url,
                                                                   fields={'filefield': (stream.name, stream.read())},
                                                                   **rest_params)
            if not response_data.ok:
                raise AlteonRequestError(response_data)
            return response_data.content
        return True

    @staticmethod
    def _return_read(bean, all_result):
        if bean.__class__ != Root:
            if all_result:
                return all_result[0]
            else:
                return None
        else:
            return all_result

    def _read_all(self, bean, retries=3, timeout=None):
        log.debug('read bean from {0}, {1}'.format(self.server, bean))
        result = None
        rest_call_params = self._rest_params
        if timeout is not None:
            rest_call_params['timeout'] = timeout
        for x in range(0, retries):
            result = self._rest_client.get(self._rest_url(bean), **rest_call_params)
            if result.ok:
                break
        return self._alteon_response_processor(result, bean)

    @staticmethod
    def _alteon_response_processor(rest_result, bean):
        if not rest_result.ok:
            if rest_result.request.method == 'DELETE':
                try:
                    json_out = rest_result.json()
                    if 'testErr' in json_out and 'not exist' in json_out['testErr']:
                        return json_out
                except ValueError:
                    pass
            raise AlteonRequestError(rest_result)
        json_out = rest_result.json()
        
        # alteon sometimes return 200OK but with status err. 
        # like we have in case of errors in snmpv3 usm user table.
        # in such cases we always want to rais error and not just in root.
        # Root: <class 'radware.alteon.beans.Global.Root'>
        # bean.__class__: <class 'radware.alteon.beans.UsmUserTable.UsmUserTable'>

        # MP return status error upon GET request for single row scenario when object not found.
        # This is a bug in MP that will be fixed in next release.
        # It happens in webApi.c at function processBBIRequest that calls processGetRestCmdElm
        # for single row scenario.
        # When ansible receives status error it aborts the script on failure.
        # As a HACK to temporarily fix it w/o an MP fix Ansible exclude following tables from error condition. 
        if 'status' in json_out and json_out['status'].startswith('err'):
            if (
                bean.__class__.__name__ == 'SlbNewSslCfgCertsTable' or 
                bean.__class__.__name__ == 'SlbNewCfgEnhVirtServerTable' or 
                bean.__class__.__name__ == 'SlbNewCfgEnhVirtServicesTable' or 
                bean.__class__.__name__ == 'SlbNewCfgEnhVirtServicesSecondPartTable' or 
                bean.__class__.__name__ == 'SlbNewCfgEnhVirtServicesFifthPartTable' or 
                bean.__class__.__name__ == 'SlbNewCfgEnhVirtServicesSixthPartTable' or 
                bean.__class__.__name__ == 'SlbNewCfgEnhVirtServicesSeventhPartTable' 
            ):
                return None
            raise AlteonRequestError(rest_result)
        return json_out

    @property
    def _rest_params(self):
        return dict(
            timeout=self._timeout,
            verify=self._validate_certs,
            user=self._user,
            password=self._password
        )

    @property
    def _rest_base_url(self):
        return 'https://{0}:{1}/config/'.format(self._server, self._https_port)

    def _rest_url(self, bean, update=None):
        if bean.__class__ != Root:
            base = self._rest_base_url + bean.__class__.__name__
            bean_indexes = bean.translate_self().get_indexes()
            if bean_indexes:
                for idx in bean_indexes:
                    if idx:
                        if not isinstance(idx, BaseBeanEnum):
                            base += '/' + str(idx)
                        else:
                            base += '/' + str(idx.value)
        else:
            if update:
                return self._rest_base_url
            base = self._rest_base_url + '?prop='
            for k, v in bean.__dict__.items():
                if v is not None:
                    base += k + ','
            base = base[:len(base)-1]
        return base

    @staticmethod
    def _reorder_json(bean):
        bean_json = bean.to_json_int()
        new_json = OrderedDict()
        for key in priority_bean_attrs[bean.__class__]:
            if key in bean_json and bean_json[key] is not None:
                new_json.update({key: bean_json.pop(key)})
        if new_json:
            new_json.update(bean_json)
            bean_json = new_json
        return bean_json

