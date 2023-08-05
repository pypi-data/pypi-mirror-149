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
Common shared functions.
"""

import sys

from loguru import logger

__version__ = "0.1.13"


def setup_logger(config):
    """
    Configure the global logger.

    Args:
        config(DotMap): Config that contains arguments
    """
    logger.remove()
    logger.add(
        sys.stderr,
        format="<green>{level: >5}</green>: {message}",
        level=config.test_parsing and "DEBUG" or config.debug or "INFO",
        colorize=True,
    )
