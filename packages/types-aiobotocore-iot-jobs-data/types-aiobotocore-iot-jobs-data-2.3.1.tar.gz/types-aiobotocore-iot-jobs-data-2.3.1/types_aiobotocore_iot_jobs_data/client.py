"""
Type annotations for iot-jobs-data service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_jobs_data/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iot_jobs_data.client import IoTJobsDataPlaneClient

    session = get_session()
    async with session.create_client("iot-jobs-data") as client:
        client: IoTJobsDataPlaneClient
    ```
"""
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import JobExecutionStatusType
from .type_defs import (
    DescribeJobExecutionResponseTypeDef,
    GetPendingJobExecutionsResponseTypeDef,
    StartNextPendingJobExecutionResponseTypeDef,
    UpdateJobExecutionResponseTypeDef,
)

__all__ = ("IoTJobsDataPlaneClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    CertificateValidationException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    InvalidStateTransitionException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    TerminalStateException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]


class IoTJobsDataPlaneClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-jobs-data.html#IoTJobsDataPlane.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_jobs_data/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IoTJobsDataPlaneClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-jobs-data.html#IoTJobsDataPlane.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_jobs_data/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-jobs-data.html#IoTJobsDataPlane.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_jobs_data/client/#can_paginate)
        """

    async def describe_job_execution(
        self,
        *,
        jobId: str,
        thingName: str,
        includeJobDocument: bool = ...,
        executionNumber: int = ...
    ) -> DescribeJobExecutionResponseTypeDef:
        """
        Gets details of a job execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-jobs-data.html#IoTJobsDataPlane.Client.describe_job_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_jobs_data/client/#describe_job_execution)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-jobs-data.html#IoTJobsDataPlane.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_jobs_data/client/#generate_presigned_url)
        """

    async def get_pending_job_executions(
        self, *, thingName: str
    ) -> GetPendingJobExecutionsResponseTypeDef:
        """
        Gets the list of all jobs for a thing that are not in a terminal status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-jobs-data.html#IoTJobsDataPlane.Client.get_pending_job_executions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_jobs_data/client/#get_pending_job_executions)
        """

    async def start_next_pending_job_execution(
        self,
        *,
        thingName: str,
        statusDetails: Mapping[str, str] = ...,
        stepTimeoutInMinutes: int = ...
    ) -> StartNextPendingJobExecutionResponseTypeDef:
        """
        Gets and starts the next pending (status IN_PROGRESS or QUEUED) job execution
        for a thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-jobs-data.html#IoTJobsDataPlane.Client.start_next_pending_job_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_jobs_data/client/#start_next_pending_job_execution)
        """

    async def update_job_execution(
        self,
        *,
        jobId: str,
        thingName: str,
        status: JobExecutionStatusType,
        statusDetails: Mapping[str, str] = ...,
        stepTimeoutInMinutes: int = ...,
        expectedVersion: int = ...,
        includeJobExecutionState: bool = ...,
        includeJobDocument: bool = ...,
        executionNumber: int = ...
    ) -> UpdateJobExecutionResponseTypeDef:
        """
        Updates the status of a job execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-jobs-data.html#IoTJobsDataPlane.Client.update_job_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_jobs_data/client/#update_job_execution)
        """

    async def __aenter__(self) -> "IoTJobsDataPlaneClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-jobs-data.html#IoTJobsDataPlane.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_jobs_data/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-jobs-data.html#IoTJobsDataPlane.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_jobs_data/client/)
        """
