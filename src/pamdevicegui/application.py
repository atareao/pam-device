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
    gi.require_version('Gio', '2.0')
    gi.require_version('GLib', '2.0')
    gi.require_version('GdkPixbuf', '2.0')
except Exception as e:
    print(e)
    exit(1)
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import GLib
from gi.repository import GdkPixbuf

from . import utils
from .utils import _
from .mainwindow import MainWindow
import webbrowser


class MainApplication(Gtk.Application):
    """pam-device application object."""
    instance = None

    def __init__(self):
        Gtk.Application.__init__(self,
                                 application_id="es.atareao.pam-device",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.license_type = Gtk.License.MIT_X11
        GLib.set_application_name(utils.APPNAME)
        GLib.set_prgname(utils.APPNAME)
        self.win = None

        self._menu = Gio.Menu()

    @staticmethod
    def get_default():
        if Application.instance is None:
            Application.instance = Application()
        return Application.instance

    def do_startup(self):
        """Startup the application."""
        Gtk.Application.do_startup(self)
        self.__setup_actions()

    def __setup_actions(self):
        self.__add_action(
                'add_device',
                callback=self.on_headerbar_clicked)
        self.__add_action(
                'remove_device',
                callback=self.on_headerbar_clicked)
        self.__add_action(
                'goto_homepage',
                callback=lambda x, y: webbrowser.open(
                    'http://www.atareao.es/'))
        self.__add_action(
            'goto_twitter',
            callback=lambda x, y: webbrowser.open(
                'http://twitter.com/atareao'))
        self.__add_action(
            'goto_github',
            callback=lambda x, y: webbrowser.open(
                'https://github.com/atareao'))
        self.__add_action(
            'goto_code',
            callback=lambda x, y: webbrowser.open(
                'https://github.com/atareao/pam-device'))
        self.__add_action(
            'goto_bug',
            callback=lambda x, y: webbrowser.open(
                'https://github.com/atareao/pam-device/issues'))
        self.__add_action(
            'goto_sugestion',
            callback=lambda x, y: webbrowser.open(
                'https://github.com/atareao/pam-device/issues'))
        self.__add_action(
            'goto_donate',
            callback=lambda x, y: webbrowser.open(
                'https://www.atareao.es/donar/'))
        self.__add_action(
            'about',
            callback=self.on_about_activate)
        self.__add_action(
            'quit',
            callback=self.__on_quit)

        self.set_accels_for_action("app.shortcuts", ["<Ctrl>question"])
        self.set_accels_for_action("app.quit", ["<Ctrl>Q"])
        self.set_accels_for_action("app.settings", ["<Ctrl>comma"])
        self.set_accels_for_action("win.add-account", ["<Ctrl>N"])
        self.set_accels_for_action("app.add_device", ["<Ctrl>A"])
        self.set_accels_for_action("app.remove_device", ["<Ctrl>R"])

    def do_activate(self, *_):
        print('do_activate')
        if self.win is None:
            self.win = MainWindow(self)
            self.win.show_all()
        self.add_window(self.win)
        self.win.present()

    def action_clicked(self, action, variant):
        print(action, variant)
        if variant:
            action.set_state(variant)

    def on_headerbar_clicked(self, action, optional):
        self.win.on_headerbar_clicked(action, action.get_name())

    def __add_action(self, name, callback=None, var_type=None,
                     value=None):
        if var_type is None:
            action = Gio.SimpleAction.new(name, None)
        else:
            action = Gio.SimpleAction.new_stateful(
                name,
                GLib.VariantType.new(var_type),
                GLib.Variant(var_type, value)
            )
        if callback is None:
            callback = self.action_clicked
        action.connect('activate', callback)
        self.add_action(action)

    def __on_quit(self, *_):
        self.get_active_window().close()
        self.quit()

    def on_about_activate(self, widget, optional):
        ad = Gtk.AboutDialog(utils.APPNAME, self.get_active_window())
        ad.set_name(utils.APPNAME)
        ad.set_version(utils.VERSION)
        ad.set_copyright('Copyrignt (c) 2019\nLorenzo Carbonell')
        ad.set_comments(utils.APPNAME)
        ad.set_license('''
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
''')
        ad.set_website('http://www.atareao.es')
        ad.set_website_label('http://www.atareao.es')
        ad.set_authors([
            'Lorenzo Carbonell <lorenzo.carbonell.cerezo@gmail.com>'])
        ad.set_documenters([
            'Lorenzo Carbonell <lorenzo.carbonell.cerezo@gmail.com>'])
        ad.set_translator_credits('\
Lorenzo Carbonell <lorenzo.carbonell.cerezo@gmail.com>\n')
        ad.set_program_name(utils.APPNAME)
        ad.set_logo(GdkPixbuf.Pixbuf.new_from_file(utils.ICON))
        ad.run()
        ad.destroy()


def main(args):
    app = MainApplication()
    app.run(args)

if __name__ == "__main__":
    main(sys.argv)
