# txt2ebook

Console tool to convert txt file to different ebook format.

## Installation

Stable version From PyPI:

```bash
python3 -m pip install txt2ebook
```

Latest development version from GitHub:

```bash
python3 -m pip install -e git+https://github.com/kianmeng/txt2ebook.git
```

## Usage

Showing help message of command-line options:

```bash
txt2ebook --help
```

```bash
Usage: tte [OPTIONS] INPUT_FILE [OUTPUT_FILE]

  Console tool to convert txt file to different ebook format.

Options:
  -f, --format TEXT               Set the export format ebook.  [default:
                                  epub]
  -t, --title TEXT                Set the title of the ebook.
  -l, --language TEXT             Set the language of the ebook.
  -a, --author TEXT               Set the author of the ebook.
  -c, --cover PATH                Set the cover of the ebook.
  -w, --width INTEGER             Set the width for line wrapping.
  -d, --debug                     Enable debugging log.
  -tp, --test-parsing             Test parsing only for volume/chapter header.
                                  [default: False]
  -nb, --no-backup                Do not backup source txt file.  [default:
                                  False]
  -nw, --no-wrapping              Remove word wrapping.  [default: False]
  -et, --epub-template TEXT       CSS template for EPUB.  [default: clean]
  -dr, --delete-regex TEXT        Regex to delete word or phrase.
  -rr, --replace-regex TEXT...    Regex to replace word or phrase.
  -dlr, --delete-line-regex TEXT  Regex to delete whole line.
  --version                       Show the version and exit.
  --help                          Show this message and exit.
```

Convert a txt file into epub:

```bash
txt2book ebook.txt
```

## Copyright and License

Copyright (c) 2021,2022 Kian-Meng Ang

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
