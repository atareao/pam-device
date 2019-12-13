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

import gi
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('Gdk', '3.0')
    gi.require_version('Gio', '2.0')
    gi.require_version('GObject', '2.0')
except Exception as e:
    print(e)
    exit(1)
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gio
from gi.repository import GObject
from . import utils
from .utils import _
from .listboxdevices import ListBoxDevices
from .configurator import Configuration
from .scandevices import ScanDevicesDialog
from .preferences import PreferencesDialog

DEFAULT_CURSOR = Gdk.Cursor(Gdk.CursorType.ARROW)
WAIT_CURSOR = Gdk.Cursor(Gdk.CursorType.WATCH)

PAGE_USB = 0
PAGE_BLUETOOTH = 1
PAGE_FACE = 2


def createLabelWithImage(label, image):
    mainbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 5)
    mainbox.pack_start(Gtk.Label.new(label), False, False, 5)
    mainbox.pack_start(Gtk.Image.new_from_icon_name(
        image, Gtk.IconSize.BUTTON), False, False, 5)
    mainbox.show_all()
    return mainbox


def is_device_in_devices(adevice, devices):
    for device in devices:
        if device['id'] == adevice['id']:
            return True
    return False


class MainWindow(Gtk.ApplicationWindow):
    __gsignals__ = {
        'text-changed': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE,
                         (object,)),
        'save-me': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE,
                    (object,)), }

    def __init__(self, app, files=[]):
        Gtk.ApplicationWindow.__init__(self, application=app)
        self.app = app
        self.set_icon_from_file(utils.ICON)
        self.connect('destroy', self.on_close)
        self.connect('realize', self.on_realize)
        self.get_root_window().set_cursor(WAIT_CURSOR)

        self.init_headerbar()

        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        self.listBox = {}
        # USB
        configuration = Configuration()
        usbs = configuration.get('usb')
        self.listBox['usb'] = ListBoxDevices('usb', usbs)
        self.listBox['usb'].connect('active-changed',
                                    self.on_usb_active_changed)

        self.notebook.append_page(self.listBox['usb'], createLabelWithImage(
            'USB', 'drive-removable-media-usb'))

        bluetooths = configuration.get('bluetooth')
        self.listBox['bluetooth'] = ListBoxDevices('bluetooth', bluetooths)
        self.notebook.append_page(
            self.listBox['bluetooth'],
            createLabelWithImage('Bluetooth', 'bluetooth-active-symbolic'))

        self.get_root_window().set_cursor(DEFAULT_CURSOR)
        self.set_default_size(700, 400)
        self.show_all()

    def on_usb_active_changed(self, widget, state, id):
        print(widget, state, id)
        configuration = Configuration()
        devices = configuration.get(widget.get_device_kind())
        for index, device in enumerate(devices):
            if device['id'] == id:
                devices[index]['enabled'] = state
            break
        configuration.set(widget.get_device_kind(), devices)
        configuration.save()

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

    def on_row_activated(self, lb, sidewidget):
        self.stack.set_visible_child_name(sidewidget.get_stack())

    def on_apply_clicked(self, *args):
        print(self.notebook.get_current_page())

    def init_headerbar(self):
        self.control = {}
        self.menu_selected = 'suscriptions'
        #
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = utils.APPNAME
        self.set_titlebar(hb)

        help_model = Gio.Menu()

        help_section0_model = Gio.Menu()
        help_section0_model.append(_('Add device'), 'app.add_device')
        help_section0_model.append(_('Remove device'), 'app.remove_device')
        help_section0 = Gio.MenuItem.new_section(None, help_section0_model)
        help_model.append_item(help_section0)

        help_section1_model = Gio.Menu()
        help_section1_model.append(_('Configuration'), 'app.preferences')
        help_section1 = Gio.MenuItem.new_section(None, help_section1_model)
        help_model.append_item(help_section1)

        help_section2_model = Gio.Menu()
        help_section2_model.append(_('Homepage'), 'app.goto_homepage')
        help_section2 = Gio.MenuItem.new_section(None, help_section2_model)
        help_model.append_item(help_section2)

        help_section3_model = Gio.Menu()
        help_section3_model.append(_('Code'), 'app.goto_code')
        help_section3_model.append(_('Issues'), 'app.goto_bug')
        help_section3 = Gio.MenuItem.new_section(None, help_section3_model)
        help_model.append_item(help_section3)

        help_section4_model = Gio.Menu()
        help_section4_model.append(_('Twitter'), 'app.goto_twitter')
        help_section4_model.append(_('GitHub'), 'app.goto_github')
        help_section4 = Gio.MenuItem.new_section(None, help_section4_model)
        help_model.append_item(help_section4)

        help_section5_model = Gio.Menu()
        help_section5_model.append(_('Donations'), 'app.goto_donate')
        help_section5 = Gio.MenuItem.new_section(None, help_section5_model)
        help_model.append_item(help_section5)

        help_section6_model = Gio.Menu()
        help_section6_model.append(_('About'), 'app.about')
        help_section6 = Gio.MenuItem.new_section(None, help_section6_model)
        help_model.append_item(help_section6)

        help_section7_model = Gio.Menu()
        help_section7_model.append(_('Quit'), 'app.quit')
        help_section7 = Gio.MenuItem.new_section(None, help_section7_model)
        help_model.append_item(help_section7)

        self.control['help'] = Gtk.MenuButton()
        self.control['help'].set_tooltip_text(_('Help'))
        self.control['help'].set_menu_model(help_model)
        self.control['help'].add(Gtk.Image.new_from_gicon(Gio.ThemedIcon(
            name='open-menu-symbolic'), Gtk.IconSize.BUTTON))
        hb.pack_end(self.control['help'])

    def on_headerbar_clicked(self, action, action_name):
        if action_name == 'preferences':
            preferencesDialog = PreferencesDialog(self)
            if preferencesDialog.run() == Gtk.ResponseType.ACCEPT:
                preferencesDialog.save()
            preferencesDialog.destroy()
        else:
            dialog = None
            if self.notebook.get_current_page() == PAGE_USB:
                device_kind = 'usb'
            elif self.notebook.get_current_page() == PAGE_BLUETOOTH:
                device_kind = 'bluetooth'
            else:
                device_kind = None
            dialog = ScanDevicesDialog(self, action_name, device_kind)
            if dialog.run() == Gtk.ResponseType.ACCEPT:
                if action_name == 'add_device':
                    new_devices = dialog.get_selected()
                    if new_devices:
                        configuration = Configuration()
                        devices = configuration.get(device_kind)
                        devices.extend(new_devices)
                        configuration.set(device_kind, devices)
                        configuration.save()
                        self.listBox[device_kind].set_items(devices)
                elif action_name == 'remove_device':
                    devices_to_remove = dialog.get_selected()
                    if devices_to_remove:
                        configuration = Configuration()
                        remain_devices = []
                        for device in configuration.get(device_kind):
                            if not is_device_in_devices(
                                    device, devices_to_remove):
                                remain_devices.append(device)
                        configuration.set(device_kind, remain_devices)
                        configuration.save()
                        self.listBox[device_kind].set_items(remain_devices)
            dialog.destroy()

    def on_toggled(self, widget, arg):
        if widget.get_active() is True:
            if arg == self.menu_selected:
                if self.menu[arg].get_active() is False:
                    self.menu[arg].set_active(True)
            else:
                old = self.menu_selected
                self.menu_selected = arg
                self.menu[old].set_active(False)
        else:
            if self.menu_selected == arg:
                widget.set_active(True)
