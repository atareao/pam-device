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
    gi.require_version('GLib', '2.0')
except Exception as e:
    print(e)
    exit(1)
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib
import re
import os
import bluetooth
import subprocess
from .import utils
from .utils import _
from .listboxdevices import ListBoxDevices
from .configurator import Configuration
from .asyncf import async_function
from .utils import set_margins


DEVNULL = open(os.devnull, 'wb')
DEFAULT_CURSOR = Gdk.Cursor(Gdk.CursorType.ARROW)
WAIT_CURSOR = Gdk.Cursor(Gdk.CursorType.WATCH)

def execute_command(command):
    return subprocess.Popen(command, shell=True,
                            stdout=subprocess.PIPE,
                            stderr=DEVNULL).stdout.read()


class ScanDevicesDialog(Gtk.Dialog):

    def __init__(self, window, action, devices_kind):
        Gtk.Dialog.__init__(self, '{} | {} {}'.format(
            utils.APPNAME, action.split('_')[0].capitalize(), devices_kind),
            window)
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT)
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT)
        self.set_modal(True)
        self.set_destroy_with_parent(True)
        self.connect('destroy', self.on_close)
        self.connect('hide', self.on_hide)
        self.connect('realize', self.on_realize)
        self.set_default_response(Gtk.ResponseType.ACCEPT)
        self.set_resizable(False)
        self.set_icon_from_file(utils.ICON)
        self.configuration = Configuration()
        self.init_ui(action, devices_kind)
        self.show_all()

    def init_ui(self, action, devices_kind):
        vbox0 = Gtk.VBox(spacing=5)
        vbox0.set_border_width(5)
        self.get_content_area().add(vbox0)

        frame1 = Gtk.Frame()
        vbox0.add(frame1)

        grid = Gtk.Grid()
        frame1.add(grid)

        self.label = Gtk.Label.new(_('Scaning devices...'))
        set_margins(self.label, 15)
        grid.attach(self.label, 0, 0, 1 ,1)

        self.devices_list = ListBoxDevices(devices_kind, [])

        grid.attach(self.devices_list, 0, 1, 1 ,1)

        self.get_root_window().set_cursor(WAIT_CURSOR)
        self.load_devices(action, devices_kind)

    def on_close(self):
        pass

    def on_hide(self, _):
        self.get_root_window().set_cursor(DEFAULT_CURSOR)

    def load_devices(self, action, devices_kind):
        def on_async_done(devices, error):
            if error:
                print(error)
            else:
                self.label.hide()
                self.devices_list.set_items(devices)
                self.get_root_window().set_cursor(DEFAULT_CURSOR)

        @async_function(on_done=on_async_done)
        def load_devices_async(action, devices_kind):
            devices = []
            if action == 'add_device':
                if devices_kind == 'usb':
                    devices = self.scan_usb()
                elif devices_kind == 'bluetooth':
                    devices = self.scan_bluetooth()
            elif action == 'remove_device':
                devices = self.configuration.get(devices_kind)
                for index, device in enumerate(devices):
                    devices[index]['enabled'] = False
            return devices

        load_devices_async(action, devices_kind)

    def on_close(self, *args):
        pass

    def on_realize(self, *_):
        monitor = Gdk.Display.get_primary_monitor(Gdk.Display.get_default())
        scale = monitor.get_scale_factor()
        monitor_width = monitor.get_geometry().width / scale
        monitor_height = monitor.get_geometry().height / scale
        width = self.get_preferred_width()[0]
        height = self.get_preferred_height()[0]
        self.move((monitor_width - width)/2, (monitor_height - height)/2)

    def scan_bluetooth(self):
        found = []
        timeout = self.configuration.get('bluetooth-scan-timeout')
        nearby_devices = bluetooth.discover_devices(duration=timeout,
                                                    lookup_names=True,
                                                    flush_cache=True,
                                                    lookup_class=False))
        for addr, name in nearby_devices:
            item = {'id': addr, 'name': name, 'enabled': False}
            if not self.exists_id('bluetooth', item['id']):
                found.append(item)
        return found

    def exists_id(self, devices_kind, id):
        devices = self.configuration.get(devices_kind)
        for device in devices:
            if id == device['id']:
                return True
        return False

    def get_selected(self):
        return self.devices_list.get_items()


    def scan_usb(self):
        device_re = re.compile(".*ID\s(?P<idVendor>\w+):(?P<idProduct>\w+)\s(?P<name>.+)$", re.I)
        serial_re = re.compile(".*iSerial\s+(?P<iSerial>[^\s]+)\s", re.I)
        found = []
        df = execute_command('lsusb').decode()
        for i in df.split('\n'):
            if i:
                info = device_re.match(i)
                if info:
                    dinfo = info.groupdict()
                    command = 'lsusb -vd {}:{}'.format(
                        dinfo['idVendor'], dinfo['idProduct'])
                    ans = execute_command(command).decode().replace('\n', '')
                    data = serial_re.match(ans)
                    if data:
                        dserial = data.groupdict()
                        dinfo['iSerial'] = dserial['iSerial']
                    else:
                        dinfo['iSerial'] = ''
                    item = {'id': '{}:{}:{}'.format(dinfo['idVendor'], dinfo['idProduct'], dinfo['iSerial']),
                            'name': dinfo['name'], 'enabled': False}
                    if not self.exists_id('usb', item['id']):
                        found.append(item)
        return found