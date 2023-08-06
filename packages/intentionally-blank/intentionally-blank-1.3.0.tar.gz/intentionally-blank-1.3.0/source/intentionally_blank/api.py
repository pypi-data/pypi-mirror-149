import sys

import logging
from contextlib import contextmanager

from functools import reduce

from intentionally_blank.formatter import create_formatter, formatter_names
from intentionally_blank.les_iterables import ensure_contains

logger = logging.getLogger(__name__)


def format_from_path_to_path(*, in_filepath, out_filepath=None, format_names=(), tab_size=None, in_place=False):
    """Format the contents of in_filepath and place the results in out_filepath.

    Raises:
        ValueError: If the output filepath is not provided when not processing in-place.
    """

    if (not in_place) and (out_filepath is None):
        raise ValueError("Output filepath must be provided if not processing in-place.")

    if (in_filepath == out_filepath) and (in_filepath != "-") and (not in_place):
        raise ValueError("Input and output file paths are equivalent.")

    if in_place and (out_filepath is None):
        out_filepath = in_filepath

    formatters = [
        create_formatter(format_name, tab_size)
        for format_name in ensure_contains(format_names, "identity")
    ]

    logger.debug("formatters = %s", formatters)

    in_lines = _read_lines(in_filepath)

    with open_path(out_filepath, "wt") as out_file:
        format_from_lines_to_file(in_lines, out_file, formatters, tab_size=None)


def format_from_file_to_file(in_file, out_file, format_names, tab_size=None):
    in_lines = list(in_file)
    format_from_lines_to_file(in_lines, out_file, format_names, tab_size)


def format_from_lines_to_file(in_lines, out_file, format_names, tab_size=None):
    out_file.writelines(format_from_lines_to_lines(in_lines, format_names, tab_size))


def format_str_to_str(in_text, format_names, tab_size=None):
    in_lines = in_text.splitlines(keepends=True)
    out_lines = format_from_lines_to_lines(in_lines, format_names, tab_size)
    return ''.join(out_lines)


def format_from_lines_to_lines(in_lines, format_names, tab_size=None):
    formatters = [
        create_formatter(format_name, tab_size)
        for format_name in ensure_contains(format_names, "identity")
    ]
    logger.debug("formatters = %s", formatters)
    return transform_lines(formatters, in_lines)


def transform_lines(formatters, in_lines):
    return reduce(lambda lines, formatter: formatter.format(lines), formatters, in_lines)


@contextmanager
def open_path(path, mode, encoding=None, newline=None):
    if not (("w" in mode) ^ ("r" in mode)):
        raise ValueError("Either 'r' or 'w' must be in mode")

    if not (("b" in mode) ^ ("t" in mode)):
        raise ValueError("Either 'b' or 't' must be in mode")

    if path == "-":
        f = sys.stdin if ("r" in mode) else sys.stdout
        closeable = False
    else:
        f = open(path, mode=mode, encoding=encoding, newline=newline)
        closeable = True

    try:
        yield f
    finally:
        if closeable:
            f.close()


def _read_lines(in_filepath):
    with open_path(in_filepath, "rt") as in_file:
        return list(in_file)


def list_formats(file=None):
    return list(formatter_names)

def describe_formatter(format_name, file=None):
    file = file or sys.stdout
    formatter = create_formatter(format_name)
    return formatter.describe()

