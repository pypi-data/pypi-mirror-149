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
'''Local serial number manager.

This manager works locally (no network connectivity required) and
assumes that there may be up to N different programming stations.  It
returns a sequence of serial numbers that are guaranteed to be unique,
provided the station id of each station is unique and the step value
is >= N.

'''

import os

from PySide2.QtWidgets import QMessageBox

from ctid_programmer import sn

class Manager(sn.Manager):

    def __init__(self, ui, state_directory_path):
        super().__init__(ui, os.path.join(state_directory_path,
                                          'serial_numbers.bin'))
        self.increment = 1
        self.first = 0

    def set_preferences(self, prefs):
        self._set_stepping(prefs.sn_increment, prefs.station_id)

    def activate(self, sn):
        old_sn = self.get()
        if old_sn is None:
            self._reset_serial_number(sn)
        elif sn != old_sn:
            choice = QMessageBox \
                     .question(self.ui,
                               'Serial Number Selection',
                               ('Would you like to switch to %d '
                                'as the next automatic serial number '
                                'for this product?  If you press "No", '
                                'the program will revert back to '
                                'the old sequence and use %d '
                                'as the next automatic serial number.'
                                % (sn, old_sn)),
                               QMessageBox.Yes, QMessageBox.No)
            if choice == QMessageBox.Yes:
                self._reset_serial_number(sn)

    def deactivate(self):
        pass

    def get(self):
        sn = super().get()
        if sn is None:
            sn = self.first
            super().set(sn)
        return sn

    def commit(self, sn, info, auto_serial_number):
        if auto_serial_number:
            self._increment_serial_number()
        else:
            super().set(None)

    def _set_stepping(self, increment, first):
        if increment < 1:
            raise ValueError('Increment must be greater than 0.')
        if first >= increment:
            raise ValueError('First valid serial-number must be in range '
                             '0..%d.' % (self.increment - 1))
        self.increment = increment
        self.first = first

    def _next_valid_serial_number(self, sn):
        mod = sn % self.increment
        if mod != self.first:
            # round up to first valid serial number
            sn += (self.first - mod) % self.increment
        return sn

    def _increment_serial_number(self):
        super().set(super().get() + self.increment)

    def _reset_serial_number(self, new_next_serial_number):
        next_sn = self._next_valid_serial_number(new_next_serial_number)
        super().set(next_sn)
