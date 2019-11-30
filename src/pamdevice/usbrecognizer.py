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
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re
import os
import subprocess
from pamdevice.recognizer import Recognizer
from pamdevice.configurator import Configuration

DEVNULL = open(os.devnull, 'wb')

def execute_command(command):
    return subprocess.Popen(command, shell=True,
                            stdout=subprocess.PIPE,
                            stderr=DEVNULL).stdout.read()

class USBRecognizer(Recognizer):

    device_type = 'usb'

    def scan(self):
        device_re = re.compile(".*ID\s(?P<idVendor>\w+):(?P<idProduct>\w+)\s(?P<name>.+)$", re.I)
        serial_re = re.compile(".*iSerial\s+(?P<iSerial>[^\s]+)\s", re.I)
        devices = []
        df = execute_command('lsusb')
        for i in df.split('\n'):
            if i:
                info = device_re.match(i)
                if info:
                    dinfo = info.groupdict()
                    command = 'lsusb -vd {}:{}'.format(
                        dinfo['idVendor'], dinfo['idProduct'])
                    ans = execute_command(command).replace('\n', '')
                    data = serial_re.match(ans)
                    if data:
                        dserial = data.groupdict()
                        dinfo['iSerial'] = dserial['iSerial']
                    else:
                        dinfo['iSerial'] = ''
                    device = {'id': '{}:{}:{}'.format(dinfo['idVendor'], dinfo['idProduct'], dinfo['iSerial']),
                            'name': dinfo['name']}
                    devices.append(device)
        return devices

