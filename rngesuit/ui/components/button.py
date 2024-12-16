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

from typing import Callable

from dearpygui import dearpygui as dpg

from rngesuit.ui.framework.component import LifecycleComponent
from rngesuit.ui.framework.events import EventManager
from rngesuit.ui.framework.themes import ThemeManager


class Button(LifecycleComponent):
    def __init__(
        self,
        label: str,
        tag: str,
        on_click: Callable[[EventManager], None] = lambda em: None,
        on_hover: Callable[[EventManager], None] = lambda em: None,
        **kwargs,
    ):
        self.tag = tag
        self.label = label
        self.children = ()
        self.em: EventManager
        self.tm: ThemeManager
        self.on_click = on_click
        self.on_hover = on_hover

        with dpg.stage():
            self.id = dpg.add_button(label=self.label, tag=self.tag, **kwargs)

            with dpg.item_handler_registry() as registry:
                dpg.add_item_clicked_handler(callback=lambda: self.on_click(self.em))
                dpg.add_item_hover_handler(callback=lambda: self.on_hover(self.em))

            dpg.bind_item_handler_registry(self.tag, registry)
