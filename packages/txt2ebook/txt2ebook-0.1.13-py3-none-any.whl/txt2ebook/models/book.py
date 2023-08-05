# Copyright (C) 2021,2022 Kian-Meng Ang
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from dataclasses import dataclass, field
from typing import List

from txt2ebook.models.chapter import Chapter
from txt2ebook.models.volume import Volume


@dataclass
class Book:
    """
    A book class model.
    """

    title: str = field(default="")
    authors: List[str] = field(default_factory=List)
    language: str = field(default="")
    cover: str = field(default="", repr=False)
    raw_content: str = field(default="", repr=False)
    massaged_content: str = field(default="", repr=False)
    parsed_content: List[tuple] = field(default_factory=List, repr=False)
    volumes: List[Volume] = field(default_factory=List, repr=False)
    chapters: List[Chapter] = field(default_factory=List, repr=False)
    structure_names: dict = field(default_factory=dict, repr=False)
