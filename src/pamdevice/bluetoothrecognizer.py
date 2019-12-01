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

import bluetooth
import getpass
from pamdevice.recognizer import Recognizer
from pamdevice.configurator import Configuration

class BluetoothRecognizer(Recognizer):

    device_type = 'bluetooth'

    def scan(self):
        found = []
        configuration = Configuration()
        timeout = configuration.get('bluetooth-scan-timeout')
        nearby_devices = bluetooth.discover_devices(duration=timeout,
                                                    lookup_names=True,
                                                    flush_cache=True,
                                                    lookup_class=False))
        for addr, name in nearby_devices:
            item = {'id': addr, 'name': name}
            found.append(item)
        return found

    def is_device_connected(self, item_id):
        configuration = Configuration()
        timeout = configuration.get('bluetooth-check-timeout')
        name = bluetooth.lookup_name(item_id.decode(), timeout=timeout)
        return name is not None