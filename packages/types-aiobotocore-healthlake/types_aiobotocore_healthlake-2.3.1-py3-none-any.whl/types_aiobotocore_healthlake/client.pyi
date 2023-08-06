"""
Type annotations for healthlake service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_healthlake.client import HealthLakeClient

    session = get_session()
    async with session.create_client("healthlake") as client:
        client: HealthLakeClient
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import JobStatusType
from .type_defs import (
    CreateFHIRDatastoreResponseTypeDef,
    DatastoreFilterTypeDef,
    DeleteFHIRDatastoreResponseTypeDef,
    DescribeFHIRDatastoreResponseTypeDef,
    DescribeFHIRExportJobResponseTypeDef,
    DescribeFHIRImportJobResponseTypeDef,
    InputDataConfigTypeDef,
    ListFHIRDatastoresResponseTypeDef,
    ListFHIRExportJobsResponseTypeDef,
    ListFHIRImportJobsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    OutputDataConfigTypeDef,
    PreloadDataConfigTypeDef,
    SseConfigurationTypeDef,
    StartFHIRExportJobResponseTypeDef,
    StartFHIRImportJobResponseTypeDef,
    TagTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("HealthLakeClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class HealthLakeClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake.html#HealthLake.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        HealthLakeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake.html#HealthLake.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#exceptions)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake.html#HealthLake.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#can_paginate)
        """
    async def create_fhir_datastore(
        self,
        *,
        DatastoreTypeVersion: Literal["R4"],
        DatastoreName: str = ...,
        SseConfiguration: "SseConfigurationTypeDef" = ...,
        PreloadDataConfig: "PreloadDataConfigTypeDef" = ...,
        ClientToken: str = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateFHIRDatastoreResponseTypeDef:
        """
        Creates a Data Store that can ingest and export FHIR formatted data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake.html#HealthLake.Client.create_fhir_datastore)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#create_fhir_datastore)
        """
    async def delete_fhir_datastore(
        self, *, DatastoreId: str = ...
    ) -> DeleteFHIRDatastoreResponseTypeDef:
        """
        Deletes a Data Store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake.html#HealthLake.Client.delete_fhir_datastore)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#delete_fhir_datastore)
        """
    async def describe_fhir_datastore(
        self, *, DatastoreId: str = ...
    ) -> DescribeFHIRDatastoreResponseTypeDef:
        """
        Gets the properties associated with the FHIR Data Store, including the Data
        Store ID, Data Store ARN, Data Store name, Data Store status, created at, Data
        Store type version, and Data Store endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake.html#HealthLake.Client.describe_fhir_datastore)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#describe_fhir_datastore)
        """
    async def describe_fhir_export_job(
        self, *, DatastoreId: str, JobId: str
    ) -> DescribeFHIRExportJobResponseTypeDef:
        """
        Displays the properties of a FHIR export job, including the ID, ARN, name, and
        the status of the job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake.html#HealthLake.Client.describe_fhir_export_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#describe_fhir_export_job)
        """
    async def describe_fhir_import_job(
        self, *, DatastoreId: str, JobId: str
    ) -> DescribeFHIRImportJobResponseTypeDef:
        """
        Displays the properties of a FHIR import job, including the ID, ARN, name, and
        the status of the job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake.html#HealthLake.Client.describe_fhir_import_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#describe_fhir_import_job)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake.html#HealthLake.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#generate_presigned_url)
        """
    async def list_fhir_datastores(
        self, *, Filter: "DatastoreFilterTypeDef" = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> ListFHIRDatastoresResponseTypeDef:
        """
        Lists all FHIR Data Stores that are in the user’s account, regardless of Data
        Store status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake.html#HealthLake.Client.list_fhir_datastores)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#list_fhir_datastores)
        """
    async def list_fhir_export_jobs(
        self,
        *,
        DatastoreId: str,
        NextToken: str = ...,
        MaxResults: int = ...,
        JobName: str = ...,
        JobStatus: JobStatusType = ...,
        SubmittedBefore: Union[datetime, str] = ...,
        SubmittedAfter: Union[datetime, str] = ...
    ) -> ListFHIRExportJobsResponseTypeDef:
        """
        Lists all FHIR export jobs associated with an account and their statuses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake.html#HealthLake.Client.list_fhir_export_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#list_fhir_export_jobs)
        """
    async def list_fhir_import_jobs(
        self,
        *,
        DatastoreId: str,
        NextToken: str = ...,
        MaxResults: int = ...,
        JobName: str = ...,
        JobStatus: JobStatusType = ...,
        SubmittedBefore: Union[datetime, str] = ...,
        SubmittedAfter: Union[datetime, str] = ...
    ) -> ListFHIRImportJobsResponseTypeDef:
        """
        Lists all FHIR import jobs associated with an account and their statuses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake.html#HealthLake.Client.list_fhir_import_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#list_fhir_import_jobs)
        """
    async def list_tags_for_resource(
        self, *, ResourceARN: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of all existing tags associated with a Data Store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake.html#HealthLake.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#list_tags_for_resource)
        """
    async def start_fhir_export_job(
        self,
        *,
        OutputDataConfig: "OutputDataConfigTypeDef",
        DatastoreId: str,
        DataAccessRoleArn: str,
        ClientToken: str,
        JobName: str = ...
    ) -> StartFHIRExportJobResponseTypeDef:
        """
        Begins a FHIR export job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake.html#HealthLake.Client.start_fhir_export_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#start_fhir_export_job)
        """
    async def start_fhir_import_job(
        self,
        *,
        InputDataConfig: "InputDataConfigTypeDef",
        JobOutputDataConfig: "OutputDataConfigTypeDef",
        DatastoreId: str,
        DataAccessRoleArn: str,
        ClientToken: str,
        JobName: str = ...
    ) -> StartFHIRImportJobResponseTypeDef:
        """
        Begins a FHIR Import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake.html#HealthLake.Client.start_fhir_import_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#start_fhir_import_job)
        """
    async def tag_resource(
        self, *, ResourceARN: str, Tags: Sequence["TagTypeDef"]
    ) -> Dict[str, Any]:
        """
        Adds a user specifed key and value tag to a Data Store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake.html#HealthLake.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#tag_resource)
        """
    async def untag_resource(self, *, ResourceARN: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes tags from a Data Store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake.html#HealthLake.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/#untag_resource)
        """
    async def __aenter__(self) -> "HealthLakeClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake.html#HealthLake.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake.html#HealthLake.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/client/)
        """
