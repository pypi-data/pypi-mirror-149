import os
import copy
import tempfile
import yarl


class Configuration(object):

    _default = None

    def __init__(
        self,
        base_url: str = None,
        *,
        access_token_path: str = None,
        access_token: str = None,
        file_chunk_timeout: float = 15.0,
        download_dir: str = None,
        ssl: bool = True,
        debug: bool = False,
        maximum_retry_delay: float = 30.0,
        job_check_interval_min: float = 10.0,
        job_check_interval_max: float = 30.0,
    ):
        if self._default:
            for key in self._default.__dict__.keys():
                self.__dict__[key] = copy.copy(self._default.__dict__[key])
            return

        full_base = yarl.URL(base_url or os.getenv("RESEARCH_PORTAL_API") or "https://research.minder.care/api")
        self.base_url = full_base.with_path("/")
        self.path_prefix = full_base.path

        if self.path_prefix.endswith("/"):
            self.path_prefix = self.path_prefix[:-1]

        self.__access_token_path = access_token_path or os.getenv("RESEARCH_PORTAL_TOKEN_PATH")
        if self.__access_token_path:
            if not os.path.exists(self.__access_token_path):
                raise ConfigurationException("RESEARCH_PORTAL_TOKEN_PATH point to a file that does not exist")
        else:
            self.__access_token_from_env = access_token or os.getenv("MINDER_TOKEN")
            if not self.__access_token_from_env:
                raise ConfigurationException(
                    "Either RESEARCH_PORTAL_TOKEN_PATH or MINDER_TOKEN environment variable must be set"
                )

        self.file_chunk_timeout = file_chunk_timeout
        self.download_dir = os.path.normpath(download_dir or os.path.join(tempfile.gettempdir(), "minder"))
        self.ssl = ssl
        self.debug = debug
        self.maximum_retry_delay = maximum_retry_delay
        self.job_check_interval_min = job_check_interval_min
        self.job_check_interval_max = job_check_interval_max

    @classmethod
    def set_default(cls, default: "Configuration"):
        cls._default = default

    @property
    def access_token(self):
        if self.__access_token_path:
            with open(self.__access_token_path) as f:
                access_token = f.read().strip()
        else:
            access_token = self.__access_token_from_env

        return access_token


class ConfigurationException(Exception):
    def __init__(self, reason: str):
        self.reason = reason

    def __str__(self):
        return "Invalid Configuration: {0}\n".format(self.reason)
