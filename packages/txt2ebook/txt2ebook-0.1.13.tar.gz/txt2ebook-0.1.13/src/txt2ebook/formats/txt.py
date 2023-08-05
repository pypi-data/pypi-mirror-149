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

import os
from datetime import datetime as dt
from pathlib import Path

from loguru import logger

from txt2ebook.models import Book


class TxtWriter:
    """
    Module for writing ebook in txt format.
    """

    def __init__(self, book: Book, opts: dict) -> None:
        self.book = book
        self.filename = opts["input_file"]
        self.no_backup = opts["no_backup"]

    def write(self) -> None:
        """
        Optionally backup and overwrite the txt file.
        """
        if not self.no_backup:
            self._backup_file()

        self._overwrite_file()

    def _backup_file(self) -> None:
        txt_filename = Path(self.filename)

        ymd_hms = dt.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = Path(
            txt_filename.resolve().parent.joinpath(
                txt_filename.stem + "_" + ymd_hms + ".bak.txt"
            )
        )
        os.rename(txt_filename, backup_filename)
        logger.info("Backup txt file: {}", backup_filename)

    def _overwrite_file(self) -> None:
        txt_filename = Path(self.filename)

        with open(txt_filename, "w", encoding="utf8") as file:
            file.write(self.book.massaged_content)
            logger.info("Overwrite txt file: {}", txt_filename.resolve())
