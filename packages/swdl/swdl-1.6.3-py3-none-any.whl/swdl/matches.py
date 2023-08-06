import logging as log
import os
import re
import subprocess
import urllib
from datetime import datetime

import m3u8
from google.cloud import storage

from .labels import CPDownloader, CPUploader, Label


class FFMPegRunner(object):
    """
    Usage:
        runner = FFMpegRunner()
        def status_handler(old, new):
            print "From {0} to {1}".format(old, new)
        runner.run('ffmpeg -i ...', status_handler=status_handler)
    """

    def run(self, command, status_handler=None):
        pipe = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )

        duration = None
        position = None

        while True:
            line = pipe.stdout.readline().strip()

            if line == "" and pipe.poll() is not None:
                print("I am here")
                break

            if duration is None:
                duration = self.find_duration(line)

            if duration:
                new_pos = self.find_position(line)
                if new_pos:
                    if new_pos != position:
                        position = new_pos
                        if callable(status_handler):
                            status_handler(position, duration)

    @staticmethod
    def find_duration(line):
        re_duration = re.compile(
            r".*Duration: (\d{2}):(\d{2}):(\d{2}).(\d{2})[^\d]*", re.U
        )
        duration_match = re_duration.match(line)
        if duration_match:
            return FFMPegRunner.time2sec(duration_match)

    @staticmethod
    def find_position(line):
        re_position = re.compile(
            r".*time=(\d{2}):(\d{2}):(\d{2})\.(\d{2})\d*", re.U | re.I
        )
        position_match = re_position.match(line)
        if position_match:
            return FFMPegRunner.time2sec(position_match)

    @staticmethod
    def time2sec(search):
        secs = sum([int(search.group(i + 1)) * 60 ** (2 - i) for i in range(3)])

        return secs


class SWLoginError(Exception):
    pass


class NoEndlistError(Exception):
    pass


class NoPlaylistError(Exception):
    pass


