import abc
import argparse
import textwrap
from typing import TYPE_CHECKING, Any, Collection, Dict, Optional

if TYPE_CHECKING:
    from .app import CliApp


class BaseCommand(abc.ABC):
    """Pure interface for CLI commands."""

    _app: Optional["CliApp"] = None
    _name: Optional[str] = None
    _parent: Optional["BaseCommand"] = None

    def __repr__(self) -> str:
        if self._name is not None:
            full_name = self.get_full_name()
        else:
            full_name = "<unnamed>"
        return f"{type(self).__name__}({full_name!r})"

    def get_app(self) -> "CliApp":
        if self._app:
            return self._app
        if self._parent:
            return self._parent.get_app()
        raise RuntimeError("BaseCommand._app is not set (did you add the command to an app?)")

    def get_name(self) -> str:
        assert self._name is not None, "BaseCommand._name is not set (did you add the command to a group?)"
        return self._name

    def get_full_name(self) -> str:
        if self._parent:
            return f"{self._parent.get_full_name()} {self._name}"
        return self.get_name()

    @abc.abstractmethod
    def get_description(self) -> str:
        ...

    @abc.abstractmethod
    def get_subcommands(self) -> Collection["BaseCommand"]:
        ...

    @abc.abstractmethod
    def init_parser(self, parser: argparse.ArgumentParser) -> None:
        ...

    @abc.abstractmethod
    def execute(self, args: Any) -> Optional[int]:
        ...


class Group(BaseCommand):
    def __init__(self, description: Optional[str] = None, help: Optional[str] = None) -> None:
        self._description = description
        self._help = help
        self._subcommands: Dict[str, BaseCommand] = {}

    def add_command(self, name: str, command: BaseCommand) -> None:
        command._name = name
        command._parent = self
        self._subcommands[name] = command

    def get_description(self) -> str:
        return self._description or get_first_line(self._help or "")

    def get_subcommands(self) -> Collection["BaseCommand"]:
        return self._subcommands.values()

    def init_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.description = self._help
        if self._subcommands:
            parser.add_argument("cmd", nargs='?', choices=self._subcommands.keys(), help="The subcommand to execute.")
            parser.add_argument("argv", metavar="...", nargs=argparse.REMAINDER, help="Arguments for the subcommand.")
        self._parser = parser

    def execute(self, args: Any) -> int:
        if self._subcommands and args.cmd:
            command = self._subcommands[args.cmd]
            return self.get_app().dispatch(command, args.argv, None)
        else:
            self._parser.print_help()
            return 0


class Command(BaseCommand):
    def get_description(self) -> str:
        return get_first_line(format_docstring(self.__doc__ or ""))

    def get_subcommands(self) -> Collection["BaseCommand"]:
        return ()

    def init_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.description = format_docstring(self.__doc__ or "")


def format_docstring(docstring: str) -> str:
    first_line, remainder = (docstring or "").partition("\n")[::2]
    return (first_line.strip() + "\n" + textwrap.dedent(remainder)).strip()


def get_first_line(text: str) -> str:
    lines = text.splitlines()
    return lines[0] if lines else ""
