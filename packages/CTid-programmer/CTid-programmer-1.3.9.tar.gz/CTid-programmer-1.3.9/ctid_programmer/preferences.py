#
# Copyright (c) 2020 eGauge Systems LLC
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
import json
import os

class Manager:

    def __init__(self, state_directory_path):
        self.path = os.path.join(state_directory_path, 'preferences.json')
        self.load()

    def load(self):
        try:
            with open(self.path, 'r') as f:
                prefs = json.load(f)
                self.sn_service = prefs.get('sn_service', None)
                self.sn_increment = prefs['sn_increment']
                self.station_id = prefs['station_id']
        except IOError:
            self.sn_service = None
            self.sn_increment = 1
            self.station_id = 0

    def save(self):
        prefs = {
            'sn_service': self.sn_service,
            'sn_increment': self.sn_increment,
            'station_id': self.station_id
        }
        with open(self.path, 'w') as f:
            json.dump(prefs, f, sort_keys=True, indent=2)
