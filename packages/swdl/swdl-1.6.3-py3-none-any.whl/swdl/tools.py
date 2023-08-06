import time
from typing import Optional

import requests
import simplejson as json


class AuthSerivceBase:
    @property
    def auth(self):
        raise NotImplementedError()


def make_request(
    url: str,
    body: dict = None,
    authorization: Optional[AuthSerivceBase] = None,
    retries: int = 3,
    **kwargs,
) -> dict:
    """

    Args:
        url: The url to send the request to.
        body: The body to send to the url. If not body is specified the GET method will
            be used. POST otherwise.
        authorization: Auth Service Object to handle Authentication.
        retries: Number of retries before aborting.
        **kwargs: Additional options which will be passed to requests call.

    Returns:
        The response as dictionary

    """
    auth = None
    if authorization:
        auth = authorization.auth
    exception = None
    for i in range(retries):
        time.sleep(i ** 2)
        try:
            if body is None:
                ret = requests.get(url, auth=auth, **kwargs)
            else:
                ret = requests.post(url, json=body, auth=auth, **kwargs)

        except requests.RequestException as e:
            exception = e
            continue
        if ret.status_code >= 500:
            exception = ConnectionError("Internal Server Error")
            continue
        if ret.status_code == 403:
            exception = ConnectionError("Failed to authenticate")
            continue
        if ret.status_code == 200:
            try:
                return ret.json()
            except json.JSONDecodeError as e:
                if ret.text == "":
                    return {"success": True}
                exception = e
                continue
        exception = ConnectionError(ret.text)
    raise ConnectionError(f"Failed to fetch data from {url}") from exception
