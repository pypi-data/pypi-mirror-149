# pylint: disable=too-few-public-methods
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

from txt2ebook.models import Book
from txt2ebook.parsers.base import BaseParser

STRUCTURE_NAMES = {
    "cover": "Cover",
}


class EnParser(BaseParser):
    """
    Module for parsing English content txt file.
    """

    default_re_title: str = r"Title:(.*)"
    default_re_author: str = r"Author:(.*)"
    default_re_volume: str = "^Volume.*$"
    default_re_chapter: str = "^Chapter.*$"

    def parse(self) -> Book:
        """
        Parse the content into volumes (optional) and chapters.

        Returns:
          txt2ebook.models.Book: The Book model
        """
        massaged_content = self.massage()
        (parsed_content, volumes, chapters) = self.parse_content(
            massaged_content
        )

        return Book(
            title=self.detect_book_title(),
            language="en",
            authors=self.detect_authors(),
            cover=self.cover,
            raw_content=self.raw_content,
            massaged_content=massaged_content,
            parsed_content=parsed_content,
            volumes=volumes,
            chapters=chapters,
            structure_names=STRUCTURE_NAMES,
        )

    def massage(self) -> str:
        """
        Massage the content.

        Returns:
          str: The book in raw string
        """
        return self.raw_content
