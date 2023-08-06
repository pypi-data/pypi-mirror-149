from argparse import ArgumentParser, Namespace
import re
from datetime import datetime

from tuixdate.common import SubCommand
from tuixdate.logger import info
from tuixdate.utils import Printer, get_tuix_cli, check_date_month


@SubCommand("timesheet")
class Timesheet:
    def __init__(self, timesheet_parser: ArgumentParser) -> None:
        timesheet_parser.add_argument(
            "project", type=str, help="Set project name"
        )
        timesheet_parser.add_argument(
            "date",
            type=check_date_month,
            nargs="?",
            default=None,
            help="Date YYYY-MM-DD, default: current day",
        )

    def process(self, args: Namespace) -> bool:
        info("process timesheet command")
        tuix_cli = get_tuix_cli()
        listAll = False
        date = args.date
        if re.match("^(?P<year>[0-9]{4})-(?P<month>[0-9]{1,2})$", str(date)):
            listAll = True
            date = datetime.strptime(date + "-01", "%Y-%m-%d")

        timesheet_entries = tuix_cli.list_timesheets_entries(
            args.project, date, listAll
        )
        Printer.print_timesheet(
            timesheet_entries,
            ["date", "checkIn", "checkOut", "pause", "hours", "comments"],
        )
