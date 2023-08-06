from argparse import ArgumentParser, Namespace
from datetime import date


from tuixdate.clients.trello_client import TrelloClient
from tuixdate.common import SubCommand
from tuixdate.logger import info
from tuixdate.globals import CONFIG_FILE
from tuixdate.utils import get_config, check_date


@SubCommand("trello")
class Trello:
    def __init__(self, trello_parser: ArgumentParser) -> None:
        trello_parser.add_argument(
            "date",
            type=check_date,
            nargs="?",
            default=date.today(),
            help="Date YYYY-MM-DD, default: current day",
        )

    def process(self, args: Namespace) -> bool:
        info("process trello command")
        config = get_config()
        if "trello_apiKey" not in config:
            print(f"Add Trello API Key in {CONFIG_FILE}")
            return
        if "trello_token" not in config:
            print(f"Add Trello Token Key in {CONFIG_FILE}")
            return
        if "trello_boardName" not in config:
            print(f"Add Trello API BoardName in {CONFIG_FILE}")
            return
        if "trello_username" not in config:
            print(f"Add Trello API username in {CONFIG_FILE}")
            return

        trello_cli = TrelloClient(
            config["trello_username"],
            config["trello_apiKey"],
            config["trello_token"],
            config["trello_boardName"],
        )
        trello_cli.get_actions(args.date)
