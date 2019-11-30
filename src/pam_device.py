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


import syslog
import os
import sys

sys.path.insert(1, '/lib/security')

syslog.openlog(facility=syslog.LOG_AUTH)
syslog.syslog(syslog.LOG_INFO, 'PAM device: {}'.format(os.path.dirname(os.path.abspath(__file__))))
syslog.closelog()
import pamdevice
import pamdevice.bluetoothrecognizer
from pamdevice.bluetoothrecognizer import BluetoothRecognizer
from pamdevice.usbrecognizer import USBRecognizer


class UserUnknownException(Exception):
    pass

def setPAMMessage(pamh, message, errorMessage=False):
    try:
        style = pamh.PAM_ERROR_MSG if errorMessage else pamh.PAM_TEXT_INFO
        msg = pamh.Message(style, '* PAM device: {}'.format(message))
        pamh.conversation(msg)
        return True
    except Exception as e:
        auth_log(str(e), syslog.LOG_ERR)
        return False


def auth_log(message, priority=syslog.LOG_INFO):
    syslog.openlog(facility=syslog.LOG_AUTH)
    syslog.syslog(priority, 'PAM device: {}'.format( message))
    syslog.closelog()


def pam_sm_authenticate(pamh, flags, argv):
    flags = pamh.PAM_DISALLOW_NULL_AUTHTOK
    try:
        userName = pamh.ruser if pamh.ruser else pamh.get_user()
        if userName is None:
            raise UserUnknownException('The user is not known!')

        message = 'The user "{}" is asking for permission with "{}".'.format(
            userName, pamh.service)
        auth_log(message, syslog.LOG_DEBUG)

        auth_log('Authentication request for user "{}"'.format(
            userName.encode('utf-8')))
        setPAMMessage(pamh, 'Authentication request for user "{}"'.format(
            userName.encode('utf-8')))

        usbr = USBRecognizer()
        auth_log('Recognizing USB devices ...')
        setPAMMessage(pamh, 'Recognizing USB devices ...')
        device = usbr.check()
        if device is not None:
            auth_log('Device {} is connected (good).'.format(
                device['id']))
            auth_log('Access granted!')
            setPAMMessage(pamh, 'Device "{}" is connected (good).'.format(
                device['name'].encode('utf-8')))
            setPAMMessage(pamh, 'Access granted!')
            return pamh.PAM_SUCCESS
        auth_log('No USB devices connected!', syslog.LOG_WARNING)
        setPAMMessage(pamh, 'No USB devices connected!')

        btr = BluetoothRecognizer()
        auth_log('Recognizing Bluetooth devices ...')
        setPAMMessage(pamh, 'Recognizing Bluetooth devices ...')
        device = btr.check()
        if device is not None:
            auth_log('Device {} is connected'.format(device['id']))
            auth_log('Access granted!')
            setPAMMessage(pamh, 'Device "{}" is connected (good).'.format(
                device['name'].encode('utf-8')))
            setPAMMessage(pamh, 'Access granted!')
            return pamh.PAM_SUCCESS
        auth_log('No Bluetooth devices connected!', syslog.LOG_WARNING)
        setPAMMessage(pamh, 'No Bluetooth devices connected!')

        setPAMMessage(pamh, 'Access denied!', True)
        return pamh.PAM_AUTH_ERR

    except UserUnknownException as e:
        auth_log(str(e), syslog.LOG_ERR)
        setPAMMessage(pamh, 'Access denied!', True)
        return pamh.PAM_USER_UNKNOWN

    except Exception as e:
        auth_log(str(e), syslog.LOG_ERR)
        return pamh.PAM_IGNORE

    return pamh.PAM_AUTH_ERR


def pam_sm_setcred(pamh, flags, argv):
    return pamh.PAM_SUCCESS

def pam_sm_acct_mgmt(pamh, flags, argv):
    return pamh.PAM_SUCCESS

def pam_sm_open_session(pamh, flags, argv):
    return pamh.PAM_SUCCESS

def pam_sm_close_session(pamh, flags, argv):
    return pamh.PAM_SUCCESS

def pam_sm_chauthtok(pamh, flags, argv):
    return pamh.PAM_SUCCESS