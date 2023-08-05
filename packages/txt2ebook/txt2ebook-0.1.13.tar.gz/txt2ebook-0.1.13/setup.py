# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['txt2ebook',
 'txt2ebook.formats',
 'txt2ebook.helpers',
 'txt2ebook.models',
 'txt2ebook.parsers']

package_data = \
{'': ['*'], 'txt2ebook.formats': ['templates/epub/*']}

install_requires = \
['CJKwrap>=2.2,<3.0',
 'EbookLib>=0.17.1,<0.18.0',
 'bs4>=0.0.1,<0.0.2',
 'cchardet>=2.1.7,<3.0.0',
 'click>=8.0.3,<9.0.0',
 'dotmap>=1.3.26,<2.0.0',
 'langdetect>=1.0.9,<2.0.0',
 'loguru>=0.5.3,<0.6.0',
 'regex>=2021.11.10,<2022.0.0']

entry_points = \
{'console_scripts': ['tte = txt2ebook.txt2ebook:main',
                     'txt2ebook = txt2ebook.txt2ebook:main']}

setup_kwargs = {
    'name': 'txt2ebook',
    'version': '0.1.13',
    'description': 'Console tool to convert txt file to different ebook format',
    'long_description': '# txt2ebook\n\nConsole tool to convert txt file to different ebook format.\n\n## Installation\n\nStable version From PyPI:\n\n```bash\npython3 -m pip install txt2ebook\n```\n\nLatest development version from GitHub:\n\n```bash\npython3 -m pip install -e git+https://github.com/kianmeng/txt2ebook.git\n```\n\n## Usage\n\nShowing help message of command-line options:\n\n```bash\ntxt2ebook --help\n```\n\n```bash\nUsage: tte [OPTIONS] INPUT_FILE [OUTPUT_FILE]\n\n  Console tool to convert txt file to different ebook format.\n\nOptions:\n  -f, --format TEXT               Set the export format ebook.  [default:\n                                  epub]\n  -t, --title TEXT                Set the title of the ebook.\n  -l, --language TEXT             Set the language of the ebook.\n  -a, --author TEXT               Set the author of the ebook.\n  -c, --cover PATH                Set the cover of the ebook.\n  -w, --width INTEGER             Set the width for line wrapping.\n  -d, --debug                     Enable debugging log.\n  -tp, --test-parsing             Test parsing only for volume/chapter header.\n                                  [default: False]\n  -nb, --no-backup                Do not backup source txt file.  [default:\n                                  False]\n  -nw, --no-wrapping              Remove word wrapping.  [default: False]\n  -et, --epub-template TEXT       CSS template for EPUB.  [default: clean]\n  -dr, --delete-regex TEXT        Regex to delete word or phrase.\n  -rr, --replace-regex TEXT...    Regex to replace word or phrase.\n  -dlr, --delete-line-regex TEXT  Regex to delete whole line.\n  --version                       Show the version and exit.\n  --help                          Show this message and exit.\n```\n\nConvert a txt file into epub:\n\n```bash\ntxt2book ebook.txt\n```\n\n## Copyright and License\n\nCopyright (c) 2021,2022 Kian-Meng Ang\n\nThis program is free software: you can redistribute it and/or modify\nit under the terms of the GNU Affero General Public License as\npublished by the Free Software Foundation, either version 3 of the\nLicense, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU Affero General Public License for more details.\n\nYou should have received a copy of the GNU Affero General Public License\nalong with this program.  If not, see <https://www.gnu.org/licenses/>.\n',
    'author': 'Kian-Meng Ang',
    'author_email': 'kianmeng@cpan.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kianmeng/txt2ebook',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
