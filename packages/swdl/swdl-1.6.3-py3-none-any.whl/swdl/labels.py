import asyncio
import json
import logging
import time
from base64 import b64decode, b64encode
from datetime import datetime
from enum import IntEnum
from multiprocessing import Process, Queue, Value
from typing import Iterable, Optional

import aiohttp
import h5py as h5
import numpy as np
import requests
from google.api_core.exceptions import NotFound, TooManyRequests
from google.cloud import storage

from .tools import AuthSerivceBase, make_request


class Team(IntEnum):
    HOME = 0
    AWAY = 1


class Events(IntEnum):
    GOAL = 0
    KICKOFF = 1
    CORNER = 2
    THROW_IN = 3
    PENALTY = 4
    FOUL = 5
    SCORE_CHANCE = 6
    UNDEFINED = 7
    WHISTLE = 8
    SEGMENT_START=50
    SEGMENT_END=51


class GameStatus(IntEnum):
    FIRST_START = 1
    FIRST_END = 2
    SECOND_START = 3
    SECOND_END = 4
    THIRD_START = 5
    THIRD_END = 6


# Map Staige event into SWML Event type with Home/Away Flag
EventsMapStaigeAPI = {
    0: (Events.GOAL, Team.HOME),
    1: (Events.GOAL, Team.AWAY),
    2: (Events.SCORE_CHANCE, Team.HOME),
    3: (Events.SCORE_CHANCE, Team.AWAY),
    4: (Events.FOUL, Team.HOME),
    5: (Events.FOUL, Team.AWAY),
    6: (Events.PENALTY, Team.HOME),
    7: (Events.PENALTY, Team.AWAY),
    35: (Events.CORNER, Team.HOME),
    36: (Events.CORNER, Team.AWAY),
    47: (Events.KICKOFF, Team.HOME),
    48: (Events.WHISTLE, Team.HOME),
    170: (Events.PENALTY, Team.HOME),
}

# Map Staige Time event into SWML game status
TimesMapStaigeAPI = {
    "soccer": {
        12: GameStatus.FIRST_START,
        13: GameStatus.FIRST_END,
        14: GameStatus.SECOND_START,
        15: GameStatus.SECOND_END,
    },
    "handball": {
        200: GameStatus.FIRST_START,
        201: GameStatus.FIRST_END,
        202: GameStatus.SECOND_START,
        203: GameStatus.SECOND_END,
    },

    "icehockey": {
        200: GameStatus.FIRST_START,
        201: GameStatus.FIRST_END,
        202: GameStatus.SECOND_START,
        203: GameStatus.SECOND_END,
        204: GameStatus.THIRD_START,
        205: GameStatus.THIRD_END,
    },
}


logger = logging.getLogger(__name__)

CP_FRAMERATE = 25
CP_DIM = 4
CP_INTERVAL = 10


class CameraPositionError(Exception):
    pass


class InvalidCameraPositionError(CameraPositionError):
    pass


def round_timestamps(array: np.ndarray):
    if array is None:
        return None
    output = np.zeros([CP_FRAMERATE * CP_INTERVAL, CP_DIM], np.float32)
    rounded_ts = np.round(array[:, 0] * CP_FRAMERATE) / CP_FRAMERATE
    array_index = np.round((rounded_ts % CP_INTERVAL) * CP_FRAMERATE).astype(int)
    array_index[array[:, 0] == 0] = -1
    for i, ts in enumerate(array_index):
        if ts == -1:
            continue
        output[ts] = array[i]
        output[ts, 0] = round(output[ts, 0] * CP_FRAMERATE) / CP_FRAMERATE
    return output


def merge_arrays(old: np.ndarray, new: np.ndarray) -> np.ndarray:
    if old is None:
        return new
    for i, item in enumerate(new):
        if item[0] != 0:
            old[i] = item
    return old


