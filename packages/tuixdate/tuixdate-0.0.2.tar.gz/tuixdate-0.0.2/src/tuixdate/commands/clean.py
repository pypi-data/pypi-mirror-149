from argparse import ArgumentParser, Namespace
from datetime import date
from tabulate import tabulate

from tuixdate.common import SubCommand
from tuixdate.logger import info
from tuixdate.utils import get_tuix_cli, check_date


@SubCommand("clean")
class Clean:
    def __init__(self, clean_parser: ArgumentParser) -> None:
        clean_parser.add_argument("project", type=str, help="Set project name")
        clean_parser.add_argument(
            "date",
            type=check_date,
            nargs="?",
            default=date.today(),
            help="Date YYYY-MM-DD, default: current day",
        )

    def process(self, args: Namespace) -> bool:
        info("process clean command")
        tuix_cli = get_tuix_cli()
        entry = tuix_cli.update_timesheets(args.project, args.date)
        table = []
        table.append(
            [
                entry["date"],
                entry["checkIn"],
                entry["checkOut"],
                entry["pause"],
                entry["hours"],
                entry["comments"],
            ]
        )
        print(
            tabulate(
                table,
                headers=[
                    "Date",
                    "checkIn",
                    "checkOut",
                    "pause",
                    "Hours",
                    "comments",
                ],
            )
        )
