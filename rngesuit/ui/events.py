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

from dataclasses import dataclass
from enum import StrEnum


class AppEventType(StrEnum):
    TEST = "change_heading_text"
    SELECT_DB = "select_db"


@dataclass
class TestEvent:
    data: str

    def ty(self) -> AppEventType:
        return AppEventType.TEST


@dataclass
class SelectDBEvent:
    database: str

    def ty(self) -> AppEventType:
        return AppEventType.SELECT_DB
