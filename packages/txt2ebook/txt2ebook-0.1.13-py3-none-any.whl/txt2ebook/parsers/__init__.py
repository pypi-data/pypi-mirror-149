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

from langdetect import detect
from loguru import logger

from txt2ebook.helpers import load_class, to_classname
from txt2ebook.parsers.en import EnParser
from txt2ebook.parsers.zhcn import ZhCnParser
from txt2ebook.parsers.zhtw import ZhTwParser


def create_parser(content: str, config: dict) -> Any:
    """
    Factory function to create parser by language.
    """
    config.language = detect_language(content, config.language)
    class_name = to_classname(config.language, "Parser")
    klass = load_class("txt2ebook.parsers", class_name)
    parser = klass(content, config)
    return parser


def detect_language(content: str, default: str) -> str:
    """
    Detect the language (ISO 639-1) of the content of the txt file.
    """
    language = default or detect(content)
    logger.info("Detect language: {}", language)
    return language


__all__ = [
    "EnParser",
    "ZhCnParser",
    "ZhTwParser",
]