class Match:
    """
    Class to store match information

    # Attributes
    matchId(str,int): Match id
    swcsId(str,int): The camera id
    name(str): The name of the match. Mostly "TeamA-TeamB"
    location(str): The location where the match took place
    userStreamLink(str): A download link for the user stream
    gridStreamLink(str):A download link for the grid stream
    state(str): Status of the stream. Can be created, live or done
    # Members
    labels(Label): #Label object that stores the labels
    """

    def __init__(
        self,
        match_id,
        camera_id="",
        location="",
        state="",
        club_a_name="",
        club_b_name="",
        club_a_id="",
        club_b_id="",
        date=None,
        active=False,
        hardware_platform="",
        video_type="",
        virtual_camera=0,
        user_stream_link="",
        grid_stream_link="",
        camera_bitrate=10000,
        league="",
        priority="",
        did="",
        canceled_reason="",
        stream_owner="",
        flags={},
    ):
        self.match_id = match_id
        self.camera_id = camera_id
        self.location = location
        self.state = state
        self.user_stream_link = user_stream_link
        if not self.user_stream_link:
            self.user_stream_link = (
                "https://storage.googleapis.com"
                "/sw-sc-de-shared/{0}/720p/{0}.m3u8".format(match_id)
            )
        self.grid_stream_link = grid_stream_link
        if not self.grid_stream_link:
            self.grid_stream_link = (
                "https://storage.googleapis.com"
                "/sw-sc-de-shared/{0}/Grid/{0}.m3u8".format(match_id)
            )
        self.team_name_home = club_a_name
        self.team_name_away = club_b_name
        self.team_id_home = club_a_id
        self.team_id_away = club_b_id
        self.date = date
        self.labels = Label()
        self.data_service = None
        self.last_label_update = None
        self.active = active
        self.hardware_platform = hardware_platform
        self.video_type = video_type
        self.virtual_camera = virtual_camera
        self.camera_bitrate = camera_bitrate
        self.stream_owner = stream_owner

        self.league = league
        self.priority = priority
        self.did = did
        self.canceled_reason = canceled_reason
        self.flags = flags

    @classmethod
    def from_json(
        cls,
        RowKey,
        swcsID="",
        field="",
        state="",
        clubAName="",
        clubBName="",
        clubAId="",
        clubBId="",
        expectedStartTime="0",
        active=False,
        hardwarePlatform="",
        videoType="",
        uselabels=0,
        userStream="",
        gridStream="",
        cameraBitrate=10000,
        league="",
        priority="",
        did="",
        canceledReason="",
        streamOwner="",
        *args,
        **kwargs,
    ):
        match_id = str(RowKey)
        camera_id = str(swcsID)
        try:
            date = datetime.fromtimestamp(float(expectedStartTime) / 1000)
        except (ValueError, TypeError):
            log.warning(
                "{}: Could not convert expected start time {} to float".format(
                    match_id, expectedStartTime
                )
            )
            date = datetime.fromtimestamp(0)
        flags = {k: v for k, v in kwargs.items() if k.startswith("flag")}
        return Match(
            match_id,
            camera_id,
            field,
            state,
            clubAName,
            clubBName,
            clubAId,
            clubBId,
            date,
            active,
            hardwarePlatform,
            videoType,
            uselabels,
            userStream,
            gridStream,
            cameraBitrate,
            league,
            priority,
            did,
            canceledReason,
            streamOwner,
            flags,
        )

    def copy_info(self, match):
        """
        Copys the info from another match

        # Arguments
        match(Match):
        """
        self.match_id = match.match_id
        self.camera_id = match.camera_id
        self.location = match.location
        self.state = match.state
        self.user_stream_link = match.user_stream_link
        self.grid_stream_link = match.grid_stream_link

    def download_user_stream(self, download_directory="."):
        """
        Downloads the user stream from the match. Needs ffmpeg

        # Attributes
        download_directory(str):

        # Raises
        NoPlaylistError: If video file is not existing
        NoEndlistError: If stream has not endlist tag. This means the stream is
        not correctly finished and can note be downlaoded with ffmpeg
        """
        self._download_match(download_directory, "User")

    def download_grid_stream(self, download_directory="."):
        """
        Downloads the grid stream from the match. Needs ffmpeg

        # Attributes
        download_directory:

        # Raises
        NoPlaylistError: If video file is not existing
        NoEndlistError: If stream has not endlist tag. This means the stream is
        not correctly finished and can note be downlaoded with ffmpeg
        """
        self._download_match(download_directory, "Grid")

    def pull_info(self):
        """
        Updates match info

        # Raises
        SWLoginError
        """
        if not self.data_service:
            raise SWLoginError("Not logged into Soccerwatch Data Service")
        m = self.data_service.pull_info(self)
        self.copy_info(m)

    def pull_labels(self, virtual_camera_id="-1"):
        """
        Updates match labels.
        Warning: May override all locally stored labels

        #Arguments
        time_from (datetime,int): Will only get labels later than this time,
        Must be msecs after 1970 or datetime
        virtual_camera_id (str): Camera Id
        with_events(bool): Defines if events should be pulled as well

        # Raises
        SWLoginError: If data service was not connected
        """
        if not self.data_service:
            raise SWLoginError("Not logged into Soccerwatch Data Service")
        positions = self.create_position_downloader(virtual_camera_id).download_all()
        self.labels.positions = positions

    def pull_events(self):
        """
        Updates match events.
        Warning: May override all locally stored labels

        # Raises
        SWLoginError: If data service was not connected
        """
        if not self.data_service:
            raise SWLoginError("Not logged into Soccerwatch Data Service")
        m = self.data_service.pull_events(self)
        self.labels = m.labels

    def push_labels(
        self,
        start_index=0,
        virtual_camera_id="-1",
        source="human",
        labbel_object: Label = None,
    ):
        """
        Uploads the labels to the cloud

        # Arguments
        start_index (int): Only positions greater than start index will be
        pushed
        virtual_camera_id (str): Camera id the positions belongs to
        source (str): Should be "human" or "machine"

        # Raises
        SWLoginError: If data service was not connected
        """
        if not self.data_service:
            raise SWLoginError("Not logged into Soccerwatch Data Service")
        self.data_service.push_labels(
            self, start_index, virtual_camera_id, source, labbel_object
        )

    def set_data_service(self, data_service):
        """
        Sets the #DataService for this match

        # Arguments
        data_service(DataService):
        """
        self.data_service = data_service
        return self

    def grid_stream_available(self):
        """
        Checks if a user stream is available

        # Returns
        bool: if available
        """
        return self._check_stream("Grid")

    def user_stream_available(self):
        """
        Checks if a user stream is available

        # Returns
        bool: if available
        """
        return self._check_stream("User")

    def user_stream_has_endlist(self):
        """
        Checks if user stream has an an endlist tag, which means that the
        stream has been completely uploaded

        # Returns

        bool: True if endlist is exsisting
        """
        return self._check_endlist("User")

    def grid_stream_has_endlist(self):
        """
        Checks if grid stream has an an endlist tag, which means that the
        stream has been completely uploaded

        # Returns

        bool: True if endlist is exsisting
        """
        return self._check_endlist("Grid")

    def _check_stream(self, streamType="User"):
        if streamType == "User":
            download_link = self.user_stream_link
        else:
            download_link = self.grid_stream_link
        try:
            playlist = m3u8.load(download_link)
            if not playlist.segments:
                return False

        except urllib.error.HTTPError:
            return False
        return True

    def _check_endlist(self, streamType="User"):
        if streamType == "User":
            download_link = self.user_stream_link
        else:
            download_link = self.grid_stream_link
        try:
            playlist = m3u8.load(download_link)
            if not playlist.is_endlist:
                return False
        except urllib.error.HTTPError:
            return False
        return True

    def _download_match(self, download_directory=".", streamType="User"):
        if streamType == "User":
            download_link = self.user_stream_link
        else:
            download_link = self.grid_stream_link
        # Check m3u8
        try:
            playlist = m3u8.load(download_link)
            if not playlist.is_endlist:
                raise NoEndlistError(
                    "Video has no endlist, can not be downloaded with FFMPEG"
                )
        except urllib.error.HTTPError:
            raise NoPlaylistError("Playlist was not found")
        command = 'ffmpeg -i {} -c copy -y "{}/{}.mp4"'.format(
            download_link, download_directory, self.match_id
        )
        print(command)

        def run_callback(actual, total):
            percent = 100.0 * actual / total
            print("%.2f%%" % percent)

        ffmpeg = FFMPegRunner()
        ffmpeg.run(command, status_handler=run_callback)

    def add_player_position(self, timestamp, players):
        """
        Uploads the player positions to the cloud

        # Arguments
        timestamp (int): Current timestamp in seconds
        players (str): 2D integer tensor 25x5: playerId, teamId, x, y, confidence.
        If playerId is -1, player is not valid.
        x, y and confidence should be scaled between 0 and 1000

        # Raises
        SWLoginError: If data service was not connected
        """
        self.labels.player_positions[timestamp] = players
        if not self.data_service:
            raise SWLoginError

        self.data_service.upload_player_positions(timestamp, self)

    def fix_grid_endlist(self):
        playlist = m3u8.load(self.grid_stream_link)
        if not playlist.segments:
            log.warning("Cannot fix playlist. No segments found")
            return False
        playlist.is_endlist = True
        temp_file = "{}.m3u8".format(self.match_id)
        playlist.dump(temp_file)
        client = storage.Client()
        bucket = client.bucket("sw-sc-de-shared")
        blob = bucket.blob("{0}/Grid/{0}.m3u8".format(self.match_id))
        blob.content_type = "video/mp4"
        blob.cache_control = "no-cache,no-store,must-revalidate,max-age=0"
        blob.upload_from_filename(temp_file)
        blob.make_public()
        os.remove(temp_file)
        return True

    def create_upload_manager(
        self, virtual_camera_id, bucket_name: str, upload_batch=250
    ):
        return CPUploader(
            self.match_id,
            bucket_name,
            virtual_camera_id,
            self.data_service.auth_service,
            self.data_service.apis["API_CAMERA_POSITION"],
            upload_batch=upload_batch,
        )

    def create_position_downloader(self, virtual_camera_id):
        return CPDownloader(self.match_id, virtual_camera_id)

    def update(self, **kwargs):
        self.data_service.update_match(self, kwargs)

    def __str__(self):
        return str(self.__dict__)
