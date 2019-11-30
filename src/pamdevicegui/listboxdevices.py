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

import gi
try:
    gi.require_version('Gtk', '3.0')
except Exception as e:
    print(e)
    exit(1)
from gi.repository import Gtk
from gi.repository import GObject
from .listboxrowdevice import ListBoxRowDevice

class ListBoxDevices(Gtk.ListBox):
    __gsignals__ = {
        'active-changed': (GObject.SIGNAL_RUN_FIRST,
                             GObject.TYPE_NONE, (bool,str,)),
    }

    def __init__(self, device_kind, items):
        super(ListBoxDevices, self).__init__()
        self.device_kind = device_kind
        self.ui(items)

    def get_device_kind(self):
        return self.device_kind

    def ui(self, items):
        for item in items:
            print(item)
            row = ListBoxRowDevice(item)
            row.connect('active-changed', self.on_row_active_changed)
            row.show()
            self.add(row)

    def on_row_active_changed(self, widget, enabled):
        self.emit('active-changed', enabled, widget.get_item()['id'])

    def get_items(self):
        items = []
        for child in self.get_children():
            item = child.get_item()
            if item['enabled']:
                items.append(item)
        return items

    def clear(self):
        for child in self.get_children():
            self.remove(child)

    def set_items(self, items):
        self.clear()
        self.ui(items)
        self.show_all()