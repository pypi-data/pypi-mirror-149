#
# Copyright (c) 2020-2022 eGauge Systems LLC
#       1644 Conestoga St, Suite 2
#       Boulder, CO 80301
#       voice: 720-545-9767
#       email: davidm@egauge.net
#
# All rights reserved.
#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# pylint: disable=no-name-in-module
#
'''Serial number allocation via the eGauge serial-number API.'''

import logging
import os

from PySide2.QtWidgets import QMessageBox

from egauge import ctid
from egauge import webapi

from egauge.webapi.cloud.credentials import CredentialsManager, LoginCanceled

from ctid_programmer import sn

log = logging.getLogger(__name__)

class Manager(sn.Manager):
    def auth_wrapper(self, method, *args, **kwargs):
        while True:
            try:
                ret = method(*args, *kwargs)
                self.credentials_manager.previous_login_failed = False
                return ret
            except webapi.json_api.UnauthenticatedError:
                pass
            except LoginCanceled:
                return None

    def __init__(self, ui, state_directory_path):
        SerialNumberWithAuth \
            = webapi.decorate_public(webapi.cloud.SerialNumber,
                                     self.auth_wrapper)
        self.credentials_manager = CredentialsManager(ui)
        self.sn_api = SerialNumberWithAuth(
            auth=webapi.auth.TokenAuth(ask=self.credentials_manager.ask))
        super().__init__(ui, os.path.join(state_directory_path,
                                          'egauge_sn_api.bin'))

    def has_calibration_data(self):
        '''Should return True if this serial-number manager can retrieve
        calibration data with get_calibration_data(), False otherwise.

        '''
        return True

    def set_product(self, manufacturer, model):
        log.debug('set_product: manufacturer=%s, model=%s',
                  manufacturer, model)

        mfg = ctid.mfg_short_name(manufacturer)
        if not super().set_product(mfg, model):
            return False

        model_list = None
        try:
            model_list = self.sn_api.get_models()
        except webapi.Error:
            pass

        if model_list is None:
            QMessageBox.critical(self.ui, 'Serial-number service failed',
                                 'Serial-number service failed to return '
                                 'model-name list.  '
                                 'Reverting to manual '
                                 'serial numbers.', QMessageBox.Ok)
            return False

        found = False
        for r in model_list:
            if r['name'] == self.product:
                found = True
                break
        if found:
            return True

        choice = QMessageBox \
                 .question(self.ui,
                           'Create Serial-Number Record?',
                           ('The eGauge Serial-Number service has no record '
                            'of product \"%s %s\".  Would you like to '
                            'create one?'
                            % (mfg, model)), QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.No:
            return False

        result = None
        try:
            result = self.sn_api.create_model(self.product, 0xffffff)
        except webapi.Error:
            log.exception('sn_api.create_model() for model "%s" failed',
                          self.product)
        return result

    def set_preferences(self, prefs):
        pass

    def get(self):
        # see if we already have a serial-number for this product:
        sn = super().get()
        if sn is not None:
            log.debug('get: product=%s; using existing SN %s',
                      self.product, sn)
            return sn

        log.debug('get: product=%s; allocating new SN ', self.product)
        return self._allocate_sn()

    def commit(self, sn, info, auto_serial_number):
        meta = {}
        try:
            ret = self.sn_api.get_metadata(self.product, sn)
            if ret is not None:
                meta = ret
        except webapi.Error:
            log.exception('commit: no metadata found for %s SN %s.',
                          self.product, sn)
        meta['ctid'] = info
        try:
            self.sn_api.set_metadata(self.product, sn, meta)
        except webapi.Error as e:
            QMessageBox.warning(self.ui, 'Failed to save CTid info',
                                'Failed to save meta data for product %s '
                                'serial-number %s: %s.' \
                                % (self.product, sn, e), QMessageBox.Ok)

        if auto_serial_number:
            self._allocate_sn()		# allocate serial number to use next
        else:
            super().set(None)

    def get_cal_data(self, sn):
        try:
            meta = self.sn_api.get_metadata(self.product, sn)
        except webapi.Error:
            log.exception('Failed to get cal data for %s SN %s.',
                          self.product, sn)
            return None

        if meta is None:
            return None
        if 'cal' in meta:
            cal = meta['cal']
        elif 'ntc' in meta:
            # for backwards compatibility:
            cal = {}
            for key, value in meta['ntc'].items():
                cal['ntc_%s' % key] = str(value)
        else:
            return None
        return cal

    def _allocate_sn(self):
        # allocate a new serial number:
        super().set(None)
        try:
            sn = self.sn_api.allocate(self.product)
            if sn is None:
                return None
        except webapi.Error as e:
            log.exception('Failed to allocate SN for product %s.',
                          self.product)
            if len(e.args) > 2 and isinstance(e.args[2], list) \
               and len(e.args[2]) >= 1:
                errors = e.args[2]
                # If this product is out of serial-numbers, let the user know:
                if errors[0] == 'Maximum serial number reached':
                    raise sn.SpaceExhausted
                QMessageBox.critical(self.ui, 'Serial-number Failure',
                                     'Failed to allocate serial-number: %s'
                                     % '\n'.join(errors),
                                     QMessageBox.Ok)
            else:
                QMessageBox.critical(self.ui, 'Serial-number Failure',
                                     'Failed to allocate serial-number: %s'
                                     % e, QMessageBox.Ok)
            return None

        super().set(sn)
        return sn
