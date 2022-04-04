from abc import abstractmethod
import argparse
from typing import Any, List, Optional


class BaseCliCommand:
    def __init__(self, name: str, description: Optional[str] = None) -> None:
        self.name = name
        self.description = description

    @abstractmethod
    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        raise NotImplementedError

    @abstractmethod
    def run(self, args: argparse.Namespace) -> None:
        raise NotImplementedError


class RootCliCommand:
    def __init__(self, description: str = "") -> None:
        self.parser = argparse.ArgumentParser(description=description)

    def subcommands(self, commands: List[BaseCliCommand]) -> "RootCliCommand":
        subparsers: Any = self.parser.add_subparsers()
        for command in commands:
            parser = subparsers.add_parser(
                name=command.name, description=command.description
            )
            command.add_arguments(parser)
            parser.set_defaults(run=command.run)
        return self

    def run(self) -> None:
        # Parse the args and run the command function
        args = self.parser.parse_args()
        if hasattr(args, "run"):
            args.run(args)
        else:
            self.parser.print_help()
