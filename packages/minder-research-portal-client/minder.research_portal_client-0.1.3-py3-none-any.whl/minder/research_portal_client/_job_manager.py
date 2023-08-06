import asyncio
import logging
from types import TracebackType
import aiohttp
import warnings
from typing import Any, Dict, List, Optional, Type, Union, final
from backoff import full_jitter
from minder.research_portal_client import Configuration, ApiClient
from minder.research_portal_client.models import ExportJobRequest, ExportJobResponse
import traceback
import sys


logger = logging.getLogger(__name__)


@final
class JobManager(object):
    def __init__(
        self,
        configuration: Configuration = None,
        *,
        loop: asyncio.AbstractEventLoop = None,
        api_client: ApiClient = None,
    ):
        if loop is None:
            if api_client is not None:
                loop = api_client._loop

        loop = aiohttp.helpers.get_running_loop(loop)

        if configuration is None:
            configuration = Configuration()
        self.configuration = configuration

        if api_client is None:
            api_client = ApiClient(configuration, loop=loop)

        if api_client._loop is not loop:
            raise RuntimeError("JobManager and ApiClient has to use same event loop")

        self._loop = loop
        self.__api_client = api_client

        if self._loop.get_debug():
            self._source_traceback = traceback.extract_stack(sys._getframe(1))

        self.__job_queue: List[str] = []
        self.__download_queue: List[str] = []

    def __del__(self, _warnings: Any = warnings) -> None:
        if not self.closed:
            kwargs: Dict = {}
            _warnings.warn(f"Unclosed  Job Manager {self!r}", ResourceWarning, **kwargs)
            context = {"job_manager": self, "message": "Unclosed Job Manager"}
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
        tasks = []
        for job_id in self.__job_queue:
            tasks.append(self.client.export.cancel_job(job_id))
        self.__job_queue.clear()
        await asyncio.gather(*tasks, return_exceptions=True)

        if not self.closed:
            await self.client.close()
            self.__api_client = None

    async def submit(self, job: ExportJobRequest):
        job_id = await self.client.export.start_job(job)
        self.__job_queue.append(job_id)

        logger.info(f"Submitted job: {job_id}")
        return job_id

    async def wait(self, job_id: str) -> ExportJobResponse:
        if job_id not in self.__job_queue:
            self.__job_queue.append(job_id)

        while True:
            delay = self.configuration.job_check_interval_min + full_jitter(
                self.configuration.job_check_interval_max - self.configuration.job_check_interval_min
            )

            job_status = await self.client.export.check_job_status(job_id)
            if job_status.status == 202:
                status = job_status.job_progress.progress

                if status == "Queued":
                    logger.info(f"The job is waiting in the queue: {job_id}\nWill check again in {delay:.1f} seconds")
                elif status == "Running":
                    logger.info(f"The job is still running: {job_id}\nWill check again in {delay:.1f} seconds")

                await asyncio.sleep(delay)
                continue

            break

        self.__job_queue.remove(job_id)

        if job_status.status != 200:
            logger.error(f"The job has failed: {job_id}")
        elif len(job_status.job_record.output) == 0:
            logger.warn(f"The job has completed, but produced no data: {job_id}")
        else:
            logger.info(f"The job has completed: {job_id}")
            self.__download_queue.append(job_id)

        return job_status

    async def wait_all(self) -> List[Union[ExportJobResponse, BaseException]]:
        tasks = []
        for job_id in self.__job_queue:
            tasks.append(self.wait(job_id))
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def download(self, job: Union[str, ExportJobResponse]) -> List[str]:
        if isinstance(job, str):
            job_status = await self.__api_client.export.check_job_status(job)
        else:
            job_status = job

        if job_status.status != 200:
            logger.error(f"Cannot download data for failed job: {job_status.id}")
            return []
        elif len(job_status.job_record.output) == 0:
            logger.warn(f"No data to download: {job_status.id}")
            return []

        tasks = []
        for output in job_status.job_record.output:
            tasks.append(self.client.download.download_file(job_status.id, output.url))
        files = await asyncio.gather(*tasks)

        logger.info(f"Successfully downloaded job output: {job_status.id}")
        return files

    async def download_all(self):
        tasks = []
        for job_id in self.__download_queue:
            tasks.append(self.download(job_id))
        return await asyncio.gather(*tasks, return_exceptions=True)

    @property
    def closed(self):
        return self.client is None or self.client.closed

    @property
    def client(self):
        return self.__api_client
