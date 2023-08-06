import requests
from requests import Response
import json
from datetime import date

from tuixdate.logger import info, warn


class TuixClient:
    def __init__(
        self, username: str, password: str, host="app.tuix.ch"
    ) -> None:
        self.username = username
        self.password = password
        self.host = f"https://{host}"
        self.token = None
        self.user_id = None

    def request(
        self, method: str, path: str, payload=None, withAuth=True
    ) -> Response:
        url = f"{self.host}{path}"
        headers = {"Content-Type": "application/json"}
        if withAuth:
            headers["x-juaapp-jwt"] = self.token
        return requests.request(method, url, headers=headers, data=payload)

    def get(self, path: str, withAuth=True) -> dict:
        response = self.request("GET", path, withAuth=withAuth)
        info(f"respone code {response.status_code}")
        if not response.ok:
            info(response.text)
        return json.loads(response.text)

    def patch(self, path: str, payload) -> dict:
        response = self.request("PATCH", path, payload, True)
        info(f"response {response.text}")
        return json.loads(response.text)

    def login(self) -> dict:
        """
        Login into tuix

        """
        payload = json.dumps(
            {
                "email": self.username,
                "password": self.password,
            }
        )
        response = self.request(
            "POST", "/api/auth/v1.0.0/login", payload, withAuth=False
        )

        if response.ok:
            self.token = response.headers["x-juaapp-jwt"]
            resp = json.loads(response.text)
            self.user_id = resp["id"]
            return resp
        else:
            raise Exception(f"Login failed, {response.status_code}")

    def list_projects(self) -> list:
        info("get projects")
        return self.get("/api/freelancer/v1.0.0/projects")["items"]

    def get_project_by_name(self, name) -> tuple:
        resp = self.list_projects()
        for item in resp:
            if item["name"] == name:
                return item["id"], item["name"]
        return None, None

    def get_timesheets(self, project_id, status=None, date=None) -> list:
        info("get timesheets")
        timesheets = []
        resp = self.get(
            f"/api/freelancer/v1.0.0/timesheets?project={project_id}"
        )
        for item in resp["items"]:
            info(str(item))
            if status and item["status"] != status:
                continue
            if date and item["from"] != date.strftime("%Y-%m-01"):
                continue
            if item["user"] and item["user"]["id"] != self.user_id:
                continue
            timesheets.append(
                {
                    "id": item["id"],
                    "from": item["from"],
                    "to": item["to"],
                    "status": item["status"],
                    "user": item["user"],
                }
            )
        info(str(timesheets))
        return timesheets

    def get_timesheets_entries(self, timesheet_id, date=None):
        info("get timesheet entries")
        entries = []
        resp = self.get(
            f"/api/freelancer/v1.0.0/timesheets/{timesheet_id}/entries"
        )
        for item in resp["items"]:
            if date and item["date"] != date.strftime("%Y-%m-%d"):
                continue
            entries.append(
                {
                    "id": item["id"],
                    "date": item["date"],
                    "checkIn": item["checkIn"],
                    "checkOut": item["checkOut"],
                    "pause": item["pause"],
                    "hours": item["hours"],
                    "comments": item["comments"],
                }
            )
        info(str(entries))
        return entries

    def list_timesheets(self, project_name, date=None) -> list:
        project_id, name = self.get_project_by_name(project_name)
        if project_id:
            return self.get_timesheets(project_id, "OPEN", date)
        else:
            print(f"Not project ({project_name}) fount")

    def list_timesheets_entries(
        self, project_name, _date, listAll=False
    ) -> list:
        project_id, name = self.get_project_by_name(project_name)
        if project_id:
            timesheets = self.get_timesheets(
                project_id, None, date.today() if not _date else _date
            )
            if len(timesheets) == 1:
                timesheet_id = timesheets[0]["id"]
                return self.get_timesheets_entries(
                    timesheet_id, None if listAll else _date
                )
        else:
            print(f"Not project ({project_name}) fount")

    def update_timesheets(
        self,
        project_name: str,
        date,
        checkIn=None,
        checkOut=None,
        pause: int = 0,
        comments: str = None,
    ):
        project_id, name = self.get_project_by_name(project_name)
        if project_id:
            timesheets = self.get_timesheets(project_id, "OPEN", date)
            if len(timesheets) != 1:
                warn("Not timesheets found!")
                return  # TODO: catch error
            timesheet_id = timesheets[0]["id"]
            entries = self.get_timesheets_entries(timesheet_id, date)
            if len(entries) != 1:
                warn("Not entries found!")
                return  # TODO: catch error
            entry_id = entries[0]["id"]
            path_data = {
                "checkIn": checkIn.strftime("%H:%M") if checkIn else None,
                "checkOut": checkOut.strftime("%H:%M") if checkIn else None,
                "pause": pause,
                "comments": comments if comments else "",
            }
            if not checkIn and not checkOut:
                path_data["hours"] = 0
            payload = json.dumps(path_data)
            info(f"payload {payload}")
            path = (
                "/api/freelancer/v1.0.0/timesheets"
                + f"/{timesheet_id}/entries/{entry_id}"
            )
            return self.patch(
                path,
                payload,
            )
        else:
            print(f"Not project ({project_name}) fount")

    def send_timesheet(self, timesheet_id: str):
        path = f"/api/freelancer/v1.0.0/timesheets/{timesheet_id}/send"
        return self.patch(path, None)
