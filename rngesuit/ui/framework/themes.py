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


class ThemeManager:
    def __init__(self):
        self.themes: dict[str, str | int] = {}
        self.fonts: dict[str, str | int] = {}

    def register_theme(self, name: str, theme: str | int):
        self.themes[name] = theme

    def get_theme(self, name: str) -> str | int:
        return self.themes[name]

    def register_font(self, name: str, font: str | int):
        self.fonts[name] = font

    def get_font(self, name: str) -> str | int:
        return self.fonts[name]
