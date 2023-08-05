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

from typing import Any

from txt2ebook.formats.epub import EpubWriter
from txt2ebook.formats.txt import TxtWriter
from txt2ebook.helpers import load_class, to_classname
from txt2ebook.models import Book


def create_format(book: Book, config: dict) -> Any:
    """
    Factory method to create ebook formatter by format.
    """
    class_name = to_classname(config.format, "Writer")
    klass = load_class("txt2ebook.formats", class_name)
    formatter = klass(book, config)
    return formatter


__all__ = [
    "Book",
    "EpubWriter",
    "TxtWriter",
]
