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

from typing import Protocol


class Component(Protocol):
    id: int | str
    tag: str
    children: tuple["Component", ...] | None

    def __init__(self, *args: "Component", **kwargs) -> None: ...

    def before_mount(self) -> None: ...
    def mount(self) -> None: ...
    def update(self) -> None: ...
    def unmount(self) -> None: ...


class LifecycleComponent(Component):
    def before_mount(self) -> None:
        pass

    def mount(self) -> None:
        pass

    def update(self) -> None:
        pass

    def unmount(self) -> None:
        pass


class RootComponent(LifecycleComponent):
    def __call__(self) -> None: ...
