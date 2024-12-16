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

from dearpygui import dearpygui as dpg

from rngesuit.ui.framework.component import Component, LifecycleComponent
from rngesuit.ui.framework.events import EventManager


class ConfigWindow(LifecycleComponent):
    def __init__(self, *args: Component, tag: str = "configwindow", **kwargs):
        self.tag = tag
        self.em: EventManager
        self.children = args

        with dpg.stage():
            with dpg.child_window(
                label="Configuration",
                tag=self.tag,
                width=400,
                height=400,
                frame_style=False,
                menubar=True,
            ) as window_id:
                self.id = window_id
                dpg.add_text("Configuration")
                dpg.add_separator()
                for child in self.children:
                    dpg.move_item(child.id, parent=self.id)
