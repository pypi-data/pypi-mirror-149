#
# Copyright (c) 2020-2021 eGauge Systems LLC
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
import pickle

from abc import ABC, abstractmethod	# ABC = abstract base class

class Error(Exception):
    pass

class SpaceExhausted(Error):
    pass

class Manager(ABC):

    def __init__(self, ui, state_path):
        '''Create a SN manager object.  UI is the QT user-interface object
        that can be used to interact with the user, e.g., to ask
        confirmation questions or to ask for authentication
        credentials, for example.  STATE_PATH is the path of a
        file that the manager can use to store state in.

        '''
        self.ui = ui
        self.path = state_path
        self.product = None
        self.serial = {}
        self._load_state()

    def has_calibration_data(self):
        '''Should return True if this serial-number manager can retrieve
        calibration data with get_calibration_data(), False otherwise.

        '''
        return False

    @abstractmethod
    def set_preferences(self, prefs):
        '''This method must be called whenever the SN manager's preferences
        may have changed.

        '''

    def set_product(self, manufacturer, model):
        '''Set the product for which to manage serial numbers.  Each product
        has its own serial-number space, so this function must be
        called at least once before any serial-numbers can be
        allocated.

        '''
        if manufacturer is None or model is None:
            self.product = None
            return True

        self.product = '%s-%s' % (manufacturer, model)
        return True

    def restore_product(self, product):
        '''Restore the product to PRODUCT.'''
        self.product = product

    def activate(self, sn):
        '''Activate automatic serial number generation using this SN manager.
        SN is the serial number that was most recently used in manual
        mode.  It may be None if the most recently used serial number
        is unavailable.  Some SN managers may choose to offer the next
        automatic serial number based on this number.

        '''

    def deactivate(self):
        '''Called when this SN manager is no longer used.  That is, when this
        method gets called when the user switches to manually entered
        serial-numbers.

        '''

    def get(self):
        '''Get the serial-number to be used next.'''
        if self.product is None:
            return None
        return self.serial.get(self.product)

    def set(self, sn):
        if self.product is None:
            return

        self.serial[self.product] = sn
        self._save_state()

    @abstractmethod
    def commit(self, sn, info, auto_serial_number):
        '''This is called after serial-number SN has been committed
        (programmed) into a device.  INFO must be a dictionary of
        information to be associated with this device.  Not all SN
        managers can preserve INFO.

        Note that this gets called even if the SN was manually
        selected (indicated by AUTH_SERIAL_NUMBER==False).  This is
        done such that if a device needs to be re-programmed (e.g.,
        with a different calibration), we get notified here with the
        latest INFO that is used for this SN.

        '''

    def get_cal_data(self, sn):
        '''Return the calibration data for the current product with serial
        number SN or None if no such data is available.

        '''
        return None

    def _load_state(self):
        try:
            with open(self.path, 'rb') as f:
                self.serial = pickle.load(f)
        except IOError:
            self.serial = {}

    def _save_state(self):
        with open(self.path, 'wb') as f:
            pickle.dump(self.serial, f)
