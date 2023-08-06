import os
from builtins import input
from datetime import datetime, timedelta
from getpass import getpass
from os.path import expanduser
from subprocess import call
from typing import Generator, Optional, Union
from urllib.parse import quote_plus

import numpy as np
import requests
import simplejson as json

from swdl.camera import Camera
from swdl.club import Club
from swdl.labels import Events, EventsMapStaigeAPI, Label, TimesMapStaigeAPI
from swdl.matches import Match

from . import settings
from .tools import AuthSerivceBase, make_request


def get_credential_file():
    return os.environ.get("SWDL_CREDENTIALS", expanduser("~/.swdlrc"))


def save_password():
    """
    Asks for username and password and stores the credentials in the credential file
    """
    user_file = get_credential_file()
    print(f"Password will be saved as plaintext in {user_file} !")
    username = input("Username: ")
    password = getpass("Password: ")
    user_config = {}
    if os.path.exists(user_file):
        user_config = json.loads(open(user_file).read())
    user_config.update({"username": username, "password": password})
    open(user_file, "w").write(json.dumps(user_config))
    call("chmod 600 {}".format(user_file).split())


class AuthService(AuthSerivceBase):
    def __init__(self, username, password, api_key=settings.API_KEY):
        base_url = "https://identitytoolkit.googleapis.com/v1/"
        self.sign_in_url = f"{base_url}accounts:signInWithPassword?key={api_key}"
        self.token_url = f"{base_url}token?key={api_key}"
        self.id_token = None
        self.refresh_token = None
        self.token_expires = None
        self.username = username
        self.password = password
        self._sign_in()
        self.refresh_before_seconds = 300

    def _sign_in(self):
        body = {
            "email": self.username,
            "password": self.password,
            "returnSecureToken": True,
        }
        ret = make_request(self.sign_in_url, body)
        self.id_token = ret["idToken"]
        self.refresh_token = ret["refreshToken"]
        self.token_expires = datetime.now() + timedelta(seconds=int(ret["expiresIn"]))

    def _refresh_token(self):
        body = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
        }
        ret = make_request(self.token_url, body)
        self.id_token = ret["id_token"]
        self.refresh_token = ret["refresh_token"]
        self.token_expires = datetime.now() + timedelta(seconds=int(ret["expires_in"]))

    @property
    def auth(self):
        if (
            self.token_expires is None
            or self.refresh_token is None
            or self.token_expires < datetime.now()
        ):
            self._sign_in()
        elif self.token_expires < (
            datetime.now() + timedelta(seconds=self.refresh_before_seconds)
        ):
            self._refresh_token()

        class BearerAuth(requests.auth.AuthBase):
            def __init__(self, token):
                self.token = token

            def __call__(self, r):
                r.headers["authorization"] = "Bearer " + self.token
                return r

        return BearerAuth(self.id_token)


