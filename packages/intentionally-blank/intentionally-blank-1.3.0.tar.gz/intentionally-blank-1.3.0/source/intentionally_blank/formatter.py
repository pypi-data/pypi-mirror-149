
import sys
import textwrap
from abc import abstractmethod

from intentionally_blank.extension import ExtensionError, create_extension, Extension, list_extensions
from intentionally_blank.text import strip_lines

INTENTIONALLY_BLANK_FORMATTER = "intentionally_blank.formatter"

DEFAULT_TAB_SIZE = 4


class Formatter(Extension):

    def __init__(self, name, tab_size=None):
        super().__init__(name)
        self._tab_size = tab_size or DEFAULT_TAB_SIZE
        
    @property
    def tab_size(self):
        return self._tab_size

    @abstractmethod
    def format(self, lines):
        """Format a collection of lines.
        
        Args:
            lines: An iterable series of strings, each with a newline terminator.
        
        Yields:
            An iterable series of strings, each with a newline terminator.
        """
        raise NotImplementedError

    def describe(self):
        return strip_lines(textwrap.dedent(type(self).__doc__))

    def _package_name(self):
        """The name of the slide master package.
        """
        module = sys.modules[self.__module__]
        package_name = module.__package__
        return package_name


class FormatterExtensionError(ExtensionError):
    pass


def create_formatter(formatter_name, tab_size=None):
        driver = create_extension(
            kind="formatter",
            namespace=INTENTIONALLY_BLANK_FORMATTER,
            name=formatter_name,
            exception_type=FormatterExtensionError,
            tab_size=tab_size,
        )
        return driver


def formatter_names():
    return list_extensions(INTENTIONALLY_BLANK_FORMATTER)


