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

from rngesuit.ui.framework.component import Component, RootComponent
from rngesuit.ui.framework.events import EventManager
from rngesuit.ui.framework.themes import ThemeManager


class UI:
    def __init__(self) -> None:
        self.root: RootComponent | None = None
        self.event_manager = EventManager()
        self.theme_manager = ThemeManager()

    def __enter__(self):
        dpg.create_context()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        dpg.destroy_context()

    def get_callbacks(self, callback_type: str):
        if self.root is None:
            raise ValueError("Root component is not set")

        def collect_callbacks(component: Component) -> list[Callable[[], None]]:
            callbacks = [getattr(component, callback_type)]
            if component.children:
                for child in component.children:
                    callbacks.extend(collect_callbacks(child))
            return callbacks

        return collect_callbacks(self.root)

    def inject_event_manager(self) -> None:
        if self.root is None:
            raise ValueError("Root component is not set")

        def inject_em(component: Component) -> None:
            setattr(component, "em", self.event_manager)
            if component.children:
                for child in component.children:
                    inject_em(child)

        inject_em(self.root)

    def inject_theme_manager(self) -> None:
        if self.root is None:
            raise ValueError("Root component is not set")

        def inject_tm(component: Component) -> None:
            setattr(component, "tm", self.theme_manager)
            if component.children:
                for child in component.children:
                    inject_tm(child)

        inject_tm(self.root)

    def run(self, *args, title: str, **kwargs) -> None:
        if self.root is None:
            raise ValueError("root component is not set")

        dpg.create_viewport(title=title)
        dpg.setup_dearpygui()

        dpg.set_viewport_resizable(True)

        self.inject_event_manager()
        self.inject_theme_manager()

        before_mount_callbacks = self.get_callbacks("before_mount")
        mount_callbacks = self.get_callbacks("mount")
        update_callbacks = self.get_callbacks("update")
        unmount_callbacks = self.get_callbacks("unmount")

        for cb in before_mount_callbacks:
            cb()

        self.root(*args, **kwargs)

        for cb in mount_callbacks:
            cb()

        dpg.show_viewport()
        while dpg.is_dearpygui_running():
            for cb in update_callbacks:
                cb()
            dpg.render_dearpygui_frame()

        for cb in unmount_callbacks:
            cb()
