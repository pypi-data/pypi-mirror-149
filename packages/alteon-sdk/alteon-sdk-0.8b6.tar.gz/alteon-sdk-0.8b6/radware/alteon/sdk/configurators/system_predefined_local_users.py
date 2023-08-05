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
from radware.sdk.common import RadwareParametersStruct, PasswordArgument
from radware.alteon.sdk.alteon_configurator import MSG_UPDATE, MSG_NO_DELETE,  AlteonConfigurator
from radware.alteon.beans.Global import *
from typing import Optional, ClassVar


class PredefinedLocalUsersParameters(RadwareParametersStruct):
    current_admin_password: Optional[PasswordArgument]
    new_admin_password: Optional[PasswordArgument]
    new_l4_admin_password: Optional[PasswordArgument]
    new_slb_admin_password: Optional[PasswordArgument]
    new_webapp_admin_password: Optional[PasswordArgument]
    new_oper_password: Optional[PasswordArgument]
    new_l4_oper_password: Optional[PasswordArgument]
    new_slb_viewer_password: Optional[PasswordArgument]
    new_user_password: Optional[PasswordArgument]
    global_language_display: Optional[EnumAgNewCfgGlobalLanguage]
    user_lockout_state: Optional[EnumAgAccessNewCfgUserAutolock]
    user_lock_login_failed_attempts: Optional[int]
    user_lockout_login_duration_minute: Optional[int]
    user_lockout_login_reset_duration_minute: Optional[int]

    def __init__(self):
        self.current_admin_password = None
        self.new_admin_password = None
        self.new_l4_admin_password = None
        self.new_slb_admin_password = None
        self.new_webapp_admin_password = None
        self.new_oper_password = None
        self.new_l4_oper_password = None
        self.new_slb_viewer_password = None
        self.new_user_password = None
        self.global_language_display = None
        self.user_lockout_state = None
        self.user_lock_login_failed_attempts = None
        self.user_lockout_login_duration_minute = None
        self.user_lockout_login_reset_duration_minute = None


bean_map = {
    Root: dict(
        struct=PredefinedLocalUsersParameters,
        direct=True,
        attrs=dict(
            agAccessAdminPasswd='current_admin_password',
            agAccessAdminNewPasswd='new_admin_password',
            agAccessAdminConfNewPasswd='new_admin_password',
            # agAccessL4AdminPasswd='new_l4_admin_password',
            # agAccessSlbAdminPasswd='new_slb_admin_password',
            # agAccessWsAdminPasswd='new_webapp_admin_password',
            # agAccessOperPasswd='new_oper_password',
            # agAccessL4OperPasswd='new_l4_oper_password',
            # agAccessSlbViewerPasswd='new_slb_viewer_password',
            # agAccessUsrPasswd='new_user_password',
            agNewCfgGlobalLanguage='global_language_display',
            agAccessNewCfgUserAutolock='user_lockout_state',
            agAccessNewCfgUserLockTreshld='user_lock_login_failed_attempts',
            agAccessNewCfgUserLockDuration='user_lockout_login_duration_minute',
            agAccessNewCfgUserLockResetTime='user_lockout_login_reset_duration_minute'
        )
    )
}

predefine_pass_map = dict(
    agAccessL4AdminPasswd='new_l4_admin_password',
    agAccessSlbAdminPasswd='new_slb_admin_password',
    agAccessWsAdminPasswd='new_webapp_admin_password',
    agAccessOperPasswd='new_oper_password',
    agAccessL4OperPasswd='new_l4_oper_password',
    agAccessSlbViewerPasswd='new_slb_viewer_password',
    agAccessUsrPasswd='new_user_password',
)


class PredefinedLocalUsersConfigurator(AlteonConfigurator):
    parameters_class: ClassVar[PredefinedLocalUsersParameters]

    def __init__(self, alteon_connection):
        super(PredefinedLocalUsersConfigurator, self).__init__(bean_map, alteon_connection)

    def _read(self, parameters: PredefinedLocalUsersParameters) -> PredefinedLocalUsersParameters:
        self._read_device_beans(parameters)
        if self._beans:
            return parameters

    def _update(self, parameters: PredefinedLocalUsersParameters, dry_run: bool) -> str:
        def _set_user_pass():
            for k, v in predefine_pass_map.items():
                value = getattr(parameters, v)
                if value is not None:
                    root = Root()
                    setattr(root, 'agAccessAdminPasswd', parameters.current_admin_password)
                    setattr(root, k, value)
                    self._device_api.update(root, dry_run=dry_run)

        self._write_device_beans(parameters, dry_run=dry_run)
        _set_user_pass()
        return self._get_object_id(parameters) + MSG_UPDATE

    def delete(self, parameters: PredefinedLocalUsersParameters, dry_run=False, **kw) -> str:
        return MSG_NO_DELETE

    def _entry_bean_instance(self, parameters):
        return self._get_bean_instance(Root, parameters)

    def dry_run_delete_procedure(self, diff):
        dry_run_procedure = DryRunDeleteProcedure()
        dry_run_procedure.ignore_all_props = True
        return dry_run_procedure


