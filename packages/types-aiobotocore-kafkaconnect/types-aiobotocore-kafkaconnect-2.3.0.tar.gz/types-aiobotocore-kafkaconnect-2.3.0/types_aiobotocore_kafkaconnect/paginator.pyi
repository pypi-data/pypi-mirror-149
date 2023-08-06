"""
Type annotations for kafkaconnect service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_kafkaconnect.client import KafkaConnectClient
    from types_aiobotocore_kafkaconnect.paginator import (
        ListConnectorsPaginator,
        ListCustomPluginsPaginator,
        ListWorkerConfigurationsPaginator,
    )

    session = get_session()
    with session.create_client("kafkaconnect") as client:
        client: KafkaConnectClient

        list_connectors_paginator: ListConnectorsPaginator = client.get_paginator("list_connectors")
        list_custom_plugins_paginator: ListCustomPluginsPaginator = client.get_paginator("list_custom_plugins")
        list_worker_configurations_paginator: ListWorkerConfigurationsPaginator = client.get_paginator("list_worker_configurations")
    ```
"""
import sys
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListConnectorsResponseTypeDef,
    ListCustomPluginsResponseTypeDef,
    ListWorkerConfigurationsResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator

__all__ = (
    "ListConnectorsPaginator",
    "ListCustomPluginsPaginator",
    "ListWorkerConfigurationsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListConnectorsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect.html#KafkaConnect.Paginator.ListConnectors)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/paginators/#listconnectorspaginator)
    """

    def paginate(
        self, *, connectorNamePrefix: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListConnectorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect.html#KafkaConnect.Paginator.ListConnectors.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/paginators/#listconnectorspaginator)
        """

class ListCustomPluginsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect.html#KafkaConnect.Paginator.ListCustomPlugins)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/paginators/#listcustompluginspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListCustomPluginsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect.html#KafkaConnect.Paginator.ListCustomPlugins.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/paginators/#listcustompluginspaginator)
        """

class ListWorkerConfigurationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect.html#KafkaConnect.Paginator.ListWorkerConfigurations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/paginators/#listworkerconfigurationspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListWorkerConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafkaconnect.html#KafkaConnect.Paginator.ListWorkerConfigurations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/paginators/#listworkerconfigurationspaginator)
        """
