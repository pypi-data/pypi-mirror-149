# slap.core.cli

Extension of [`argparse`][0] to provide fast and customizable argument parsing.

  [0]: https://docs.python.org/3/library/argparse.html

## Usage

```py
import argparse
from typing import Any, Optional

from slap.core.cli import CliApp, Command


class HelloCommand(Command):
    def init_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("name")

    def execute(self, args: Any) -> Optional[int]:
        print(f"Hello, {args.name}!")


app = CliApp("minimal", "0.1.0")
app.add_command("hello", HelloCommand())
app.run()
```

Gives you the following CLI:

```
$ python examples/minimal.py
usage: minimal [-h] [-v] [--version] [{hello}] ...

positional arguments:
  {hello}        The subcommand to execute.
  ...            Arguments for the subcommand.

options:
  -h, --help     show this help message and exit
  -v, --verbose  Increase the verbosity level.
  --version      show program's version number and exit

subcommands:
  hello
```

## Compatibility

Requires Python 3.6 or higher.
