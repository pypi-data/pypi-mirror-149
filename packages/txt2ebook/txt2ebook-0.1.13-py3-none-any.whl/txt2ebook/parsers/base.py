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

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

import regex as re
from loguru import logger

from txt2ebook.models import Chapter, Volume


@dataclass
class BaseParser(ABC):
    """
    Abstract base class for all Parser classes.
    """

    raw_content: str = field()
    config: dict = field()

    default_re_title: str = field(init=False)
    default_re_author: str = field(init=False)
    default_re_volume: str = field(init=False)
    default_re_chapter: str = field(init=False)

    def __getattr__(self, key):
        if key in self.config.keys():
            return self.config[key]

        raise AttributeError(key)

    @abstractmethod
    def parse(self):
        """
        Parsing function to be implemented by child class.
        """
        raise NotImplementedError

    def get_regex(self, metadata) -> str:
        """
        Get the regex by the book metadata we want to parse and extract.

        Args:
          metadata(str): The type of the regex for each parser by language.

        Returns:
          str: The regex of the type.
        """
        regexs = getattr(self, f"re_{metadata}")
        if regexs:
            return regexs if metadata == "replace" else "|".join(regexs)

        return getattr(self, f"default_re_{metadata}")

    def detect_book_title(self) -> str:
        """
        Extract book title from the content of the txt file.

        Returns:
          str: The extracted book title
        """
        if self.title:
            return self.title

        match = re.search(self.get_regex("title"), self.raw_content)
        if match:
            book_title = next(
                (title.strip() for title in match.groups() if title)
            )
            logger.info("Found book title: {}", book_title)
            return book_title

        logger.info("No book title found from file!")
        return ""

    def detect_authors(self) -> list:
        """
        Extract author from the content of the txt file.

        Returns:
          list: A list of author names
        """
        if self.author:
            return self.author

        match = re.search(self.get_regex("author"), self.raw_content)
        if match:
            author = match.group(1).strip()
            logger.info("Found author: {}", author)
            return [author]

        logger.info("No author found from file!")
        return []

    @staticmethod
    def to_unix_newline(content: str) -> str:
        """
        Convert all other line ends to Unix line end.

        Args:
          content(str): The book content

        Returns:
          str: The formatted book content
        """
        return content.replace("\r\n", "\n").replace("\r", "\n")

    def do_delete_regex(self, content: str) -> str:
        """
        Remove words/phrases based on regex.

        Args:
          content(str): The book content

        Returns:
          str: The formatted book content
        """
        for delete_regex in self.get_regex("delete"):
            content = re.sub(
                re.compile(rf"{delete_regex}", re.MULTILINE), "", content
            )
        return content

    def do_replace_regex(self, content: str) -> str:
        """
        Replace words/phrases based on regex.

        Args:
          content(str): The book content

        Returns:
          str: The formatted book content
        """
        for search, replace in self.get_regex("replace"):
            content = re.sub(
                re.compile(rf"{search}", re.MULTILINE), rf"{replace}", content
            )
        return content

    def do_delete_line_regex(self, content: str) -> str:
        """
        Delete whole line based on regex.

        Args:
          content(str): The book content

        Returns:
          str: The formatted book content
        """
        for delete_line_regex in self.get_regex("delete_line"):
            content = re.sub(
                re.compile(rf"^.*{delete_line_regex}.*$", re.MULTILINE),
                "",
                content,
            )
        return content

    def parse_content(self, content: str) -> tuple:
        """
        Parse the content into volumes (if exists) and chapters.

        Args:
          content(str): The book content

        Returns:
          tuple: The formatted book content, volumes (if exists), and chapters
        """
        volume_pattern = re.compile(self.get_regex("volume"), re.MULTILINE)
        volume_headers = re.findall(volume_pattern, content)

        volumes = []
        chapters = []

        if not volume_headers:
            logger.info("Found volumes: 0")
            (parsed_content, chapters) = self.parse_chapters(content)
            if parsed_content:
                logger.info("Found chapters: {}", len(parsed_content))
            else:
                logger.error("Found chapters: 0")
        else:
            logger.info("Found volumes: {}", len(volume_headers))
            volume_bodies = re.split(volume_pattern, content)
            parsed_volumes = list(zip(volume_headers, volume_bodies[1:]))

            parsed_content = []
            for volume_header, body in parsed_volumes:
                (parsed_body, chapters) = self.parse_chapters(body)
                if parsed_body:
                    parsed_content.append((volume_header, parsed_body))
                    volumes.append(
                        Volume(
                            title=volume_header,
                            raw_content=body,
                            chapters=chapters,
                        )
                    )
                else:
                    logger.error(
                        "Found 0 chapters for volume: {}", volume_header
                    )

        return (parsed_content, volumes, chapters)

    def parse_chapters(self, content: str) -> tuple:
        """
        Split the content of txt file into chapters by chapter regex.

        Args:
          content(str): The book content

        Returns:
          tuple: A list of parsed chapters and chapters
        """
        regex = re.compile(self.get_regex("chapter"), re.MULTILINE)
        headers = re.findall(regex, content)

        if not headers:
            return (False, [])

        bodies = re.split(regex, content)
        parsed_chapters = list(zip(headers, bodies[1:]))

        chapters = []
        for title, body in parsed_chapters:
            title = title.rstrip()
            paragraphs = self.parse_paragraphs(body, title)
            chapters.append(
                Chapter(title=title, raw_content=body, paragraphs=paragraphs)
            )

        return (parsed_chapters, chapters)

    def parse_paragraphs(self, body: str, title: str) -> List[str]:
        """
        Split the body of text into list of individual paragraph.

        With assumptions of:
        - newline in UNIX format
        - each paragraph is separated by an empty line (two newlines)
        - resort to single newline if not paragraphs found

        Args:
          body(str): The body of a chapter
          title(str): The title of a chapter

        Returns:
          list: A list of paragraph of a chapter
        """
        # remove whitespaces (e.g.: newline) at the head/tail of string
        body = body.strip("\n")
        paragraphs = body.split("\n\n")
        if len(paragraphs) == 1:
            logger.debug("one paragraph found for chapter: {}", title)
            paragraphs = body.split("\n")

        # remove empty string from parsed paragraphs
        return list(filter(None, paragraphs))
