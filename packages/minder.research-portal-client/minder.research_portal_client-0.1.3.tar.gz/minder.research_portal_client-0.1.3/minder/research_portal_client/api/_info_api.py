import asyncio
from http import HTTPStatus
import logging
from typing import final
from backoff import expo, full_jitter
from minder.research_portal_client import ApiClient, ApiException
from minder.research_portal_client.models import AvailableDatasetsResponse, OrganizationsResponse

logger = logging.getLogger(__name__)


@final
class InfoApi(object):
    __base_path = "/info"

    def __init__(self, api_client: ApiClient):
        self.__api_client = api_client

    async def list_datasets(self) -> AvailableDatasetsResponse:
        api_url = f"{self.__base_path}/datasets"
        gen_delay = expo(max_value=self.__api_client.configuration.maximum_retry_delay)
        while True:
            async with self.__api_client.get(api_url) as response:
                if response.status != HTTPStatus.OK:
                    err = ApiException(
                        message="Failed to list datasets", http_resp=response, content=await response.text()
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

                return await self.__api_client.deserialize(response, AvailableDatasetsResponse)

    async def list_organizations(self) -> OrganizationsResponse:
        api_url = f"{self.__base_path}/organizations"
        gen_delay = expo(max_value=self.__api_client.configuration.maximum_retry_delay)
        while True:
            async with self.__api_client.get(api_url) as response:
                if response.status != HTTPStatus.OK:
                    err = ApiException(
                        message="Failed to list organizations", http_resp=response, content=await response.text()
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

                return await self.__api_client.deserialize(response, OrganizationsResponse)
