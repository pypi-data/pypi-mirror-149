import asyncio
from http import HTTPStatus
import logging
from typing import List, final
from backoff import expo, full_jitter
from minder.research_portal_client.models import ExportJobRequest, ExportJobResponse
from minder.research_portal_client import ApiClient, ApiException

logger = logging.getLogger(__name__)


@final
class ExportApi(object):
    __base_path = "/export"

    def __init__(self, api_client: ApiClient):
        self.__api_client = api_client

    async def start_job(self, request: ExportJobRequest) -> str:
        api_url = f"{self.__base_path}"
        gen_delay = expo(max_value=self.__api_client.configuration.maximum_retry_delay)
        while True:
            async with self.__api_client.post(api_url, json=request.to_dict()) as response:
                if response.status != HTTPStatus.ACCEPTED:
                    err = ApiException(
                        message="Failed to start export jobs", http_resp=response, content=await response.text()
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

                job_id = response.headers.get("content-location").split("/")[-1]
                return job_id

    async def list_jobs(self) -> List[ExportJobResponse]:
        api_url = f"{self.__base_path}"
        gen_delay = expo(max_value=self.__api_client.configuration.maximum_retry_delay)
        while True:
            async with self.__api_client.get(api_url) as response:
                if response.status != HTTPStatus.OK:
                    err = ApiException(
                        message="Failed to list completed jobs", http_resp=response, content=await response.text()
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

                return await self.__api_client.deserialize(response, "list[ExportJobResponse]")

    async def check_job_status(self, job_id: str) -> ExportJobResponse:
        api_url = f"{self.__base_path}/{job_id}"
        gen_delay = expo(max_value=self.__api_client.configuration.maximum_retry_delay)
        while True:
            async with self.__api_client.get(api_url) as response:
                if response.status == HTTPStatus.INTERNAL_SERVER_ERROR:
                    raise ApiException(message=f"Export job has failed: {job_id}")

                if response.status not in (HTTPStatus.OK, HTTPStatus.ACCEPTED):
                    err = ApiException(
                        message="Failed to get job status", http_resp=response, content=await response.text()
                    )
                    if response.status >= 501 or response.status in [
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

                return await self.__api_client.deserialize(response, ExportJobResponse)

    async def cancel_job(self, job_id: str):
        api_url = f"{self.__base_path}/{job_id}"
        gen_delay = expo(max_value=self.__api_client.configuration.maximum_retry_delay)
        while True:
            async with self.__api_client.delete(api_url) as response:
                if response.status != HTTPStatus.OK:
                    err = ApiException(
                        message="Failed to cancel export job", http_resp=response, content=await response.text()
                    )
                    if response.status >= 500 or response.status in [
                        HTTPStatus.REQUEST_TIMEOUT,
                        425,  # HTTPStatus.TOO_EARLY
                        HTTPStatus.TOO_MANY_REQUESTS,
                        HTTPStatus.PRECONDITION_FAILED,
                    ]:
                        delay = full_jitter(next(gen_delay))
                        err.message = f"{err.message}.\n         Retrying in {delay:.1f} seconds..."
                        logger.error(err)
                        await asyncio.sleep(delay)
                        continue

                    raise err

                return
