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
from .utils import set_margins


class ListBoxRowDevice(Gtk.ListBoxRow):
    __gsignals__ = {
        'active-changed': (GObject.SIGNAL_RUN_FIRST,
                             GObject.TYPE_NONE, (bool,)),
    }

    def __init__(self, item):
        super(Gtk.ListBoxRow, self).__init__()
        self.set_name('listboxrowdevice')
        self.ui()
        self.set_item(item)


    def ui(self):
        grid = Gtk.Grid()
        self.add(grid)

        self.label_id = Gtk.Label.new()
        self.label_id.set_width_chars(30)
        set_margins(self.label_id, 10)
        grid.attach(self.label_id, 0, 0, 1, 1)

        self.label_name = Gtk.Label.new()
        self.label_name.set_width_chars(50)
        set_margins(self.label_name, 10)
        grid.attach(self.label_name, 1, 0, 1, 1)

        self.switch_enabled = Gtk.Switch.new()
        set_margins(self.switch_enabled, 10)
        self.switch_enabled.connect('state-set', self.on_active_changed)
        grid.attach(self.switch_enabled, 2, 0, 1, 1)

    def on_active_changed(self, widget, state, on_load=True):
        self.emit('active-changed', self.switch_enabled.get_active())

    def set_item(self, item):
        print('=====', item, '====')
        self.label_id.set_text(item['id'])
        self.label_name.set_text(item['name'])
        self.switch_enabled.set_active(item['enabled'])

    def get_item(self):
        id = self.label_id.get_text()
        name = self.label_name.get_text()
        enabled = self.switch_enabled.get_active()
        return {'id':id, 'name':name, 'enabled':enabled}


