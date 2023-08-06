import http.client
import json
from datetime import datetime, timedelta
from urllib.parse import quote
import re

from tuixdate.logger import exception, info


class TrelloClient:
    def __init__(self, username, apiKey, token, boardName):
        try:
            self.username = username
            self.apiKey = apiKey
            self.token = token
            self.boardName = boardName
            self.headers = {
                "Cookie": "dsc=68346d752217aca9979ae0ba828bb742f9a5ee9e4ab9d73eb3d01b7410cb8194; preAuthProps=s%3A61f05e692995cd122e1815d9%3AisEnterpriseAdmin%3Dfalse.tS%2Bl%2FwL%2BubdUbx%2B65u8ZbPfZEY6cvpx%2FfzWy2Wer1Pc"  # noqa: E501
            }
            self.conn = http.client.HTTPSConnection("api.trello.com")
            info(f"create trello client for {self.username}")
        except Exception as e:
            exception(e)

    def get_board(self):
        payload = ""
        headers = self.headers
        headers["Accept"] = "application/json"
        url = (
            f"/1/members/{self.username}/boards"
            + f"?key={self.apiKey}&token={self.token}"
        )
        self.conn.request("GET", url, payload, headers)
        res = self.conn.getresponse()
        data = res.read()
        boards = json.loads(data.decode("utf-8"))
        info(f"get boards : {len(boards)}")
        for board in boards:
            name = board["name"]
            info(f"board name: {name}")
            if name == self.boardName:
                return board
        return None

    def get_actions(self, date: datetime):
        info(f"get actions on {date}")
        board_id = self.get_board()["id"]
        info(f"board id: {board_id}")
        before_date = date + timedelta(days=1)
        since = quote(date.strftime("%b %d %Y EDT"))
        before = quote(before_date.strftime("%b %d %Y EDT"))
        payload = ""
        self.conn.request(
            "GET",
            f"/1/boards/{board_id}/actions"
            + "?filter=commentCard"
            + f"&key={self.apiKey}"
            + f"&token={self.token}"
            + f"&limit=1000&since={since}&before={before}",
            payload,
            self.headers,
        )
        res = self.conn.getresponse()
        data = res.read()
        actions = json.loads(data.decode("utf-8"))
        info(f"get actions {len(actions)}")
        cards_update_ids = []
        for action in actions:
            card_id = action["data"]["card"]["id"]
            card_name = action["data"]["card"]["name"]
            # update = datetime.strptime(
            #     action["date"], "%Y-%m-%dT%H:%M:%S.%f%z"
            # )
            # comment = action["data"]["text"]
            # info(f"action comment: {comment}")
            # print(card_id, update, action['memberCreator']['username'])
            if action["memberCreator"]["username"] == self.username:
                info(f"get owner action in card {card_name}")
                cards_update_ids.append(card_id)
        cards_update_ids = list(dict.fromkeys(cards_update_ids))
        info(f"card IDs {cards_update_ids}")
        branches = []
        for card_id in cards_update_ids:
            card = self.get_card(card_id)
            if card["branch"]:
                branches.append(card["branch"])
        info(f"branches {branches}")
        print('"' + " ".join(branches) + '"')

    def get_card(self, card_id):
        info(f"get card id {card_id}")
        payload = ""
        headers = self.headers
        headers["Accept"] = "application/json"
        self.conn.request(
            "GET",
            f"/1/cards/{card_id}?key={self.apiKey}&token={self.token}",
            payload,
            headers,
        )
        res = self.conn.getresponse()
        data = res.read()
        card = json.loads(data.decode("utf-8"))
        desc = card["desc"]
        info(f"card desc {desc}")
        branch = None
        branch_regex = r".*\*\*branch[\*\*]*:[\*\*]*\s*(?P<branch>[\w\_-]+).*"
        matches = re.search(branch_regex, desc)
        if matches:
            branch = matches["branch"]
        return {"desc": desc, "branch": branch}
