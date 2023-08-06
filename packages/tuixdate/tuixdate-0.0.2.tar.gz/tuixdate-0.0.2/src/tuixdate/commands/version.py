from argparse import ArgumentParser, Namespace

from tuixdate import __version__
from tuixdate.common import SubCommand
from tuixdate.logger import info


@SubCommand("version")
class Version:
    def __init__(self, _: ArgumentParser) -> None:
        pass

    def process(self, args: Namespace) -> bool:
        info("process version command")
        print(f"v{__version__}")
        exit(0)
