from argparse import ArgumentParser, Namespace
from datetime import date

from tuixdate.common import SubCommand
from tuixdate.logger import info
from tuixdate.utils import check_date, check_value, get_tuix_cli


@SubCommand("push")
class Push:
    def __init__(self, push_parser: ArgumentParser) -> None:
        push_parser.add_argument("project", type=str, help="Set project name")
        push_parser.add_argument(
            "check_in",
            type=check_value,
            help="Set checkIn HH:MM PM|AM or 24HH:MM",
        )
        push_parser.add_argument(
            "check_out", type=check_value, help="Set checkOut HH:MM PM|AM"
        )
        push_parser.add_argument(
            "pause", type=int, help="Set pause 0..N minutes"
        )
        push_parser.add_argument("comments", type=str, help="Set comments")
        push_parser.add_argument(
            "date",
            type=check_date,
            nargs="?",
            default=date.today(),
            help="Date YYYY-MM-DD, default: current day",
        )

    def process(self, args: Namespace):
        info("process push command")
        tuix_cli = get_tuix_cli()
        tuix_cli.update_timesheets(
            args.project,
            args.date,
            args.check_in,
            args.check_out,
            args.pause,
            args.comments,
        )
