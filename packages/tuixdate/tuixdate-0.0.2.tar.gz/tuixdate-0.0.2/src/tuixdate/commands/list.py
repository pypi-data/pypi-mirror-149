from argparse import ArgumentParser, Namespace
from datetime import date
from tabulate import tabulate

from tuixdate.common import SubCommand
from tuixdate.utils import check_date, get_tuix_cli
from tuixdate.logger import info


@SubCommand("list")
class List:
    def __init__(self, arg_parser: ArgumentParser) -> None:
        arg_parser.add_argument("project", type=str, help="Set project name")
        arg_parser.add_argument(
            "date",
            type=check_date,
            nargs="?",
            default=date.today(),
            help="Date YYYY-MM-DD, default: current day",
        )

    def process(self, args: Namespace):
        info("process list command")
        tuix_cli = get_tuix_cli()
        timesheets = tuix_cli.list_timesheets(args.project, args.date)
        table = []
        for timesheet in timesheets:
            table.append(
                [
                    timesheet["id"],
                    timesheet["from"],
                    timesheet["to"],
                    timesheet["status"],
                ]
            )
        info(f"timesheets: {timesheets}")
        print(tabulate(table, headers=["ID", "From", "To", "Status"]))
        if args.date:
            timesheet_entries = tuix_cli.list_timesheets_entries(
                args.project, args.date
            )
            table = []
            for entries in timesheet_entries:
                table.append(
                    [
                        entries["date"],
                        entries["checkIn"],
                        entries["checkOut"],
                        entries["pause"],
                        entries["comments"],
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
                        "comments",
                    ],
                )
            )
