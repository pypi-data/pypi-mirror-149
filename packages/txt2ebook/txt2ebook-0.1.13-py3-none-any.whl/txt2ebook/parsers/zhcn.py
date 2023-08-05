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

import cjkwrap
import regex as re
from loguru import logger

from txt2ebook.models import Book
from txt2ebook.parsers.base import BaseParser

IDEOGRAPHIC_SPACE = "\u3000"
SPACE = "\u0020"
NUMS_WORDS = "零一二三四五六七八九十百千两"
FULLWIDTH_NUMS = "０１２３４５６７８９"
RE_NUMS = f"[.0-9{FULLWIDTH_NUMS}{NUMS_WORDS}]"
STRUCTURE_NAMES = {
    "cover": "封面",
}


class ZhCnParser(BaseParser):
    """
    Module for parsing txt format in Simplified Chinese (zh-cn).
    """

    default_re_title: str = r"书名：(.*)|【(.*)】|《(.*)》"
    default_re_author: str = r"作者：(.*)"
    default_re_volume: str = "|".join(
        [
            f"^第{RE_NUMS}*[集卷册][^。~\n]*$",
            f"^卷{RE_NUMS}.*$",
        ]
    )
    default_re_chapter: str = "|".join(
        [
            f"^第{RE_NUMS}*[章篇回折].*$",
            "^[楔引]子[^，].*$",
            "^序[章幕曲]?$",
            "^前言.*$",
            "^[内容]*简介.*$",
            "^[号番]外篇.*$",
            "^尾声$",
            "^终章.*$",
            "^后记.*$",
        ]
    )

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
            language="zh-cn",
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
        Massage the txt content.

        Returns:
          str: The book in parsed string
        """
        content = self.raw_content

        content = BaseParser.to_unix_newline(content)

        if self.re_delete:
            content = self.do_delete_regex(content)

        if self.re_replace:
            content = self.do_replace_regex(content)

        if self.re_delete_line:
            content = self.do_delete_line_regex(content)

        if self.no_wrapping:
            content = self.do_no_wrapping(content)

        if self.width:
            content = self.do_wrapping(content)

        return content

    def do_no_wrapping(self, content: str) -> str:
        """
        Remove wrapping. Paragraph should be in one line.

        Args:
            content (str): Massage book content

        Returns:
            str: Massage book content
        """
        # Convert to single spacing before we removed wrapping.
        lines = content.split("\n")
        content = "\n\n".join([line.strip() for line in lines if line])

        unwrapped_content = ""
        for line in content.split("\n\n"):
            # if a line contains more opening quote(「) than closing quote(」),
            # we're still within the same paragraph.
            # e.g.:
            # 「...」「...
            # 「...
            if line.count("「") > line.count("」"):
                unwrapped_content = unwrapped_content + line.strip()
            elif (
                re.search(r"[…。？！]{1}」?$", line)
                or re.search(r"」$", line)
                or re.match(r"^[ \t]*……[ \t]*$", line)
                or re.match(r"^「」$", line)
                or re.match(r".*[》：＊\*]$", line)
                or re.match(r".*[a-zA-Z0-9]$", line)
            ):
                unwrapped_content = unwrapped_content + line.strip() + "\n\n"
            elif re.match(self.get_regex("chapter"), line):
                # replace full-width space with half-wdith space.
                # looks nicer on the output.
                header = line.replace(IDEOGRAPHIC_SPACE * 2, SPACE).replace(
                    IDEOGRAPHIC_SPACE, SPACE
                )
                unwrapped_content = (
                    unwrapped_content + "\n\n" + header.strip() + "\n\n"
                )
            else:
                unwrapped_content = unwrapped_content + line.strip()

        return unwrapped_content

    def do_wrapping(self, content: str) -> str:
        """
        Wrapping and filling CJK text.

        Args:
            content (str): Massage book content

        Returns:
            str: Massage book content
        """
        logger.info("Wrapping paragraph to width: {}", self.width)

        paragraphs = []
        # We don't remove empty line and keep all formatting as it.
        for paragraph in content.split("\n"):
            paragraph = paragraph.strip()

            lines = cjkwrap.wrap(paragraph, width=self.width)
            paragraph = "\n".join(lines)
            paragraphs.append(paragraph)

        wrapped_content = "\n".join(paragraphs)
        return wrapped_content
