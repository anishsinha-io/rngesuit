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

import os
import sys
from pathlib import Path

from dearpygui import dearpygui as dpg

from rngesuit.ui.components.button import Button
from rngesuit.ui.config.configwindow import ConfigWindow
from rngesuit.ui.config.selectdb import SelectDB
from rngesuit.ui.events import SelectDBEvent
from rngesuit.ui.framework.app import UI
from rngesuit.ui.mainwindow import MainWindow

if __package__ is None:
    sys.exit(
        "please run this script with the command: python -u -m gesu.main from the root directory where you cloned this project"
    )

ROOT_PATH = Path(os.path.dirname(os.path.abspath(__package__)))
ASSETS_PATH = ROOT_PATH / "assets"


def main():
    with UI() as ui:
        with dpg.theme() as button_theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 0, 0))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (200, 0, 0))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (150, 0, 0))

        ui.theme_manager.register_theme("button", button_theme)

        with dpg.font_registry():
            jetbrains_mono_medium_path = str(
                ASSETS_PATH
                / "fonts"
                / "jetbrains-mono"
                / "ttf"
                / "JetBrainsMono-Medium.ttf"
            )

            jetbrains_mono = dpg.add_font(
                jetbrains_mono_medium_path, 28, pixel_snapH=True
            )
        ui.theme_manager.register_font("jetbrains-mono", jetbrains_mono)

        dpg.set_global_font_scale(0.5)

        root = MainWindow(
            ConfigWindow(
                SelectDB(
                    Button(
                        label="sqlite",
                        tag="sqlite-button",
                        on_click=lambda em: em.dispatch(SelectDBEvent("sqlite")),
                    ),
                    Button(
                        label="postgresql",
                        tag="postgresql-button",
                        on_click=lambda em: em.dispatch(SelectDBEvent("postgresql")),
                    ),
                    Button(
                        label="mysql",
                        tag="mysql-button",
                        on_click=lambda em: em.dispatch(SelectDBEvent("mysql")),
                    ),
                ),
            ),
        )
        ui.root = root
        ui.run(title="RNGesuit")


if __name__ == "__main__":
    main()
