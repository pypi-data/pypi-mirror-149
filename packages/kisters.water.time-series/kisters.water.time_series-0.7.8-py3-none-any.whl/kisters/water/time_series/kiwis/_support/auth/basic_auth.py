import base64
import logging
from abc import ABC, abstractmethod


class Auth(ABC):
    @abstractmethod
    def auth_header(self, refresh: bool = False) -> str:
        """Returns the authentication header"""


class BasicAuth(Auth):
    """Basic authentication module."""

    def __init__(self, user: str, password: str):
        self._user = user
        self._password = password
        self._logger = logging.getLogger(__name__)

    def auth_header(self, refresh: bool = False) -> str:
        """Get the auth header."""
        try:
            e = base64.b64encode(bytes(self._user + ":" + self._password, "utf-8")).decode("utf-8")
        except TypeError:
            e = base64.b64encode(self._user + ":" + self._password).decode("utf-8")
        self._logger.debug("Using basic auth with header {}".format(e))
        return "Basic " + e
