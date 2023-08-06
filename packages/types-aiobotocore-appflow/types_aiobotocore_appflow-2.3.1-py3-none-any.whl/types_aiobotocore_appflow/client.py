"""
Type annotations for appflow service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appflow/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_appflow.client import AppflowClient

    session = get_session()
    async with session.create_client("appflow") as client:
        client: AppflowClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import ConnectionModeType, ConnectorTypeType
from .type_defs import (
    ConnectorProfileConfigTypeDef,
    ConnectorProvisioningConfigTypeDef,
    CreateConnectorProfileResponseTypeDef,
    CreateFlowResponseTypeDef,
    DescribeConnectorEntityResponseTypeDef,
    DescribeConnectorProfilesResponseTypeDef,
    DescribeConnectorResponseTypeDef,
    DescribeConnectorsResponseTypeDef,
    DescribeFlowExecutionRecordsResponseTypeDef,
    DescribeFlowResponseTypeDef,
    DestinationFlowConfigTypeDef,
    ListConnectorEntitiesResponseTypeDef,
    ListConnectorsResponseTypeDef,
    ListFlowsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    RegisterConnectorResponseTypeDef,
    SourceFlowConfigTypeDef,
    StartFlowResponseTypeDef,
    StopFlowResponseTypeDef,
    TaskTypeDef,
    TriggerConfigTypeDef,
    UpdateConnectorProfileResponseTypeDef,
    UpdateFlowResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("AppflowClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ConnectorAuthenticationException: Type[BotocoreClientError]
    ConnectorServerException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    UnsupportedOperationException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class AppflowClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appflow.html#Appflow.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appflow/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AppflowClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appflow.html#Appflow.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appflow/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appflow.html#Appflow.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appflow/client/#can_paginate)
        """

    async def create_connector_profile(
        self,
        *,
        connectorProfileName: str,
        connectorType: ConnectorTypeType,
        connectionMode: ConnectionModeType,
        connectorProfileConfig: "ConnectorProfileConfigTypeDef",
        kmsArn: str = ...,
        connectorLabel: str = ...
    ) -> CreateConnectorProfileResponseTypeDef:
        """
        Creates a new connector profile associated with your Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appflow.html#Appflow.Client.create_connector_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appflow/client/#create_connector_profile)
        """

    async def create_flow(
        self,
        *,
        flowName: str,
        triggerConfig: "TriggerConfigTypeDef",
        sourceFlowConfig: "SourceFlowConfigTypeDef",
        destinationFlowConfigList: Sequence["DestinationFlowConfigTypeDef"],
        tasks: Sequence["TaskTypeDef"],
        description: str = ...,
        kmsArn: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateFlowResponseTypeDef:
        """
        Enables your application to create a new flow using Amazon AppFlow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appflow.html#Appflow.Client.create_flow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appflow/client/#create_flow)
        """

    async def delete_connector_profile(
        self, *, connectorProfileName: str, forceDelete: bool = ...
    ) -> Dict[str, Any]:
        """
        Enables you to delete an existing connector profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appflow.html#Appflow.Client.delete_connector_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appflow/client/#delete_connector_profile)
        """

    async def delete_flow(self, *, flowName: str, forceDelete: bool = ...) -> Dict[str, Any]:
        """
        Enables your application to delete an existing flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appflow.html#Appflow.Client.delete_flow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appflow/client/#delete_flow)
        """

    async def describe_connector(
        self, *, connectorType: ConnectorTypeType, connectorLabel: str = ...
    ) -> DescribeConnectorResponseTypeDef:
        """
        Describes the given custom connector registered in your Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appflow.html#Appflow.Client.describe_connector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appflow/client/#describe_connector)
        """

    async def describe_connector_entity(
        self,
        *,
        connectorEntityName: str,
        connectorType: ConnectorTypeType = ...,
        connectorProfileName: str = ...,
        apiVersion: str = ...
    ) -> DescribeConnectorEntityResponseTypeDef:
        """
        Provides details regarding the entity used with the connector, with a
        description of the data model for each entity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appflow.html#Appflow.Client.describe_connector_entity)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appflow/client/#describe_connector_entity)
        """

    async def describe_connector_profiles(
        self,
        *,
        connectorProfileNames: Sequence[str] = ...,
        connectorType: ConnectorTypeType = ...,
        connectorLabel: str = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> DescribeConnectorProfilesResponseTypeDef:
        """
        Returns a list of `connector-profile` details matching the provided `connector-
        profile` names and `connector-types`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appflow.html#Appflow.Client.describe_connector_profiles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appflow/client/#describe_connector_profiles)
        """

    async def describe_connectors(
        self,
        *,
        connectorTypes: Sequence[ConnectorTypeType] = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> DescribeConnectorsResponseTypeDef:
        """
        Describes the connectors vended by Amazon AppFlow for specified connector types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appflow.html#Appflow.Client.describe_connectors)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appflow/client/#describe_connectors)
        """

    async def describe_flow(self, *, flowName: str) -> DescribeFlowResponseTypeDef:
        """
        Provides a description of the specified flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appflow.html#Appflow.Client.describe_flow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appflow/client/#describe_flow)
        """

    async def describe_flow_execution_records(
        self, *, flowName: str, maxResults: int = ..., nextToken: str = ...
    ) -> DescribeFlowExecutionRecordsResponseTypeDef:
        """
        Fetches the execution history of the flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appflow.html#Appflow.Client.describe_flow_execution_records)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appflow/client/#describe_flow_execution_records)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appflow.html#Appflow.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appflow/client/#generate_presigned_url)
        """

    async def list_connector_entities(
        self,
        *,
        connectorProfileName: str = ...,
        connectorType: ConnectorTypeType = ...,
        entitiesPath: str = ...,
        apiVersion: str = ...
    ) -> ListConnectorEntitiesResponseTypeDef:
        """
        Returns the list of available connector entities supported by Amazon AppFlow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appflow.html#Appflow.Client.list_connector_entities)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appflow/client/#list_connector_entities)
        """

    async def list_connectors(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListConnectorsResponseTypeDef:
        """
        Returns the list of all registered custom connectors in your Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appflow.html#Appflow.Client.list_connectors)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appflow/client/#list_connectors)
        """

    async def list_flows(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListFlowsResponseTypeDef:
        """
        Lists all of the flows associated with your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appflow.html#Appflow.Client.list_flows)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appflow/client/#list_flows)
        """

    async def list_tags_for_resource(
        self, *, resourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves the tags that are associated with a specified flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appflow.html#Appflow.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appflow/client/#list_tags_for_resource)
        """

    async def register_connector(
        self,
        *,
        connectorLabel: str = ...,
        description: str = ...,
        connectorProvisioningType: Literal["LAMBDA"] = ...,
        connectorProvisioningConfig: "ConnectorProvisioningConfigTypeDef" = ...
    ) -> RegisterConnectorResponseTypeDef:
        """
        Registers a new connector with your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appflow.html#Appflow.Client.register_connector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appflow/client/#register_connector)
        """

    async def start_flow(self, *, flowName: str) -> StartFlowResponseTypeDef:
        """
        Activates an existing flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appflow.html#Appflow.Client.start_flow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appflow/client/#start_flow)
        """

    async def stop_flow(self, *, flowName: str) -> StopFlowResponseTypeDef:
        """
        Deactivates the existing flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appflow.html#Appflow.Client.stop_flow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appflow/client/#stop_flow)
        """

    async def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Applies a tag to the specified flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appflow.html#Appflow.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appflow/client/#tag_resource)
        """

    async def unregister_connector(
        self, *, connectorLabel: str, forceDelete: bool = ...
    ) -> Dict[str, Any]:
        """
        Unregisters the custom connector registered in your account that matches the
        connectorLabel provided in the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appflow.html#Appflow.Client.unregister_connector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appflow/client/#unregister_connector)
        """

    async def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes a tag from the specified flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appflow.html#Appflow.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appflow/client/#untag_resource)
        """

    async def update_connector_profile(
        self,
        *,
        connectorProfileName: str,
        connectionMode: ConnectionModeType,
        connectorProfileConfig: "ConnectorProfileConfigTypeDef"
    ) -> UpdateConnectorProfileResponseTypeDef:
        """
        Updates a given connector profile associated with your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appflow.html#Appflow.Client.update_connector_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appflow/client/#update_connector_profile)
        """

    async def update_flow(
        self,
        *,
        flowName: str,
        triggerConfig: "TriggerConfigTypeDef",
        sourceFlowConfig: "SourceFlowConfigTypeDef",
        destinationFlowConfigList: Sequence["DestinationFlowConfigTypeDef"],
        tasks: Sequence["TaskTypeDef"],
        description: str = ...
    ) -> UpdateFlowResponseTypeDef:
        """
        Updates an existing flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appflow.html#Appflow.Client.update_flow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appflow/client/#update_flow)
        """

    async def __aenter__(self) -> "AppflowClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appflow.html#Appflow.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appflow/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appflow.html#Appflow.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appflow/client/)
        """
