from argparse import ArgumentParser, Namespace
from datetime import date
from tuixdate.clients.tuix import TuixClient

from tuixdate.common import SubCommand
from tuixdate.logger import info
from tuixdate.utils import get_tuix_cli


@SubCommand("send")
class Send:
    def __init__(self, send_parser: ArgumentParser):
        send_parser.add_argument(
            "project",
            type=str,
            help='Set project name, "all" for send timesheet of all projects',
        )

    def send_timesheet(self, cli: TuixClient, project_name, project_id):
        timesheets = cli.get_timesheets(
            project_id, status="OPEN", date=date.today()
        )
        if len(timesheets) != 1:
            print("Timesheet not found")
            return
        timesheet = timesheets[0]
        timesheet_id = timesheet["id"]
        date_from = timesheet["from"]
        date_to = timesheet["to"]
        question = "Are you sure to send timesheet for "
        answer = input(
            f'{question}"{project_name}" from {date_from} to {date_to} [Y/n]: '
        )
        if str(answer).upper() in ["Y", "YES"]:
            resp = cli.send_timesheet(timesheet_id)
            if "status" in resp and str(resp["status"]).upper() == "SENT":
                print(f"✅ {project_name}")

    def process(self, args: Namespace):
        info("process push command")
        cli = get_tuix_cli()
        cli.login()
        project_name = args.project
        if project_name == "all":
            projects = cli.list_projects()
            for project in projects:
                project_name = project["name"]
                project_id = project["id"]
                self.send_timesheet(cli, project_name, project_id)
        else:
            project_id, project_name = cli.get_project_by_name(project_name)
            if project_name:
                self.send_timesheet(cli, project_name, project_id)
            else:
                print("Project not found! 😱")
