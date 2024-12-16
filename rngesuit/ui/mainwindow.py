# Copyright (C) 2024 Anish Sinha
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from typing import override

import dearpygui.dearpygui as dpg

from rngesuit.ui.events import AppEventType, SelectDBEvent
from rngesuit.ui.framework.component import Component, RootComponent
from rngesuit.ui.framework.events import Callback, EventManager
from rngesuit.ui.framework.themes import ThemeManager


class MainWindow(RootComponent):
    def __init__(self, *args: Component, tag: str = "mainwindow", **kwargs):
        self.tag = tag
        self.children = args

        self.em: EventManager
        self.tm: ThemeManager

        with dpg.stage() as stage:
            with dpg.window(label=tag, tag=tag) as window_id:
                self.id = window_id
                self.stage = stage
                dpg.set_primary_window(self.tag, value=True)
                dpg.add_text("RNGesuit")
                dpg.add_text("Hello, world!", tag="heading-tag")

        for child in self.children:
            dpg.move_item(child.id, parent=self.id)

    def before_mount(self):
        dpg.bind_font(self.tm.get_font("jetbrains-mono"))
        self.em.subscribe(
            [AppEventType.SELECT_DB],
            Callback(tag="change-heading-cb", cb=self.change_heading),
        )

    def change_heading(self, event):
        match event:
            case SelectDBEvent(database):
                dpg.set_value("heading-tag", database)

    @override
    def __call__(self):
        dpg.unstage(self.stage)
