from intentionally_blank.formatter import Formatter


class NewlineAtEofFormatter(Formatter):
    """Ensure the last line of the file has a newline terminator.
    """

    def format(self, lines):
        """
        Args:
            lines: An iterable series of strings, each with a newline terminator.
        
        Yields:
            An iterable series of strings, each with a newline terminator.
        """
        return map(ensure_newline_terminator, lines)
    

def ensure_newline_terminator(line):
    if line.endswith("\n"):
        return line
    return f"{line}\n"
