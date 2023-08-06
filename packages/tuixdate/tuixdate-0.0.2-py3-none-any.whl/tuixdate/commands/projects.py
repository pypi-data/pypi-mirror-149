from argparse import ArgumentParser, Namespace
from tabulate import tabulate

from tuixdate.common import SubCommand
from tuixdate.logger import info
from tuixdate.utils import get_tuix_cli


@SubCommand("projects")
class Projects:
    def __init__(self, projects_parser: ArgumentParser) -> None:
        pass

    def process(self, args: Namespace) -> bool:
        info("process projects command")
        tuix_cli = get_tuix_cli()
        projects = tuix_cli.list_projects()
        table = []
        for project in projects:
            info(f"project: {project}")
            table.append([project["name"]])
        print(tabulate(table, headers=["Name"]))
