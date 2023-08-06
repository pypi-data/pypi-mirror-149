import abc
import argparse
import logging
from typing import Any, Dict, Iterable, Optional, Sequence, Type, TypeVar, Union, cast

from .command import BaseCommand

T_Feature = TypeVar("T_Feature", bound="Feature")


class FeatureHub:
    def __init__(self, features: Iterable[Union["Feature", Type["Feature"]]] = ()) -> None:
        self._features: Dict[Type[Feature], Feature] = {}
        for feature in features:
            self.add_feature(feature)

    def add_feature(self, feature: Union["Feature", Type["Feature"]]) -> None:
        if isinstance(feature, type):
            feature = feature()
        self._features[type(feature)] = feature

    def get_feature(self, feature_type: Type[T_Feature]) -> Optional[T_Feature]:
        return cast(Optional[T_Feature], self._features.get(feature_type))

    def require_feature(self, feature_type: Type[T_Feature]) -> T_Feature:
        return cast(T_Feature, self._features[feature_type])

    def init_parser(self, parser: argparse.ArgumentParser) -> None:
        for feature in self._features.values():
            feature.init_parser(parser)

    def before_execute(self, command: BaseCommand, args: Any) -> None:
        for feature in self._features.values():
            feature.before_execute(self, command, args)

    def after_execute(self, command: BaseCommand, args: Any) -> None:
        for feature in self._features.values():
            feature.after_execute(self, command, args)


class Feature(abc.ABC):
    @abc.abstractmethod
    def init_parser(self, parser: argparse.ArgumentParser) -> None:
        ...

    def before_execute(self, hub: FeatureHub, command: BaseCommand, args: Any) -> None:
        ...

    def after_execute(self, hub: FeatureHub, command: BaseCommand, args: Any) -> None:
        ...


class VerbosityFeature(Feature):

    DEFAULT_LEVELS = ["WARNING", "INFO", "DEBUG"]

    def __init__(self, long_name: str = "verbose", short_name: str = "v", dest: str = "verbosity") -> None:
        self.long_name = long_name
        self.short_name = short_name
        self.dest = dest
        self.level: int = 0

    def init_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            f"-{self.short_name}",
            f"--{self.long_name}",
            dest=self.dest,
            default=0,
            action="count",
            help="Increase the verbosity level.",
        )

    def before_execute(self, hub: FeatureHub, command: BaseCommand, args: Any) -> None:
        self.level = getattr(args, self.dest)


class LoggingFeature(Feature):

    DEFAULT_LEVELS = ["WARNING", "INFO", "DEBUG"]
    DEFAULT_FORMAT = "%(levelname)s | %(name)s | %(message)s"

    def __init__(self, format: str = DEFAULT_FORMAT, levels: Sequence[str] = DEFAULT_LEVELS) -> None:
        self.format = format
        self.levels = levels

    def init_parser(self, parser: argparse.ArgumentParser) -> None:
        pass

    def before_execute(self, hub: FeatureHub, command: BaseCommand, args: Any) -> None:
        verbosity = hub.require_feature(VerbosityFeature).level
        level = getattr(logging, self.levels[min(verbosity, len(self.levels))])
        logging.basicConfig(level=level, format=self.format)
