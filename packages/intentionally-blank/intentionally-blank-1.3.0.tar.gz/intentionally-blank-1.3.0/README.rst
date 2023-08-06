Intentionally Blank
===================

Canonicalise the leading indentation of blank lines in text files.

.. image:: https://github.com/sixty-north/intentionally-blank/workflows/CI/badge.svg?branch=master
     :target: https://github.com/sixty-north/intentionally-blank/actions?workflow=CI
     :alt: CI Status

Installation
------------

The ``intentionally-blank`` package is available on the Python Package Index (PyPI):

.. image:: https://badge.fury.io/py/intentionally-blank.svg
    :target: https://badge.fury.io/py/intentionally-blank

The package supports Python 3 only. To install::

  $ python -m pip install intentionally-blank

Synopsis
--------

For the purposes of this tool, a "blank line" is a line containing only whitespace characters.

*Intentionally Blank* can apply one or more formatters to a text file for the purposes of modifying
the arrangement or representation of whitespace.

To get command-line help, use the ``--help`` option::

  $ intentionally-blank --help
  Usage: intentionally-blank [OPTIONS] COMMAND [ARGS]...

  Options:
    --verbosity [CRITICAL|ERROR|WARNING|INFO|DEBUG|NOTSET]
                                    The logging level to use.
    --version                       Show the version and exit.
    --help                          Show this message and exit.

  Commands:
    describe-format
    format
    list-formats


To list the available formatters, used the ``list-formats`` command::

  $ intentionally-blank list-formats
  empty
  identity
  leading
  visible

To describe the action of particular formatter, use the ``describe-format`` command::

  $ intentionally-blank describe-format --format=leading
  Blank lines have leading whitespace equal to that on the previous non-blank line.

To actually reformat a text file, we can use the ``format`` command. To get help on a particular
command, like ``format``, use the command and the ``--help`` option::

  $ intentionally-blank format --help
  Usage: intentionally-blank format [OPTIONS] INPUT OUTPUT

  Options:
    --format [empty|identity|leading|visible]
    --help                          Show this message and exit.


Now, use the ``format`` command to adjust whitespace::

  $ intentionally-blank format --format=leading infile.txt outfile.txt


To have blank lines be completely empty save for the terminating newline sequence, use
``--format=empty``::

  $ intentionally-blank format --format=empty infile.txt outfile.txt

Multiple ``--format`` options can be provided, and they will be applied in the order given. Here we
apply the "leading" format, and then the "visible" format which makes whitespace characters
visible::

  $ intentionally-blank format --format=leading --format=visible infile.txt outfile.txt

Either the INPUT or OUTPUT positional arguments can be replaced with a hyphen ``-`` to cause input
to be read from stdin or output to be written to stdout::

  $ intentionally-blank format --format=leading --format=visible infile.txt -
  """Model␣for␣aircraft␣flights."""↵
  ↵
  ↵
  class␣Flight:↵
  ␣␣␣␣"""A␣flight␣with␣a␣particular␣passenger␣aircraft."""↵
  ␣␣␣␣↵
  ␣␣␣␣def␣__init__(self,␣number,␣aircraft):↵
  ␣␣␣␣␣␣␣␣if␣not␣number[:2].isalpha():↵
  ␣␣␣␣␣␣␣␣␣␣␣␣raise␣ValueError(f"No␣airline␣code␣in␣'{number}'")↵
  ␣␣␣␣␣␣␣␣␣␣␣␣↵
