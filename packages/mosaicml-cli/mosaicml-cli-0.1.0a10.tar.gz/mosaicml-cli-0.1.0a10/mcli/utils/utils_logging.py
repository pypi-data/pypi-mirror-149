"""Utils for logging"""
import logging

from rich import print as rprint
from rich.console import Console
from rich.highlighter import NullHighlighter
from rich.logging import RichHandler
from rich.theme import Theme
from rich.tree import Tree

console = Console()
err_console = Console(stderr=True)

FAIL = '[red]✗[/] '
OK = '[green]✔[/] '
INFO = '[blue]i[/] '
QUESTION = '? '  # Placeholder for a colored question mark
WARN = '[red bold]![/] '


class TreeCompatibleHandler(RichHandler):
    """Logs messages using the ``RichHandler``, with support for ``rich.tree.Tree`` objects.

    NOTE: Currently only supports printing the Tree on stdout.
    TODO (TL): Add support for printing to stderr
    """

    def emit(self, record) -> None:
        if record.levelno >= self.level and isinstance(record.msg, Tree):
            rprint(record.msg)
        else:
            super().emit(record)


console_handler = TreeCompatibleHandler(show_time=False,
                                        show_level=False,
                                        show_path=False,
                                        console=Console(stderr=True, theme=Theme({'file': 'bold blue'})),
                                        highlighter=NullHighlighter())

console_handler.setFormatter(logging.Formatter(fmt='%(message)s'))
console_handler.markup = True


def log_tree(tree: Tree, level: str, logger: logging.Logger) -> None:

    mapping = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARN': logging.WARN,
        'ERROR': logging.ERROR,
    }
    try:
        level_val: int = mapping[level.upper()]
        if level_val >= logger.level:
            logger.log(level_val, '')
            rprint(tree)
            logger.log(level_val, '')
    except KeyError as key_error:
        raise ValueError(f'Invalid log level {level}. Should be one of {list(mapping.keys())}') from key_error
