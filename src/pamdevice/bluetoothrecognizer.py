#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of pam-device
#
# Copyright (c) 2019 Lorenzo Carbonell Cerezo <atareao@atareao.es>
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
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re
from pamdevice.recognizer import execute_command, Recognizer


class BluetoothRecognizer(Recognizer):

    device_type = 'bluetooth'

    def scan(self):
        device_re = re.compile(r"^\s+([^\s]+)\s+(.*)$", re.I)
        devices = []
        df = execute_command('hcitool scan --flush')
        for i in df.split('\n'):
            if i:
                info = device_re.match(i)
                if info:
                    dinfo = info.groups()
                    if len(dinfo) == 2:
                        device = {'id': dinfo[0], 'name': dinfo[1]}
                        devices.append(device)
        return devices

    def is_device_connected(self, item_id):
        df = execute_command('hcitool name {}'.format(item_id))
        if df:
            return True
        return False
