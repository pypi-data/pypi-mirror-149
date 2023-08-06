"""
Type annotations for mwaa service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_mwaa.client import MWAAClient

    session = get_session()
    async with session.create_client("mwaa") as client:
        client: MWAAClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import WebserverAccessModeType
from .paginator import ListEnvironmentsPaginator
from .type_defs import (
    CreateCliTokenResponseTypeDef,
    CreateEnvironmentOutputTypeDef,
    CreateWebLoginTokenResponseTypeDef,
    GetEnvironmentOutputTypeDef,
    ListEnvironmentsOutputTypeDef,
    ListTagsForResourceOutputTypeDef,
    LoggingConfigurationInputTypeDef,
    MetricDatumTypeDef,
    NetworkConfigurationTypeDef,
    UpdateEnvironmentOutputTypeDef,
    UpdateNetworkConfigurationInputTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("MWAAClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class MWAAClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa.html#MWAA.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MWAAClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa.html#MWAA.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa.html#MWAA.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa/client/#can_paginate)
        """

    async def create_cli_token(self, *, Name: str) -> CreateCliTokenResponseTypeDef:
        """
        Creates a CLI token for the Airflow CLI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa.html#MWAA.Client.create_cli_token)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa/client/#create_cli_token)
        """

    async def create_environment(
        self,
        *,
        DagS3Path: str,
        ExecutionRoleArn: str,
        Name: str,
        NetworkConfiguration: "NetworkConfigurationTypeDef",
        SourceBucketArn: str,
        AirflowConfigurationOptions: Mapping[str, str] = ...,
        AirflowVersion: str = ...,
        EnvironmentClass: str = ...,
        KmsKey: str = ...,
        LoggingConfiguration: "LoggingConfigurationInputTypeDef" = ...,
        MaxWorkers: int = ...,
        MinWorkers: int = ...,
        PluginsS3ObjectVersion: str = ...,
        PluginsS3Path: str = ...,
        RequirementsS3ObjectVersion: str = ...,
        RequirementsS3Path: str = ...,
        Schedulers: int = ...,
        Tags: Mapping[str, str] = ...,
        WebserverAccessMode: WebserverAccessModeType = ...,
        WeeklyMaintenanceWindowStart: str = ...
    ) -> CreateEnvironmentOutputTypeDef:
        """
        Creates an Amazon Managed Workflows for Apache Airflow (MWAA) environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa.html#MWAA.Client.create_environment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa/client/#create_environment)
        """

    async def create_web_login_token(self, *, Name: str) -> CreateWebLoginTokenResponseTypeDef:
        """
        Creates a web login token for the Airflow Web UI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa.html#MWAA.Client.create_web_login_token)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa/client/#create_web_login_token)
        """

    async def delete_environment(self, *, Name: str) -> Dict[str, Any]:
        """
        Deletes an Amazon Managed Workflows for Apache Airflow (MWAA) environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa.html#MWAA.Client.delete_environment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa/client/#delete_environment)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa.html#MWAA.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa/client/#generate_presigned_url)
        """

    async def get_environment(self, *, Name: str) -> GetEnvironmentOutputTypeDef:
        """
        Describes an Amazon Managed Workflows for Apache Airflow (MWAA) environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa.html#MWAA.Client.get_environment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa/client/#get_environment)
        """

    async def list_environments(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListEnvironmentsOutputTypeDef:
        """
        Lists the Amazon Managed Workflows for Apache Airflow (MWAA) environments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa.html#MWAA.Client.list_environments)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa/client/#list_environments)
        """

    async def list_tags_for_resource(self, *, ResourceArn: str) -> ListTagsForResourceOutputTypeDef:
        """
        Lists the key-value tag pairs associated to the Amazon Managed Workflows for
        Apache Airflow (MWAA) environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa.html#MWAA.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa/client/#list_tags_for_resource)
        """

    async def publish_metrics(
        self, *, EnvironmentName: str, MetricData: Sequence["MetricDatumTypeDef"]
    ) -> Dict[str, Any]:
        """
        **Internal only**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa.html#MWAA.Client.publish_metrics)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa/client/#publish_metrics)
        """

    async def tag_resource(self, *, ResourceArn: str, Tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Associates key-value tag pairs to your Amazon Managed Workflows for Apache
        Airflow (MWAA) environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa.html#MWAA.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa/client/#tag_resource)
        """

    async def untag_resource(self, *, ResourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes key-value tag pairs associated to your Amazon Managed Workflows for
        Apache Airflow (MWAA) environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa.html#MWAA.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa/client/#untag_resource)
        """

    async def update_environment(
        self,
        *,
        Name: str,
        AirflowConfigurationOptions: Mapping[str, str] = ...,
        AirflowVersion: str = ...,
        DagS3Path: str = ...,
        EnvironmentClass: str = ...,
        ExecutionRoleArn: str = ...,
        LoggingConfiguration: "LoggingConfigurationInputTypeDef" = ...,
        MaxWorkers: int = ...,
        MinWorkers: int = ...,
        NetworkConfiguration: "UpdateNetworkConfigurationInputTypeDef" = ...,
        PluginsS3ObjectVersion: str = ...,
        PluginsS3Path: str = ...,
        RequirementsS3ObjectVersion: str = ...,
        RequirementsS3Path: str = ...,
        Schedulers: int = ...,
        SourceBucketArn: str = ...,
        WebserverAccessMode: WebserverAccessModeType = ...,
        WeeklyMaintenanceWindowStart: str = ...
    ) -> UpdateEnvironmentOutputTypeDef:
        """
        Updates an Amazon Managed Workflows for Apache Airflow (MWAA) environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa.html#MWAA.Client.update_environment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa/client/#update_environment)
        """

    def get_paginator(
        self, operation_name: Literal["list_environments"]
    ) -> ListEnvironmentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa.html#MWAA.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa/client/#get_paginator)
        """

    async def __aenter__(self) -> "MWAAClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa.html#MWAA.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mwaa.html#MWAA.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mwaa/client/)
        """
