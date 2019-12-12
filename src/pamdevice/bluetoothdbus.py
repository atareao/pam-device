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

import dbus
import time
import logging
from dbus.mainloop.glib import DBusGMainLoop
from dbus import service # pylint: disable=W0611
from dbus import DBusException


logger = logging.getLogger(__name__)

SERVICE_NAME = 'org.bluez'
ADAPTER_INTERFACE = SERVICE_NAME + '.Adapter1'
DEVICE_INTERFACE = SERVICE_NAME + '.Device1'


class BluetoothDBusException(Exception):
    pass


def get_managed_objects():
    bus = dbus.SystemBus()
    manager = dbus.Interface(bus.get_object(SERVICE_NAME, '/'),
                             'org.freedesktop.DBus.ObjectManager')
    return manager.GetManagedObjects()


def find_device(device_address, adapter_pattern=None):
    return find_device_in_objects(
        get_managed_objects(), device_address, adapter_pattern)


def find_device_in_objects(objects, device_address, adapter_pattern=None):
    bus = dbus.SystemBus()
    path_prefix = ""

    if adapter_pattern:
        adapter = find_adapter_in_objects(objects, adapter_pattern)
        path_prefix = adapter.object_path

    for path, ifaces in objects.items():
        device = ifaces.get(DEVICE_INTERFACE)

        if device is None:
            continue

        if (device["Address"] == device_address and path.startswith(
                path_prefix)):
            obj = bus.get_object(SERVICE_NAME, path)
            return dbus.Interface(obj, DEVICE_INTERFACE)

    raise BluetoothDBusException("Bluetooth device not found")


def find_adapter(pattern=None):
    return find_adapter_in_objects(get_managed_objects(), pattern)


def find_adapter_in_objects(objects, pattern=None):
    bus = dbus.SystemBus()
    for path, ifaces in objects.items():
        adapter = ifaces.get(ADAPTER_INTERFACE)
        if adapter is None:
            continue
        if not pattern or pattern == adapter["Address"] or path.endswith(
                pattern):
            obj = bus.get_object(SERVICE_NAME, path)
            return dbus.Interface(obj, ADAPTER_INTERFACE)

    raise BluetoothDBusException('Bluetooth adapter not found')


def scan(timeout=10):
    try:
        adapter = find_adapter()
    except (BluetoothDBusException,
            dbus.exceptions.DBusException) as error:
        logger.error(str(error) + "\n")
    else:
        try:
            adapter.SetDiscoveryFilter({'Transport': 'auto'})
            adapter.StartDiscovery()
            time.sleep(timeout)
            adapter.StopDiscovery()
        except dbus.exceptions.DBusException as error:
            logger.error(str(error) + "\n")


def get_devices():
    devices = []
    try:
        objects = get_managed_objects()

        for path, interfaces in objects.items():
            if DEVICE_INTERFACE in interfaces:
                print(path)
                dev = interfaces[DEVICE_INTERFACE]
                if "Address" not in dev:
                    continue
                if "Name" not in dev:
                    dev["Name"] = "<unknown>"
                device = {
                    "mac_address": dev["Address"].encode("utf-8"),
                    "name": dev["Name"].encode("utf-8")
                }
                adevice = find_device(dev["Address"])
                try:
                    #adevice.Connect()
                    bus = dbus.SystemBus()
                    manager = dbus.Interface(bus.get_object(SERVICE_NAME, '/'),
                             'org.freedesktop.DBus.ObjectManager')
                    device_object = bus.get_object('org.bluez', path)
                    _object = dbus.Interface(device_object, 'org.bluez.Device1')
                    _properties = dbus.Interface(_object, 'org.freedesktop.DBus.Properties')
                    print(_properties.Get(DEVICE_INTERFACE, 'Name'))
                    if _properties.Get(DEVICE_INTERFACE, 'Connected') == 1:
                        devices.append(device)
                except Exception as e:
                    print(e)
                # props = adevice.GetAll()
                # print("\n".join(("%s: %s" % (k, props[k]) for k in props)))
                
    except dbus.exceptions.DBusException as error:
        logger.error(str(error) + "\n")

    return devices



if __name__ == '__main__':
    scan(10)
    print(get_devices())
