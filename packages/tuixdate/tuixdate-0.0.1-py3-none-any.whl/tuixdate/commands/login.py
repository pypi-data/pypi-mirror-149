from argparse import ArgumentParser, Namespace
from getpass import getpass
import json

from tuixdate.clients.tuix import TuixClient
from tuixdate.common import SubCommand
from tuixdate.globals import CONFIG_FILE
from tuixdate.logger import info
from tuixdate.utils import mkdir_config_folder


@SubCommand("login")
class Login:
    def __init__(self, login_parser: ArgumentParser) -> None:
        login_parser.add_argument(
            "username", nargs="?", type=str, help="Set Tuix username"
        )
        login_parser.add_argument(
            "host",
            nargs="?",
            type=str,
            default="app.tuix.ch",
            help="Tuix hostname",
        )
        login_parser.add_argument("-P", nargs="?", dest="password")

    def process(self, args: Namespace) -> bool:
        info("process login command")
        if not args.username:
            args.username = input("username: ")
        if not args.password:
            args.password = getpass()

        trello_username = input("Trello username: ")
        trello_apiKey = input("Trello apiKey: ")
        trello_token = input("Trello token: ")
        trello_boardName = input("Trello board: ")

        config = {
            "username": args.username,
            "password": args.password,
            "host": args.host,
            "trello_apiKey": trello_apiKey,
            "trello_token": trello_token,
            "trello_boardName": trello_boardName,
            "trello_username": trello_username,
        }

        try:
            cli = TuixClient(
                config["username"], config["password"], config["host"]
            )
            cli.login()
            mkdir_config_folder()
            with open(CONFIG_FILE, "w") as outfile:
                json.dump(config, outfile, indent=2)
            info(f"Create or overwrite file {CONFIG_FILE}")
            print("Login success")
        except Exception as e:
            print(e)
