import argparse
import logging

from tuixdate.logger import info

subcommans = {}


class SubCommand:
    def __init__(self, *args, **kwargs) -> None:
        self.name = None
        if args and isinstance(args[0], str):
            self.name = args[0]

    def __call__(self, cls):
        subcommans[self.name] = cls


def process_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v",
        "--verbose",
        help="Be verbose",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
    )

    subparser = parser.add_subparsers(help="Commands", dest="command")
    sub_cmd_objs = []

    for name, cls in subcommans.items():
        arg_parser = subparser.add_parser(name)
        sub_cmd_objs.append((name, cls(arg_parser)))

    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)

    for sub_cmd in sub_cmd_objs:
        sub_cmd_name = sub_cmd[0]
        sub_cmd_obj = sub_cmd[1]
        if args.command == sub_cmd_name and hasattr(sub_cmd_obj, "process"):
            sub_cmd_obj.process(args)
            exit(0)

    info("Command unknown")
