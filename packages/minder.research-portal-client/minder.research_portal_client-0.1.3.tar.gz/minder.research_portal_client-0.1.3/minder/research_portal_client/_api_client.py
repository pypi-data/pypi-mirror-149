import asyncio
import datetime
import logging
from types import TracebackType
import aiohttp
import warnings
from typing import Any, Dict, Optional, Type, TypeVar, Union, final
import yarl
from minder.research_portal_client import Configuration, Serializer
import traceback
import sys


_T = TypeVar("_T")
logger = logging.getLogger(__name__)


def _with_config(target):
    def api_call(self, *args, **kwargs):
        if self.closed:
            raise RuntimeError("API client is closed")

        self._session.headers.update({"Authorization": f"Bearer {self.configuration.access_token}"})

        func = target(self)

        url: Union[str, yarl.URL] = args[0]

        if isinstance(url, str):
            url = yarl.URL(url)

        url = url.with_path(f"{self.configuration.path_prefix}{url.path}")

        args = list(args)
        args[0] = url

        return func(*tuple(args), **kwargs)

    return api_call


@final
class ApiClient(object):
    PRIMITIVE_TYPES = (float, bool, bytes, str, int)
    NATIVE_TYPES_MAPPING = {
        "int": int,
        "long": int,
        "float": float,
        "str": str,
        "bool": bool,
        "date": datetime.date,
        "datetime": datetime.datetime,
        "object": object,
    }

    def __init__(self, configuration: Configuration = None, *, loop: asyncio.AbstractEventLoop = None):
        self._loop = aiohttp.helpers.get_running_loop(loop)

        if self._loop.get_debug():
            self._source_traceback = traceback.extract_stack(sys._getframe(1))

        if configuration is None:
            configuration = Configuration()
        self.configuration = configuration

        headers = {}
        if configuration.debug:
            headers["X-Azure-DebugInfo"] = "1"

        async def on_request_start(_, trace_config_ctx, params: aiohttp.TraceRequestStartParams):
            trace_config_ctx.start = asyncio.get_event_loop().time()

        async def on_request_end(_, trace_config_ctx, params: aiohttp.TraceRequestEndParams):
            elapsed = asyncio.get_event_loop().time() - trace_config_ctx.start
            logger.debug(
                "%s %s %d %.3f ms - %d",
                params.method,
                params.url,
                params.response.status,
                elapsed,
                params.response.content_length,
            )

        trace_config = aiohttp.TraceConfig()
        trace_config.on_request_start.append(on_request_start)
        trace_config.on_request_end.append(on_request_end)

        self._session = aiohttp.ClientSession(
            self.configuration.base_url,
            loop=self._loop,
            connector=aiohttp.TCPConnector(ssl=self.configuration.ssl),
            headers=headers,
            trace_configs=[trace_config],
        )

        self.__serializer = Serializer()

    def __del__(self, _warnings: Any = warnings) -> None:
        if not self.closed:
            kwargs: Dict = {}
            _warnings.warn(f"Unclosed  API client {self!r}", ResourceWarning, **kwargs)
            context = {"api_client": self, "message": "Unclosed API client"}
            if self._loop.get_debug():
                context["source_traceback"] = self._source_traceback
            self._loop.call_exception_handler(context)

    def __enter__(self) -> None:
        raise TypeError("Use async with instead")

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.close()

    async def close(self):
        if not self.closed:
            await self._session.close()
            self._session = None

    @property
    def closed(self):
        return self._session is None or self._session.closed

    @_with_config
    def head(self):
        return self._session.head

    @_with_config
    def get(self):
        return self._session.get

    @_with_config
    def post(self):
        return self._session.post

    @_with_config
    def put(self):
        return self._session.put

    @_with_config
    def delete(self):
        return self._session.delete

    @property
    def info(self):
        from minder.research_portal_client.api import InfoApi

        return InfoApi(self)

    @property
    def export(self):
        from minder.research_portal_client.api import ExportApi

        return ExportApi(self)

    @property
    def download(self):
        from minder.research_portal_client.api import DownloadApi

        return DownloadApi(self)

    @property
    def reports(self):
        from minder.research_portal_client.api import ReportsApi

        return ReportsApi(self)

    async def deserialize(self, response: aiohttp.ClientResponse, response_type: Union[Type[_T], str]) -> _T:
        json = await response.json()

        try:
            return self.__serializer.deserialize(json, response_type)

        except ValueError:
            return json


class ApiException(Exception):
    def __init__(
        self,
        status: int = None,
        reason: str = None,
        message: str = None,
        http_resp: aiohttp.ClientResponse = None,
        content: str = None,
    ):
        self.message = message

        if http_resp:
            self.status = http_resp.status
            self.reason = http_resp.reason
            self.headers = http_resp.headers

            self.body = content
            http_resp.release()
        else:
            self.status = status or 0
            self.reason = reason

    def __str__(self):
        """Custom error messages for exception"""
        error_message = "({0})\n" "Reason: {1}\n".format(self.status, self.reason)

        if self.message:
            error_message += "Message: {0}\n".format(self.message)

        if self.headers:
            error_message += "HTTP response headers: {0}\n".format(self.headers)

        if self.body:
            error_message += "HTTP response body: {0}\n".format(self.body)

        return error_message
