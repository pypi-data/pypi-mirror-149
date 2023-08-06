import asyncio
from http import HTTPStatus
import logging
import os
from typing import List, final
from backoff import expo, full_jitter
from minder.research_portal_client import ApiClient, ApiException
import pathlib

logger = logging.getLogger(__name__)


@final
class ReportsApi(object):
    __base_path = "/reports"

    def __init__(self, api_client: ApiClient):
        self.__api_client = api_client

    async def list_reports(self) -> "List[str]":
        api_url = f"{self.__base_path}"
        gen_delay = expo(max_value=self.__api_client.configuration.maximum_retry_delay)
        while True:
            async with self.__api_client.get(api_url) as response:
                if response.status != HTTPStatus.OK:
                    err = ApiException(
                        message="Failed to list reports", http_resp=response, content=await response.text()
                    )
                    if response.status >= 500 or response.status in [
                        HTTPStatus.REQUEST_TIMEOUT,
                        425,  # HTTPStatus.TOO_EARLY
                        HTTPStatus.TOO_MANY_REQUESTS,
                    ]:
                        delay = full_jitter(next(gen_delay))
                        err.message = f"{err.message}.\n         Retrying in {delay:.1f} seconds..."
                        logger.error(err)
                        await asyncio.sleep(delay)
                        continue

                    raise err

                return await self.__api_client.deserialize(response, "list[str]")

    async def upload_report(self, filepath: str, remote_path: str = None, content_type: str = None) -> str:
        if not os.path.exists(filepath):
            raise ApiException(status=0, reason="Failed to find a file to upload")

        if remote_path is None:
            remote_path = os.path.basename(filepath)

        api_url = f"{self.__base_path}/{remote_path}"

        if content_type is None:
            ext = pathlib.Path(filepath).suffix
            if ext == ".html":
                content_type = "text/html"
            elif ext == ".pdf":
                content_type = "application/pdf"
            elif ext == ".csv":
                content_type = "text/csv"
            else:
                content_type = "application/octet-stream"

        headers = {"content-type": content_type}

        gen_delay = expo(max_value=self.__api_client.configuration.maximum_retry_delay)
        while True:
            with open(filepath, "rb") as f:
                async with self.__api_client.put(api_url, data=f, headers=headers) as response:
                    if response.status != HTTPStatus.OK:
                        err = ApiException(
                            message=f"Failed to upload report: {filepath}",
                            http_resp=response,
                            content=await response.text(),
                        )
                        if response.status >= 500 or response.status in [
                            HTTPStatus.REQUEST_TIMEOUT,
                            425,  # HTTPStatus.TOO_EARLY
                            HTTPStatus.TOO_MANY_REQUESTS,
                        ]:
                            delay = full_jitter(next(gen_delay))
                            err.message = f"{err.message}.\n         Retrying in {delay:.1f} seconds..."
                            logger.error(err)
                            await asyncio.sleep(delay)
                            continue

                        raise err

                    return response.headers()["content-location"]