def get_segment_indeces(np_data):
    rounded_ts = np.round(np_data[:, 0] * CP_FRAMERATE) / CP_FRAMERATE
    time_indexes = (rounded_ts // CP_INTERVAL).astype(int)
    return time_indexes


class CPManager:
    """Tool to savely push camera positions to a cloud bucket"""

    def __init__(self):
        self.client = storage.Client()

    @staticmethod
    def _get_manifest(match_id: str, virtual_cam_id: int, bucket: storage.Bucket):
        manifest_path = f"{match_id}/camera_positions/{virtual_cam_id}/cp.json"
        blob = bucket.blob(manifest_path)
        try:
            manifest_string = blob.download_as_string()
        except NotFound:
            manifest_string = None
        if not manifest_string:
            return None
        try:
            return json.loads(manifest_string)
        except json.JSONDecodeError:
            return None

    @staticmethod
    def _upload_manifest(
        manifest: dict, match_id: str, virtual_cam_id: int, bucket: storage.Bucket
    ):
        for i in range(5):
            try:
                manifest_path = f"{match_id}/camera_positions/{virtual_cam_id}/cp.json"
                blob = bucket.blob(manifest_path)
                blob.cache_control = "no-cache,no-store,must-revalidate,max-age=0"
                blob.upload_from_string(json.dumps(manifest))
                break
            except TooManyRequests:
                pass

    @staticmethod
    def _upload_segment(
        data: bytes,
        match_id: str,
        virtual_camera_id: int,
        time_id: int,
        bucket: storage.Bucket,
    ):

        upload_path = f"{match_id}/camera_positions/{virtual_camera_id}/{time_id}.cp"
        for i in range(5):
            try:
                blob = bucket.blob(upload_path)
                blob.cache_control = "no-cache,no-store,must-revalidate,max-age=0"
                blob.upload_from_string(data)
                break
            except TooManyRequests:
                pass

    def upload_data(
        self, cam_data: bytes, match_id: str, virtual_cam_id: int, bucket_name: str
    ):
        """Push the camera positions to the bucket
        Args:
            cam_data: The camera positions. Must be a base64 encoded float32 array
            match_id: The camera id
            virtual_cam_id: The virtual camera id
            bucket_name: The name of the bucket the camera positions should be stored to

        """

        try:
            np_data = np.frombuffer(b64decode(cam_data), np.float32).reshape(-1, CP_DIM)
        except ValueError:
            raise InvalidCameraPositionError(
                f"The provided data data seems not to contain valid camera positions. "
                f"Make sure your data array is of shape (None, {CP_DIM}), 32bit float "
                f"and is base64 encoded."
            )
        bucket = self.client.bucket(bucket_name)
        time_indexes = get_segment_indeces(np_data)
        time_idx_set = list(set(time_indexes))
        for time_id in sorted(time_idx_set):
            data = np_data[time_indexes == time_id]

            upload_path = f"{match_id}/camera_positions/{virtual_cam_id}/{time_id}.cp"
            blob = bucket.blob(upload_path)
            try:
                existing_data = blob.download_as_string()
                existing_data = np.frombuffer(
                    b64decode(existing_data), np.float32
                ).reshape([-1, CP_DIM])
            except (NotFound, ValueError):
                existing_data = None

            data = round_timestamps(data)
            existing_data = round_timestamps(existing_data)
            data = merge_arrays(existing_data, data)
            cam_data = b64encode(data.tobytes())
            self._upload_segment(cam_data, match_id, virtual_cam_id, time_id, bucket)

        new_max = int(max(time_idx_set))
        manifest = self._get_manifest(match_id, virtual_cam_id, bucket)
        if manifest:
            if "max_index" in manifest:
                old_max = manifest["max_index"]
                if new_max <= old_max:
                    return

        manifest = {
            "max_index": new_max,
            "framerate": CP_FRAMERATE,
            "interval": CP_INTERVAL,
            "dimensions": CP_DIM,
        }
        self._upload_manifest(manifest, match_id, virtual_cam_id, bucket)


class Label:
    """
    Structure to store label data, just wraping numpy arrays
    """

    def __init__(self):
        self.positions_dim = 4
        self.events = np.zeros((0, 3), dtype=np.uint32)
        self.status = np.zeros((11,), dtype=np.uint32)
        self.positions = np.zeros((0, self.positions_dim), dtype=np.float32)
        self.player_positions = {0: np.zeros((25, 3), dtype=np.float32)}
        self.label_resolution = 40

    @classmethod
    def from_file(cls, path="labels.h5"):
        """
        Reads from hdf5 file

        # Attributes
        path(str):
        """
        file = h5.File(path, "r")
        label = cls()
        label.positions = file["labels"][:]
        label.events = file["events"][:]
        label.status = file["status"][:]
        file.close()
        return label

    def save(self, path="labels.h5"):
        """
        Saves label to hdf5

        # Attributes
        path(str):
        """
        file = h5.File(path, "w")
        file["events"] = self.events
        file["labels"] = self.positions
        file["status"] = self.status
        file.close()

    def set_position(self, timestamp, pos: np.ndarray):
        """
        Adds a position to the given timestamp

        # Arguments:
        timestamp (int): video time in ms
        target_position (array): x, y and z where the camera should look at
        actual_position (array): x, y and z where the camera actually looking
        at
        """
        row = int(timestamp / self.label_resolution)
        if self.positions.shape[0] < row + 1:
            self.positions.resize((row + 1, self.positions_dim), refcheck=False)
        item = [row * self.label_resolution, pos[0], pos[1], pos[2]]
        self.positions[row] = item


class CPUploader:
    """Tool to push camera positions to the camera position service"""

    def __init__(
        self,
        match_id: str,
        upload_bucket: str,
        virtual_camera_id: int,
        auth: AuthSerivceBase,
        url: str,
        upload_batch=250,
    ):
        """
        Args:
            match_id: The match id
            upload_bucket: Name of the bucket to upload data to
            virtual_camera_id: The virtual camera id
            auth: The authentication. (username, password)
            url: Url to the camera position upload service
            upload_batch: How many positions should be pushed together
        """
        self.match_id = match_id
        self.virtual_camera_id = virtual_camera_id
        self.label_resolution = 40
        self._position_queue = Queue()
        self._process = Process(target=self._upload_loop, args=(self._position_queue,))
        self.cp_url = url
        self.auth = auth
        self._upload_batch = upload_batch
        self.upload_bucket = upload_bucket
        self._future = None

    def start(self):
        if not self._process.is_alive():
            self._process.start()

    def stop(self):
        if self._process.is_alive():
            self._position_queue.put(None)
            self._process.join()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def _upload_loop(self, queue: Queue):
        items = []
        while True:
            item = queue.get()
            if item is None:
                self._upload_positions(items)
                break
            items.append(item)
            if len(items) >= self._upload_batch:
                self._upload_positions(items)
                items = []

    def _upload_positions(self, items):
        if not items:
            return
        data = b64encode(np.stack(items).tobytes())

        body = {
            "match_id": self.match_id,
            "vci": self.virtual_camera_id,
            "data": data,
            "bucket_name": self.upload_bucket,
        }
        make_request(self.cp_url, body, authorization=self.auth)

    def push_position(self, timestamp: float, pos: np.ndarray):
        """Push one position
        Args:
            timestamp: timestamp of the position in seconds
            pos: [x,y,zoom]

        """

        row = round(timestamp * (1000 / self.label_resolution))
        item = np.array(
            [row * self.label_resolution / 1000, pos[0], pos[1], pos[2]], np.float32
        )
        self._position_queue.put(item)


class CPDownloader:
    """
    Tool to download or stream camera positions

    """

    def __init__(self, match_id: str, virtual_camera_id: int):
        """
        Args:
            match_id: The match id
            virtual_camera_id: The virtual camera id
        """
        self.match_id = match_id
        self.virtual_camera_id = virtual_camera_id
        self._result_queue = Queue()
        self._cp_base_link = (
            f"https://storage.googleapis.com/sw-sc-de-shared/"
            f"{self.match_id}/camera_positions/{self.virtual_camera_id}/"
        )
        self._prefetched_segments = {}

        self._latest_segment = self._get_lastest_segment()
        self._latest_segment_on_timeout = self._latest_segment

        self._process = Process(target=self._loop, args=(self._result_queue,))
        self.stop_flag = Value("b", False)

    def start(self):
        if not self._process.is_alive():
            self.stop_flag.value = False
            self._process.start()

    def stop(self):
        if self._process.is_alive():
            self.stop_flag.value = True
            self._process.join()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def download_all(self) -> np.ndarray:
        """Downloads all camera positions

        Returns: All positions in an [nx4] array

        """
        num_segments = self._get_lastest_segment() + 1

        segments = self._get_segments(range(num_segments))
        data = np.zeros([num_segments * CP_INTERVAL * CP_FRAMERATE, CP_DIM], np.float32)
        for index, segment in enumerate(segments):
            if segment is None:
                continue
            start = index * CP_FRAMERATE * CP_INTERVAL
            end = start + CP_FRAMERATE * CP_INTERVAL
            data[start:end] = segment
        return data

    def _get_manifest(self):
        try:
            data = requests.get(self._cp_base_link + "cp.json")
        except requests.exceptions.ConnectionError as e:
            logger.exception(e)
            return
        if data.status_code == 200:
            return data.json()

    async def _get_segment(self, segment, session: aiohttp.ClientSession):
        async with session.get(self._cp_base_link + f"{segment}.cp") as data:
            if data.status == 200:
                text = await data.text()
                return np.frombuffer(b64decode(text), np.float32).reshape((-1, 4))

    def _get_segments(self, segment_indexes: Iterable):
        loop = asyncio.new_event_loop()

        async def pull():
            async with aiohttp.ClientSession() as session:
                tasks = [self._get_segment(s, session) for s in segment_indexes]

                result = await asyncio.gather(*tasks)
                return result

        segments = loop.run_until_complete(pull())
        return segments

    def _loop(self, result_queue: Queue):
        segment_id = 0
        while not self.stop_flag.value:
            latest_segment = self._get_lastest_segment()
            segments = self._get_segments(range(segment_id, latest_segment))
            for i, s in enumerate(segments):
                result_queue.put([segment_id + i, s])
            segment_id = latest_segment
            time.sleep(5)

    def _process_result_queue(self):
        while not self._result_queue.empty():
            i, segment = self._result_queue.get()
            self._prefetched_segments[i] = segment
            if i > self._latest_segment:
                self._latest_segment = i

    @staticmethod
    def _get_rounded_cam_pos(timestamp: float, segment: np.ndarray) -> np.ndarray:
        row = round(timestamp % CP_INTERVAL * CP_FRAMERATE)
        return segment[row]

    def _get_lastest_segment(self):
        manifest = self._get_manifest()
        total_segments = -1
        if manifest and "max_index" in manifest:
            total_segments = manifest["max_index"]
        return total_segments

    def get_position(
        self, timestamp: float, timeout: float = 0.0
    ) -> Optional[np.ndarray]:
        """Returns the position to the given timestamp

        Downloads the given position from the cloud and prefetches the next positions.
        If you want to random access the positions consider to usw download_all.
        Waits for a certain position if a timeout is given, only if an upload
        activity is recognized.

        Args:
            timestamp: The timestamp of the desired psition.
            timeout: The timeout in seconds to wait for a camera positions if currently
            not available.

        Returns: The position [x,y,zoom]

        """
        if not self._process.is_alive():
            raise RuntimeError(
                "You need to call start() before you can fetch positions"
            )
        timestamp = round(timestamp * CP_FRAMERATE) / CP_FRAMERATE
        segment_id = timestamp // CP_INTERVAL
        start_time = actual_time = 0
        while actual_time - start_time <= timeout:
            self._process_result_queue()
            if segment_id in self._prefetched_segments:
                segment = self._prefetched_segments[segment_id]
                if segment is not None:
                    poi = self._get_rounded_cam_pos(timestamp, segment)
                    if poi[0] != 0:
                        return poi[1:]
                return
            if segment_id - self._latest_segment > timeout / CP_INTERVAL:
                return
            if self._latest_segment_on_timeout == self._latest_segment:
                return
            actual_time = datetime.now().timestamp()
            if start_time == 0:
                start_time = actual_time
            diff = actual_time - start_time
            logger.warning(f"Waiting for position {diff}/{timeout}")
            time.sleep(5)
        self._latest_segment_on_timeout = self._latest_segment

        return
