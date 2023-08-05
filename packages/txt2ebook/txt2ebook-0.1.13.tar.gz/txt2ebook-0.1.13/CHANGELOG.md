# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## v0.1.13 - 2022-05-02
Added
- Generate documentation through Sphinx
- Add contribution guideline on how to contribute to this project
- Add `-vp/--volume-page` option to create separate page for volume title
- Add `-rv/--re-volume` option to parse multiple volume header by regex
- Add `-rc/--re-chapter` option to parse multiple volume header by regex
- Add `-ra/--re-author` option to parse and extract author by regex
- Add `-rt/--re-title` option to parse and extract title by regex

Changed
- Rename and standardize on regex option
- Rename `-dr/--delete-regex` to `-rd/re-delete`
- Rename `-rr/--replace-regex` to `-rr/re-replace`
- Rename `-dlr/--delete-line-regex` to `-rl/re-delete-line`
- Refactor detecting book title to base parsing class

Fixed
- Show longer and exact raw string when repr(Chapter)

## v0.1.12 - 2022-01-18
Added
- Add `tte` as the alternative shorter command name to `txt2ebook`
- Separate page for volume title in epub format
- Use Tox for automation and testing

Changed
- Refactor EPUB template loading
- Refactor base parser module to use dataclass
- Stricter rules on Chinese header parsing
- Support Python 3.7 onwards
- Use DotMap to manage config
- Add more fields to repr for Chapter model

Fixed
- Fix removing line by regex not working
- Fix section header not showing in toc in Foliate
- Fix cannot parse content with no empty line as paragraph separator
- Fix cannot generate ebook for English text file

## v0.1.11 - 2021-12-19
Added
- Add `--epub-template/-et` option to set CSS style for EPUB file
- Add `--test-parsing/-tp` option to show only parsed headers without
  generating ebook
- Build cover page when cover image `--cover` was set
- Add typing to the project
- Update more project classifiers

Changed
- Update default table of content style sheet
- Switch logging to loguru library and rephrase logging messages
- Wrap program's config with configuror library

Fixed
- Do not capture newline when parsing book title and author name
- Add missing language when generating HTML for each chapter
- Remove whitespace in chapter title in HTML
- Generate EPUB file in tmp dir when running test case

## v0.1.10 - 2021-11-22
Fixed
- Do not generate txt file twice when txt format was set
- Fix cannot parse txt file other than Unix line end
- Fix test default to unknown parser

Changed
- Refactor parser and writer factory into subpackage
- Support setting multiple authors
- Move common functions to helper subpackage
- Set unique identified for epub based on book's title

## v0.1.9 - 2021-10-26
Added
- Add `--format` option to specify output format

Fixed
- Fix missing deps in requirements.txt
- Fix issues raised by PyLint

Changed
- Refactor txt and epub file generation in separate module
- Refactor txt formatting and parsing in separate module
- Switch chapter header regex to constant

## v0.1.8 - 2021-10-04
Added
- Allow setting of optional argument for output path and file name
- Add `--width` option to set line width for paragraph wrapping

Changed
- Rename `--remove-wrapping` option to `-no-wrapping` to follow the convention
- Refactor and move string helper functions
- Refactor extracting title and author from txt file
- Replace magic number with constant
- Remove using Click's context object

Fixed
- Disable backup txt fixtures during test
- Fix warnings raised by Pylint

## v0.1.7 - 2021-09-19
Added
- Detect the original encoding of txt file, convert, and save to utf-8
- Add `--cover` option to add cover image to ebook

Changed
- Revise logging message format
- Do not raise exception when no chapter header found
- Show indentation for chapter title in debugging message
- Match different chapter headers and line separator
- Replace full-width space with half-width space in chapter headers
- Generate HTML manually instead through Markdown
- Keep original txt file formatting except chapter header
- Refactor and use more ways to extract book title from txt file
- Relax chapter header regex rules

Fixed
- Fix paragraph wrapping of imbalance opening and closing quote
- Fix group match not working with replacing regex

## v0.1.6 - 2021-09-11
Changed
- Backup original txt file and overwrite with parsed content
- Include and refactor more chapter header regex

Added
- Add `--no-backup` option to skip backup the original txt file

## v0.1.5 - 2021-09-02
Added
- Add `--delete-regex` option to remove selected words or phrases from the file
  content
- Add `--replace-regex` option to replace selected words or phrases from the
  file content
- Add `--delete-line-regex` option to remove whole line from the file content
- Detect author name from file content
- Parse volumes and chapters correctly and generate nested toc

Fixed
- Fix incorrect chapter filename
- Fix missing title in Epub file
- Fix issues raised by Flake8 and PyLint
- Replace missing space between chapter header and chapter title

Changed
- Parse more different chapter headers
- Save HTML filename in Epub as chapter header and title
- Dump parsed txt file during debug mode
- Use only single quotation punctuation

## v0.1.4 - 2021-08-04
Added
- Add `--remove_wrapping` option to remove text wrapping in the body content of
  a chapter
- Capture the book title from the file if found and not explicitly set through
  `--title` option

Fixed
- Fix no paragraph separation for txt file without single-line spacing for
  markdown
- Fix issues raised by PyLint

Changed
- Parse more different chapter headers
- Refactor argument parsing

## v0.1.3 - 2021-07-24
Fixed
- Fix no parsing and split by introduction chapter
- Fix issues raised by PyLint

Changed
- Switch license to AGPL-3

## v0.1.2 - 2021-07-20
Added
- Add option to set metadata for ebook
- Add missing requirements.txt
- Show full help message when missing required argument

Changed
- Use better way to check for input file
- Print message using click.ecto
- Code formatting

## v0.1.1 - 2021-07-13

Added
- Enable logging for debugging and showing status
- Set log level through `LOG` environment variable

Fixed
- Check for missing filename, empty file content, and missing chapters

## v0.1.0 - 2021-07-08

Added
- Initial public release
- Support converting txt file in Chinese language into epub format
