import asyncio
import os
import logging
from http import HTTPStatus
import aiohttp
from typing import Generic, TypeVar, final
from backoff import expo, full_jitter
import yarl
from minder.research_portal_client import ApiClient, ApiException


logger = logging.getLogger(__name__)


@final
class DownloadApi(object):
    def __init__(self, api_client: ApiClient):
        self.__api_client = api_client

    async def download_file(self, job_id: str, file_url: str):  # noqa: C901
        file_url = yarl.URL(file_url).path_qs
        if file_url.startswith(self.__api_client.configuration.path_prefix):
            file_url = file_url[len(self.__api_client.configuration.path_prefix) :]

        job_dir = os.path.join(self.__api_client.configuration.download_dir, job_id)
        filepath = os.path.join(job_dir, file_url.split("/")[-1])

        if not os.path.exists(job_dir):
            logger.info(f"Job directory does not exist. Creating: {job_dir}")
            os.makedirs(os.path.abspath(job_dir))

        if os.path.exists(filepath):
            logger.warn(f"File already exists. Checking integrity: {filepath}")
            existing_size = os.path.getsize(filepath)

            gen_delay = expo(max_value=self.__api_client.configuration.maximum_retry_delay)
            while True:
                async with self.__api_client.head(file_url) as response:
                    if response.status != HTTPStatus.OK:
                        err = ApiException(
                            message=f"Failed to get file headers: {filepath}",
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

                    if response.content_length == existing_size:
                        logger.info(f"File already downloaded: {filepath}")
                        return filepath
                    elif response.content_length > existing_size:
                        logger.info(
                            f"Detected partially downloaded file ({existing_size}/{response.content_length}). "
                            f"Resuming: {filepath}"
                        )
                    else:
                        logger.error(f"File size mismatch. Redownloading: {filepath}")
                        os.remove(filepath)
                        existing_size = 0

                break
        else:
            existing_size = 0

        with open(filepath, "ab") as f:
            gen_delay = expo(max_value=self.__api_client.configuration.maximum_retry_delay)
            while True:
                headers = {}
                if existing_size > 0:
                    headers["Range"] = f"bytes={existing_size}-"

                async with self.__api_client.get(file_url, headers=headers) as response:
                    if response.status not in [HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT]:
                        err = ApiException(
                            message=f"Failed to download a file: {filepath}",
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

                    try:
                        iter = _AsyncStreamIteratorWithTimeout(
                            response.content.iter_any(),
                            chunk_timeout=self.__api_client.configuration.file_chunk_timeout,
                        )
                        async for data in iter:
                            f.write(data)
                    except asyncio.TimeoutError:
                        delay = full_jitter(next(gen_delay))
                        logger.warn(
                            f"Connection interupted while downloading a file: {filepath}\n"
                            f"Reconnecting in {delay:.1f} seconds..."
                        )
                        f.flush()
                        existing_size = f.tell()
                        await asyncio.sleep(delay)
                        continue

                logger.debug(f"Successfully downloaded file: {filepath} [{os.path.getsize(filepath)}]")
                break

        return filepath


_T = TypeVar("_T")


class _AsyncStreamIteratorWithTimeout(Generic[_T]):
    def __init__(self, iter: aiohttp.streams.AsyncStreamIterator[_T], chunk_timeout: float):
        self.__iter = iter
        self.__chunk_timeout = chunk_timeout

    def __aiter__(self) -> "_AsyncStreamIteratorWithTimeout[_T]":
        return self

    async def __anext__(self) -> _T:
        result = await asyncio.wait_for(self.__iter.__anext__(), self.__chunk_timeout)
        return result
