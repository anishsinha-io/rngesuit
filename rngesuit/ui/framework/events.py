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

from typing import Callable, Protocol


class Event(Protocol):
    def ty(self) -> str: ...


EventCallback = Callable[[Event], None]


class Callback:
    def __init__(self, tag: str, cb: Callable[[Event], None]) -> None:
        self.tag = tag
        self.cb = cb

    def __call__(self, event: Event) -> None:
        self.cb(event)


class EventManager:
    def __init__(self) -> None:
        self.subscribers: dict[str, list[Callback]] = {}

    def subscribe(self, event_type: list[str], callback: Callback) -> None:
        for et in event_type:
            if et not in self.subscribers:
                self.subscribers[et] = []
            self.subscribers[et].append(callback)

    def unsubscribe(self, event_type: list[str], tag: str) -> None:
        for et in event_type:
            if et in self.subscribers:
                self.subscribers[et] = [
                    cb for cb in self.subscribers[et] if cb.tag != tag
                ]

    def dispatch(self, event: Event) -> None:
        for callback in self.subscribers.get(event.ty(), []):
            callback(event)
