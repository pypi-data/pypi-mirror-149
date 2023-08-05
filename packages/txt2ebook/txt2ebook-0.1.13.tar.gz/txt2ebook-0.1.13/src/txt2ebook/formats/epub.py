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

import pkgutil
import uuid
from pathlib import Path
from typing import Optional

from ebooklib import epub
from loguru import logger

from txt2ebook.models import Book, Chapter, Volume

SPACE = "\u0020"


class EpubWriter:
    """
    Module for writing ebook in epub format.
    """

    def __init__(self, book: Book, config: dict) -> None:
        self.book = book
        self.config = config
        self.content = book.parsed_content

    def __getattr__(self, key):
        if key in self.config.keys():
            return self.config[key]

        raise AttributeError(key)

    def write(self) -> None:
        """
        Optionally backup and overwrite the txt file.
        """
        book = epub.EpubBook()

        if self.book.title:
            book.set_title(self.book.title)
            book.set_identifier(self._gen_id())

        if self.book.language:
            book.set_language(self.book.language)

        if self.book.authors:
            book.add_author(", ".join(self.book.authors))

        if self.book.cover:
            with open(self.book.cover, "rb") as image:
                book.set_cover("cover.jpg", image.read(), False)

                cover_page = self._build_cover()
                book.add_item(cover_page)
                book.toc.append(cover_page)
                book.spine.append(cover_page)

        self._build_nav(book)

        if self.book.volumes:
            logger.debug("Generate {} EPUB volumes", len(self.book.volumes))

            for volume in self.book.volumes:
                html_volume = self._build_volume(volume)
                book.add_item(html_volume)
                book.spine.append(html_volume)

                html_chapters = []
                for chapter in volume.chapters:
                    html_chapter = self._build_chapter(chapter, volume)
                    book.add_item(html_chapter)
                    book.spine.append(html_chapter)
                    html_chapters.append(html_chapter)

                if self.volume_page:
                    logger.debug("create separate volume page: {}", volume)
                    book.toc.append((html_volume, html_chapters))
                else:
                    book.toc.append((epub.Section(volume.title), html_chapters))
        else:
            logger.debug("Generate {} EPUB chapters", len(self.book.chapters))

            for chapter in self.book.chapters:
                html_chapter = self._build_chapter(chapter)
                book.add_item(html_chapter)
                book.spine.append(html_chapter)
                book.toc.append(html_chapter)

        output_filename = self._gen_output_filename()
        output_filename.parent.mkdir(parents=True, exist_ok=True)
        epub.write_epub(output_filename, book, {})
        logger.info("Generate EPUB file: {}", output_filename)

    def _build_nav(self, book: epub.EpubBook) -> None:
        book.add_item(epub.EpubNcx())

        try:
            logger.info("EPUB CSS template: {}", self.epub_template)
            css_file = Path("templates", "epub", self.epub_template + ".css")
            css = pkgutil.get_data(__package__, str(css_file))

            book_css = epub.EpubItem(
                uid="style_nav",
                file_name="style/book.css",
                media_type="text/css",
                content=css,
            )
            book.add_item(book_css)

            nav = epub.EpubNav()
            nav.add_link(
                href="style/book.css", rel="stylesheet", type="text/css"
            )
            book.add_item(nav)
            book.spine.append("nav")

        except FileNotFoundError as error:
            logger.error("Unknown EPUB template name: {}", self.epub_template)
            raise SystemExit() from error

    def _gen_id(self) -> str:
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, self.book.title))

    def _gen_output_filename(self) -> Path:
        """
        Determine the output EPUB filename.
        """
        return Path(
            self.output_file
            or Path(self.book.title or self.input_file).stem + ".epub"
        )

    def _build_cover(self) -> epub.EpubHtml:
        html = """
            <div id="cover"">
                <img src="cover.jpg" alt="cover" />
            </div>
        """
        cover = epub.EpubHtml(
            title=self.book.structure_names["cover"],
            file_name="cover.xhtml",
            lang=self.book.language,
            content=html,
        )
        cover.add_link(href="style/book.css", rel="stylesheet", type="text/css")
        return cover

    def _build_volume(self, volume: Volume) -> epub.EpubHtml:
        """
        Generates the whole volume to HTML.
        """
        filename = volume.title
        filename = filename.replace(SPACE, "_")

        header = volume.title
        title = volume.title.split(" ")
        if len(title) == 2:
            header = f"{title[0]}<br />{title[1]}"

        html = "<div class='volume'>"
        html = html + f"<h1 class='volume'>{header}</h1>"
        html = html + "</div>"

        epub_html = epub.EpubHtml(
            title=volume.title,
            file_name=filename + ".xhtml",
            lang=self.book.language,
            content=html,
        )
        epub_html.add_link(
            href="style/book.css", rel="stylesheet", type="text/css"
        )

        return epub_html

    def _build_chapter(
        self, chapter: Chapter, volume: Optional[Volume] = None
    ) -> epub.EpubHtml:
        """
        Generates the whole chapter to HTML.
        """
        if volume:
            filename = f"{volume.title}_{chapter.title}"
        else:
            filename = chapter.title

        filename = filename.replace(SPACE, "_")

        html = f"<h2>{chapter.title}</h2>"
        for paragraph in chapter.paragraphs:
            paragraph = paragraph.replace("\n", "")
            html = html + f"<p>{paragraph}</p>"

        epub_html = epub.EpubHtml(
            title=chapter.title,
            file_name=filename + ".xhtml",
            lang=self.book.language,
            content=html,
        )
        epub_html.add_link(
            href="style/book.css", rel="stylesheet", type="text/css"
        )

        return epub_html
