import argparse
import sys
from typing import Collection, Iterable, Optional, Sequence, Type, Union

from .argparse import ArgumentParser, Formatter
from .command import BaseCommand, Group
from .features import Feature, FeatureHub, LoggingFeature, VerbosityFeature


class CliApp:
    """Entrypoint for a CLI application. This is the central instance that manages dispatch."""

    def __init__(
        self,
        name: str,
        version: Optional[str] = None,
        description: Optional[str] = None,
        root: Optional[BaseCommand] = None,
        features: Iterable[Union[Feature, Type[Feature]]] = (VerbosityFeature, LoggingFeature),
    ) -> None:

        root = root or Group()
        root._app = self
        root._name = name

        self.name = name
        self.version = version
        self.description = description
        self.root = root
        self.features = FeatureHub(features)

    def add_command(self, name: str, command: BaseCommand) -> None:
        if not isinstance(self.root, Group):
            raise RuntimeError(
                f"CliApp.root must be a Group in order to add subcommands, got {type(self.root).__name__}"
            )
        self.root.add_command(name, command)

    def new_argument_parser(self, prog: str, subcommands: Collection[BaseCommand]) -> argparse.ArgumentParser:
        return ArgumentParser(prog=prog, formatter_class=lambda prog: Formatter(prog, subcommands))

    def dispatch(
        self,
        command: BaseCommand,
        argv: Sequence[str],
        parser: Optional[argparse.ArgumentParser] = None,
        features: Optional[FeatureHub] = None,
    ) -> int:

        parser = parser or self.new_argument_parser(command.get_full_name(), command.get_subcommands())

        if features:
            features.init_parser(parser)
        command.init_parser(parser)

        args = parser.parse_args(argv)

        if features:
            features.before_execute(command, args)
        try:
            response = command.execute(args)
        finally:
            if features:
                features.after_execute(command, args)

        if response is not None and not isinstance(response, int):
            raise TypeError(
                f"Return value of {type(command).__name__}.execute() is {type(response).__name__}, expected int|None"
            )

        return 0 if response is None else response

    def run(self, argv: Optional[Sequence[str]] = None) -> int:
        return self.dispatch(self.root, sys.argv[1:] if argv is None else argv, None, self.features)
