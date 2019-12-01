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

from pamdevice.bluetoothrecognizer import BluetoothRecognizer

if __name__ == '__main__':
    #btr = BluetoothRecognizer()
    # print(btr.scan())
    #print(btr.check())

    print("Performing inquiry...")

    import bluetooth

    #nearby_devices = bluetooth.discover_devices(duration=1, lookup_names=True, flush_cache=True, lookup_class=False)
    nearby_devices = bluetooth.discover_devices(duration=2, lookup_names=False, flush_cache=False, lookup_class=False)

    print("Found {} devices".format(len(nearby_devices)))

    for device in nearby_devices:
        print(device)
