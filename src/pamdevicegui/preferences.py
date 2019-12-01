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
    gi.require_version('Gdk', '3.0')
except Exception as e:
    print(e)
    exit(1)
from gi.repository import Gtk
from gi.repository import Gdk
from .configurator import Configuration
from . import utils
from .utils import _
from .utils import set_margins


class PreferencesDialog(Gtk.Dialog):

    def __init__(self, window):
        Gtk.Dialog.__init__(self, '{} | {}'.format(
            utils.APPNAME, _('Preferences')),
            window)
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT)
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT)
        self.set_modal(True)
        self.set_destroy_with_parent(True)
        self.connect('realize', self.on_realize)
        self.set_default_response(Gtk.ResponseType.ACCEPT)
        self.set_resizable(False)
        self.set_icon_from_file(utils.ICON)
        self.init_ui()
        self.load()
        self.show_all()

    def init_ui(self):
        vbox0 = Gtk.VBox(spacing=5)
        vbox0.set_border_width(5)
        self.get_content_area().add(vbox0)

        frame1 = Gtk.Frame()
        vbox0.add(frame1)

        grid = Gtk.Grid()
        frame1.add(grid)

        label1 = Gtk.Label.new(_('Scaning bluetooth time:'))
        set_margins(label1, 15)
        grid.attach(label1, 0, 0, 1 ,1)

        self.entry1 = Gtk.SpinButton.new_with_range(1, 100, 1)
        set_margins(self.entry1, 15)
        self.entry1.set_digits(0)
        grid.attach(self.entry1, 1, 0, 1, 1)

        label2 = Gtk.Label.new(_('Check for bluetooth device time:'))
        set_margins(label2, 15)
        grid.attach(label2, 0, 1, 1 ,1)

        self.entry2 = Gtk.SpinButton.new_with_range(1, 100, 1)
        set_margins(self.entry2, 15)
        self.entry2.set_digits(0)
        grid.attach(self.entry2, 1, 1, 1, 1)

    def on_realize(self, *_):
        monitor = Gdk.Display.get_primary_monitor(Gdk.Display.get_default())
        scale = monitor.get_scale_factor()
        monitor_width = monitor.get_geometry().width / scale
        monitor_height = monitor.get_geometry().height / scale
        width = self.get_preferred_width()[0]
        height = self.get_preferred_height()[0]
        self.move((monitor_width - width)/2, (monitor_height - height)/2)

    def load(self):
        configuration = Configuration()
        self.entry1.set_value(configuration.get('bluetooth-scan-timeout'))
        self.entry2.set_value(configuration.get('bluetooth-check-timeout'))
    
    def save(self):
        configuration = Configuration()
        configuration.set('bluetooth-scan-timeout',
                          int(self.entry1.get_value()))
        configuration.set('bluetooth-check-timeout',
                          int(self.entry2.get_value()))
        configuration.save()

if __name__ == '__main__':
    preferences = PreferencesDialog(None)
    preferences.run()