class DataService:
    """
    Helper service to download soccerwatch data

    # Attributes
    username (str): Name of the user to connect to the service
    password (str): Password required to login.
    """

    def __init__(self, username=None, password=None):
        if not username:
            user_file = get_credential_file()
            if os.path.exists(user_file):
                user_config = json.loads(open(user_file).read())
                username = user_config["username"]
                password = user_config["password"]
        self.auth_service = AuthService(username, password)
        self.auth = self.auth_service.auth
        self.url_extension = "/intern/rest/v1/streamInterface"
        self.user_escaped = username

        self.apis = self._get_apis()

    @staticmethod
    def _get_apis() -> dict:
        for i in range(5):
            ret = ""
            try:
                ret = requests.get(settings.DISCOVERY_URL)
                return ret.json()
            except json.JSONDecodeError as e:
                print("Got invalid json")
                print(e.msg)
                print("Json:", ret)
                raise e

    def fetch(self, url, body=None) -> Optional[dict]:
        """
        Performs a get request on the given URL.

        # Arguments
        url (str): URL to perform get request

        # Retrurns
        str: Dictionary created from JSON dump of the response

        # Example
        ```python
        ds = DataService()
        ds.get("www.google.de")
        ```
        """
        next_token = ""
        while True:
            response = make_request(
                url + next_token,
                body,
                authorization=self.auth_service,
            )

            yield response
            if "nextToken" in response:
                next_token = "/" + quote_plus(response["nextToken"])
            else:
                return

    def get_matches(
        self, max_results: int = -1, date: datetime = None
    ) -> Generator[Match, None, None]:
        """
        Lists all matches

        # Args:
            max_results: Maximum number of matches to return

        # Returns:
            list: All matches in type #Match`
        """
        url = "{}/metas/".format(self.apis["API_VIDEO"])
        if date:
            time_string = date.strftime("%Y-%m-%d")
            url = f"{self.apis['API_VIDEO']}/metasExport/{time_string}/"
        counter = 0
        for matches in self.fetch(url):
            if "data" not in matches or not matches["data"]:
                return
            else:
                for match in matches["data"]:
                    counter += 1
                    yield Match.from_json(**match).set_data_service(self)
                    if counter == max_results:
                        return

    def get_match(self, match_id):
        """
        Returns a single #Match for a given match id

        # Arguments
        match_id (int,str): Match id

        #Returns
        Match: The requested match
        """
        url = "{}/meta/{}".format(self.apis["API_VIDEO"], match_id)
        response = list(self.fetch(url))
        if not response:
            return Match(match_id)
        ret = response[0]

        return Match.from_json(**ret).set_data_service(self)

    def get_events(self, match_id):
        """
        Returns all Events from azure

        # Arguments
        match_id (str,int): Matchid

        # Returns
        list: Events as got as dictionaries
        """
        url = "{}/Tag/{}".format(self.apis["API_TAG"], match_id)
        result = list(self.fetch(url))
        if not result:
            return []
        return result[0]["data"]

    def add_event(self, match_id, event_id, timestamp):
        """
        Add a new event zo azure

        # Arguments
        match_id (str,int): Matchid
        event_id (int): Type of the event
        timestamp (int): Time in secends when the event occurs
        """
        url = "{}/AiTag".format(self.apis["API_TAG"])
        body = {"matchId": str(match_id), "eventType": event_id, "timestamp": timestamp}
        call = self.fetch(url, body)
        list(call)

    def upload_player_positions(self, timestamp, match):
        try:
            match_id = match.match_id
            players = match.labels.player_positions[timestamp]
            data = {}
            data["playerPositions"] = []
            for i in range(players.shape[0]):
                if players[i][0] == -1:
                    continue
                data["playerPositions"].append({})
                data["playerPositions"][i]["playerId"] = int(players[i][0])
                data["playerPositions"][i]["teamId"] = int(players[i][1])
                data["playerPositions"][i]["positionX"] = float(players[i][2] / 1000.0)
                data["playerPositions"][i]["positionY"] = float(players[i][3] / 1000.0)
                data["playerPositions"][i]["certainty"] = float(players[i][4] / 1000.0)

            url = "{}/playerPositions/{}/{}".format(
                self.apis["API_ANALYTICS"], match_id, timestamp
            )
            call = self.fetch(url, data)
            list(call)

        except KeyError:
            # ToDo do something
            pass

    def get_positions(self, match_id, time=None, virtual_camera_id="-1"):
        """
        Get the camera positions of a match

        # Arguments
        match_id (str,int): Match id
        time (datetime): Datetime to limit the data given back. Will only
        return data later than time
        virtual_camera_id (str): The camera id of the positions
        source (str): Should be human or machine

        # Returns
        list: Dictionaries of the positions

        # Example
        """
        if not time:
            last_modified = 0
        elif type(time) == int:
            last_modified = time
        elif type(time) == datetime:
            last_modified = int(time.strftime("%s")) * 1000
        else:
            raise TypeError

        virtual_camera_id = str(virtual_camera_id)

        url = "{}/CameraPosition/{}".format(self.apis["API_ANALYTIC"], match_id)
        body = {"virtualCameraId": virtual_camera_id, "lastModified": last_modified}

        call = self.fetch(url, body=body)
        for bulk in call:
            if "data" in bulk:
                for pos in bulk["data"]:
                    yield pos

    def pull_info(self, match):
        """
        Updates the information about a match

        # Arguments
        match (Match): A match

        # Returns
        Match: Updated match

        # Raises
        ValueError: If input is not a match
        """
        if not isinstance(match, Match):
            raise ValueError("Argument must be a valid match")
        return self.get_match(match.match_id)

    def push_labels(
        self,
        match,
        start_index=0,
        virtual_camera_id="-1",
        source="human",
        label_object: Label = None,
    ):
        """
        Uploads the positions greater than the given #start_index to the cloud
        service

        # Arguments
        match (str): The match
        start_index (int): only positions greater than start index will be
        pushed
        virtual_camera_id (str): Camera id the positions belongs to
        source (str): Should be "human" or "machine"
        """
        if label_object is None:
            label_object = match.labels

        message_body = self._create_label_body(
            match.match_id,
            label_object.positions,
            start_index,
            virtual_camera_id,
            source,
        )
        url = "{}/addCameraPositionBulk".format(self.apis["API_ANALYTIC"])
        call = self.fetch(url, message_body)
        next(call)

    @staticmethod
    def _create_label_body(
        match_id, position_list, start_index=0, virtual_camera_id="-1", source="human"
    ):

        # ToDo push events and status
        message_body = dict()
        message_body["virtualCameraId"] = str(virtual_camera_id)
        message_body["matchId"] = str(match_id)
        message_body["source"] = str(source)
        message_body["positions"] = list()
        for i in range(start_index, len(position_list)):
            timestamp = int(position_list[i, 0])
            if timestamp == 0:
                continue
            message_body["positions"].append(dict())
            message_body["positions"][-1]["timestamp"] = timestamp
            message_body["positions"][-1]["x"] = str(position_list[i, 1])
            message_body["positions"][-1]["y"] = str(position_list[i, 2])
            message_body["positions"][-1]["zoom"] = str(position_list[i, 3])
        return message_body

    def pull_events(self, match: Match):
        match_id = match.match_id

        label = match.labels
        label.events = np.zeros((0, 3), dtype=np.float32)
        label.status = np.zeros((11,), dtype=np.uint32)
        events = self.get_events(match_id)
        for i, e in enumerate(events):
            e_mapped = self.map_events_from_staige_api(e, match.video_type)
            if e_mapped[0] < 0:
                continue
            if len(e_mapped) == 2:
                label.status[e_mapped[1]] = e_mapped[0]
            else:
                label.events = np.append(label.events, [e_mapped], axis=0).astype(
                    np.uint32
                )
        match.labels = label
        return match

    def get_camera(self, camera_id: Union[str, int]) -> Optional[Camera]:
        url = self.apis["API_CAMERA"] + "/info/single/{}".format(camera_id)
        data = list(self.fetch(url))[0]
        if not data:
            return None

        return Camera.from_json(self, **data)

    def get_club(self, club_id: Union[str, int]) -> Optional[Club]:
        url = self.apis["API_CLUB"] + "/info/{}".format(club_id)
        data = list(self.fetch(url))[0]
        if not data:
            return None

        return Club.from_json(self, **data)

    def set_camera_stitching_status(self, camera_id: str, status: str):
        body = {"uid": str(camera_id), "stitching": str(status)}
        url = self.apis["API_CAMERA"] + "/manage"
        next(self.fetch(url, body))

    def update_match(self, match: Match, data: dict):
        url = self.apis["API_VIDEO"] + "/meta/" + match.match_id
        next(self.fetch(url, body=data))

    def update_camera(self, camera: Camera, data: dict):
        url = self.apis["API_CAMERA"] + "/manage"
        data["uid"] = str(camera.id)
        next(self.fetch(url, body=data))

    @staticmethod
    def map_events_from_staige_api(event, sport_type="soccer"):
        """
        Maps a event dictionary to a list

        # Arguments
        event (dict): Event dictionary

        # Returns
        list: With either 2 or 3 entries
        """

        try:
            e = int(event["eventType"])
            timestamp = int(event["timestamp"])
        except KeyError:
            return [-1, Events.UNDEFINED, 0]

        if e in EventsMapStaigeAPI:
            return [timestamp, *EventsMapStaigeAPI[e]]
        if sport_type not in TimesMapStaigeAPI:
            sport_type = "soccer"
        time_map = TimesMapStaigeAPI[sport_type]
        # For status
        if e in time_map:
            return [timestamp * 1000, time_map[e]]
        return [timestamp, Events.UNDEFINED, 0]
