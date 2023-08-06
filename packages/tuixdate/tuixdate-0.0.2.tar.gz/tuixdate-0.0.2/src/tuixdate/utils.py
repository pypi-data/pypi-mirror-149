from os import mkdir
from pathlib import Path
from tabulate import tabulate
import re
import argparse
from datetime import datetime
import json

from tuixdate.globals import CONFIG_FILE
from tuixdate.clients.tuix import TuixClient
from tuixdate.logger import info


def check_value(value):
    match = re.match(
        "((?P<hour>[0-9]{1,2}):(?P<minutes>[0-9]{2})( (?P<daytime>[PA]M))?)",
        value,
    )
    if match:
        if match.group("daytime"):
            return datetime.strptime(value, "%I:%M %p")
        else:
            return datetime.strptime(value, "%H:%M")
    raise argparse.ArgumentTypeError(
        "must be in the form HH:MM PM|AM or 24HH:MM"
    )


def check_date(value):
    if re.match(
        "(?P<year>[0-9]{4})-(?P<month>[0-9]{1,2})-(?P<day>[0-9]{1,2})", value
    ):
        return datetime.strptime(value, "%Y-%m-%d")
    raise argparse.ArgumentTypeError("must be in the form YYYY-mm-dd")


def check_date_month(value):
    if re.match(
        "(?P<year>[0-9]{4})-(?P<month>[0-9]{1,2})-(?P<day>[0-9]{1,2})", value
    ):
        return datetime.strptime(value, "%Y-%m-%d")
    elif re.match("(?P<year>[0-9]{4})-(?P<month>[0-9]{1,2})", value):
        return value
    raise argparse.ArgumentTypeError(
        "must be in the form YYYY-mm-dd or YYYY-mm"
    )


def get_config():
    config = {}
    try:
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
    except FileNotFoundError:
        print("🚨 execute: tuixdate login <your_username>")
    return config


def get_tuix_cli():
    try:
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
    except FileNotFoundError:
        print("🚨 execute: tuixdate login <your_username>")
        exit(1)
    except KeyError as e:
        print("Value not found in config file, " + str(e))
        exit(1)
    info(f"Connect to {config['host']}")
    tuix_cli = TuixClient(
        config["username"], config["password"], config["host"]
    )
    tuix_cli.login()
    info("tuix client create success")
    return tuix_cli


def mkdir_config_folder():
    config_folder = Path(CONFIG_FILE).parent
    if not config_folder.exists():
        mkdir(config_folder)


class Printer:
    def print_timesheet(timeshift: list, fields: list, headers: list = []):
        if not headers:
            headers = fields
        table = []
        for item in timeshift:
            row = []
            for field in fields:
                row.append(item[field])
            table.append(row)
        print(tabulate(table, headers=[header.upper() for header in fields]))
