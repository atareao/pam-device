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

import abc
from pamdevice.configurator import Configuration

class Recognizer(object):

    device_type = None

    @abc.abstractmethod
    def scan(self):
        pass

    def exists(self, item_id):
        configuration = Configuration()
        items = configuration.get(self.device_type)
        for item in items:
            if item['id'] == item_id:
                return True
        return False

    def add(self, item):
        if not self.exists(item['id']):
            configuration = Configuration()
            items = configuration.get(self.device_type)
            items.append(item)
            configuration.set(_device, items)
            configuration.save()

    def remove(self, item_id):
        if self.exists(item_id):
            configuration = Configuration()
            items = configuration.get(self.device_type)
            for index, item in enumerate(items):
                if item['id'] == item_id:
                    del items[index]
                    break
            configuration.set(self.device_type, items)
            configuration.save()

    def is_device_connected(self, item_id):
        for device in self.scan():
            if device['id'] == item_id:
                return True
        return False


    def check(self):
        configuration = Configuration()
        for item in configuration.get(self.device_type):
            if item['enabled'] and self.is_device_connected(item['id']):
                return {'id': item['id'], 'name': item['name']}
        return None