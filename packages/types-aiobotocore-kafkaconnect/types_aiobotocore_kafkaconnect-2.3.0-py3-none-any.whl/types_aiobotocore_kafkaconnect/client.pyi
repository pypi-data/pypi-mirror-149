"""
Type annotations for kafkaconnect service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kafkaconnect.client import KafkaConnectClient

    session = get_session()
    async with session.create_client("kafkaconnect") as client:
        client: KafkaConnectClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import CustomPluginContentTypeType
from .paginator import (
    ListConnectorsPaginator,
    ListCustomPluginsPaginator,
    ListWorkerConfigurationsPaginator,
)
from .type_defs import (
    CapacityTypeDef,
    CapacityUpdateTypeDef,
    CreateConnectorResponseTypeDef,
    CreateCustomPluginResponseTypeDef,
    CreateWorkerConfigurationResponseTypeDef,
    CustomPluginLocationTypeDef,
    DeleteConnectorResponseTypeDef,
    DeleteCustomPluginResponseTypeDef,
    DescribeConnectorResponseTypeDef,
    DescribeCustomPluginResponseTypeDef,
    DescribeWorkerConfigurationResponseTypeDef,
    KafkaClusterClientAuthenticationTypeDef,
    KafkaClusterEncryptionInTransitTypeDef,
    KafkaClusterTypeDef,
    ListConnectorsResponseTypeDef,
    ListCustomPluginsResponseTypeDef,
    ListWorkerConfigurationsResponseTypeDef,
    LogDeliveryTypeDef,
    PluginTypeDef,
    UpdateConnectorResponseTypeDef,
    WorkerConfigurationTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("KafkaConnectClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]

class KafkaConnectClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect.html#KafkaConnect.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        KafkaConnectClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect.html#KafkaConnect.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/client/#exceptions)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect.html#KafkaConnect.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/client/#can_paginate)
        """
    async def create_connector(
        self,
        *,
        capacity: "CapacityTypeDef",
        connectorConfiguration: Mapping[str, str],
        connectorName: str,
        kafkaCluster: "KafkaClusterTypeDef",
        kafkaClusterClientAuthentication: "KafkaClusterClientAuthenticationTypeDef",
        kafkaClusterEncryptionInTransit: "KafkaClusterEncryptionInTransitTypeDef",
        kafkaConnectVersion: str,
        plugins: Sequence["PluginTypeDef"],
        serviceExecutionRoleArn: str,
        connectorDescription: str = ...,
        logDelivery: "LogDeliveryTypeDef" = ...,
        workerConfiguration: "WorkerConfigurationTypeDef" = ...
    ) -> CreateConnectorResponseTypeDef:
        """
        Creates a connector using the specified properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect.html#KafkaConnect.Client.create_connector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/client/#create_connector)
        """
    async def create_custom_plugin(
        self,
        *,
        contentType: CustomPluginContentTypeType,
        location: "CustomPluginLocationTypeDef",
        name: str,
        description: str = ...
    ) -> CreateCustomPluginResponseTypeDef:
        """
        Creates a custom plugin using the specified properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect.html#KafkaConnect.Client.create_custom_plugin)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/client/#create_custom_plugin)
        """
    async def create_worker_configuration(
        self, *, name: str, propertiesFileContent: str, description: str = ...
    ) -> CreateWorkerConfigurationResponseTypeDef:
        """
        Creates a worker configuration using the specified properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect.html#KafkaConnect.Client.create_worker_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/client/#create_worker_configuration)
        """
    async def delete_connector(
        self, *, connectorArn: str, currentVersion: str = ...
    ) -> DeleteConnectorResponseTypeDef:
        """
        Deletes the specified connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect.html#KafkaConnect.Client.delete_connector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/client/#delete_connector)
        """
    async def delete_custom_plugin(
        self, *, customPluginArn: str
    ) -> DeleteCustomPluginResponseTypeDef:
        """
        Deletes a custom plugin.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect.html#KafkaConnect.Client.delete_custom_plugin)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/client/#delete_custom_plugin)
        """
    async def describe_connector(self, *, connectorArn: str) -> DescribeConnectorResponseTypeDef:
        """
        Returns summary information about the connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect.html#KafkaConnect.Client.describe_connector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/client/#describe_connector)
        """
    async def describe_custom_plugin(
        self, *, customPluginArn: str
    ) -> DescribeCustomPluginResponseTypeDef:
        """
        A summary description of the custom plugin.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect.html#KafkaConnect.Client.describe_custom_plugin)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/client/#describe_custom_plugin)
        """
    async def describe_worker_configuration(
        self, *, workerConfigurationArn: str
    ) -> DescribeWorkerConfigurationResponseTypeDef:
        """
        Returns information about a worker configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect.html#KafkaConnect.Client.describe_worker_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/client/#describe_worker_configuration)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect.html#KafkaConnect.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/client/#generate_presigned_url)
        """
    async def list_connectors(
        self, *, connectorNamePrefix: str = ..., maxResults: int = ..., nextToken: str = ...
    ) -> ListConnectorsResponseTypeDef:
        """
        Returns a list of all the connectors in this account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect.html#KafkaConnect.Client.list_connectors)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/client/#list_connectors)
        """
    async def list_custom_plugins(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListCustomPluginsResponseTypeDef:
        """
        Returns a list of all of the custom plugins in this account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect.html#KafkaConnect.Client.list_custom_plugins)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/client/#list_custom_plugins)
        """
    async def list_worker_configurations(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListWorkerConfigurationsResponseTypeDef:
        """
        Returns a list of all of the worker configurations in this account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect.html#KafkaConnect.Client.list_worker_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/client/#list_worker_configurations)
        """
    async def update_connector(
        self, *, capacity: "CapacityUpdateTypeDef", connectorArn: str, currentVersion: str
    ) -> UpdateConnectorResponseTypeDef:
        """
        Updates the specified connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect.html#KafkaConnect.Client.update_connector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/client/#update_connector)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_connectors"]) -> ListConnectorsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect.html#KafkaConnect.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_custom_plugins"]
    ) -> ListCustomPluginsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect.html#KafkaConnect.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_worker_configurations"]
    ) -> ListWorkerConfigurationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect.html#KafkaConnect.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/client/#get_paginator)
        """
    async def __aenter__(self) -> "KafkaConnectClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect.html#KafkaConnect.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect.html#KafkaConnect.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/client/)
        """
