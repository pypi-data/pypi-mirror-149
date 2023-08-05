# pylint: disable=no-value-for-parameter
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

"""
Main program of txt2ebook.
"""

from pathlib import Path
from typing import Dict

import click
from bs4 import UnicodeDammit
from dotmap import DotMap
from loguru import logger

from txt2ebook import __version__, setup_logger
from txt2ebook.formats import create_format
from txt2ebook.parsers import create_parser


@click.command(no_args_is_help=True)
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path(), required=False)
@click.option(
    "--format",
    "-f",
    default="epub",
    show_default=True,
    type=click.Choice(["epub", "txt"]),
    help="Set the export format ebook.",
)
@click.option(
    "--title",
    "-t",
    default=None,
    show_default=True,
    help="Set the title of the ebook.",
)
@click.option(
    "--language",
    "-l",
    default=None,
    help="Set the language of the ebook.",
)
@click.option(
    "--author",
    "-a",
    default=None,
    multiple=True,
    help="Set the author of the ebook.",
)
@click.option(
    "--cover",
    "-c",
    type=click.Path(exists=True),
    default=None,
    help="Set the cover of the ebook.",
)
@click.option(
    "--width",
    "-w",
    type=click.INT,
    show_default=True,
    help="Set the width for line wrapping.",
)
@click.option(
    "--debug",
    "-d",
    is_flag=True,
    flag_value="DEBUG",
    show_default=True,
    help="Enable debugging log.",
)
@click.option(
    "--volume-page",
    "-vp",
    is_flag=True,
    show_default=True,
    help="Show the volume as separate page.",
)
@click.option(
    "--test-parsing",
    "-tp",
    is_flag=True,
    show_default=True,
    help="Test parsing only for volume/chapter header.",
)
@click.option(
    "--no-backup",
    "-nb",
    is_flag=True,
    flag_value=True,
    show_default=True,
    help="Do not backup source txt file.",
)
@click.option(
    "--no-wrapping",
    "-nw",
    is_flag=True,
    show_default=True,
    help="Remove word wrapping.",
)
@click.option(
    "--epub-template",
    "-et",
    default="clean",
    show_default=True,
    help="CSS template for EPUB.",
)
@click.option(
    "--re-delete",
    "-rd",
    multiple=True,
    help="Regex to delete word or phrase.",
)
@click.option(
    "--re-replace",
    "-rr",
    nargs=2,
    multiple=True,
    help="Regex to replace word or phrase.",
)
@click.option(
    "--re-delete-line",
    "-rl",
    multiple=True,
    help="Regex to delete whole line.",
)
@click.option(
    "--re-volume",
    "-rv",
    multiple=True,
    help="Regex to parse volume header.",
)
@click.option(
    "--re-chapter",
    "-rc",
    multiple=True,
    help="Regex to parse chapter header.",
)
@click.option(
    "--re-author",
    "-ra",
    multiple=True,
    help="Regex to parse author of the book.",
)
@click.option(
    "--re-title",
    "-rt",
    multiple=True,
    help="Regex to parse title of the book.",
)
@click.version_option(prog_name="txt2ebook", version=__version__)
def main(**kwargs: Dict) -> None:
    """
    Console tool to convert txt file to different ebook format.
    """
    config = DotMap(**kwargs)
    setup_logger(config)

    try:
        filename = Path(config.input_file)
        logger.info("Parsing txt file: {}", filename.resolve())

        with open(filename, "rb") as file:
            unicode = UnicodeDammit(file.read())
            logger.info("Detect encoding : {}", unicode.original_encoding)
            content = unicode.unicode_markup

            if not content:
                raise RuntimeError(f"Empty file content in {filename}")

            parser = create_parser(content, config)
            book = parser.parse()

            if config.test_parsing or config.debug:
                logger.debug(repr(book))

                for volume in book.volumes:
                    logger.debug(repr(volume))
                    for chapter in volume.chapters:
                        logger.debug(repr(chapter))

                for chapter in book.chapters:
                    logger.debug(repr(chapter))

            if not config.test_parsing:
                if book.parsed_content:
                    writer = create_format(book, config)
                    writer.write()

                # We write to txt for debugging purpose if output format is not
                # txt.
                if config.format != "txt":
                    config.format = "txt"
                    txt_writer = create_format(book, config)
                    txt_writer.write()

    except RuntimeError as error:
        logger.error(str(error))


if __name__ == "__main__":
    main()  # pragma: no cover
    raise SystemExit()  # pragma: no cover
