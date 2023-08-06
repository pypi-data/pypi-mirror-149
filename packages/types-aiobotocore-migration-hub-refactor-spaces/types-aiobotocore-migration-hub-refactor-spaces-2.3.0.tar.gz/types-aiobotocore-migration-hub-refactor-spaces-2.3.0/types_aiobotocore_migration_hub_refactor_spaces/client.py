"""
Type annotations for migration-hub-refactor-spaces service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_migration_hub_refactor_spaces.client import MigrationHubRefactorSpacesClient

    session = get_session()
    async with session.create_client("migration-hub-refactor-spaces") as client:
        client: MigrationHubRefactorSpacesClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import RouteTypeType, ServiceEndpointTypeType
from .paginator import (
    ListApplicationsPaginator,
    ListEnvironmentsPaginator,
    ListEnvironmentVpcsPaginator,
    ListRoutesPaginator,
    ListServicesPaginator,
)
from .type_defs import (
    ApiGatewayProxyInputTypeDef,
    CreateApplicationResponseTypeDef,
    CreateEnvironmentResponseTypeDef,
    CreateRouteResponseTypeDef,
    CreateServiceResponseTypeDef,
    DeleteApplicationResponseTypeDef,
    DeleteEnvironmentResponseTypeDef,
    DeleteRouteResponseTypeDef,
    DeleteServiceResponseTypeDef,
    GetApplicationResponseTypeDef,
    GetEnvironmentResponseTypeDef,
    GetResourcePolicyResponseTypeDef,
    GetRouteResponseTypeDef,
    GetServiceResponseTypeDef,
    LambdaEndpointInputTypeDef,
    ListApplicationsResponseTypeDef,
    ListEnvironmentsResponseTypeDef,
    ListEnvironmentVpcsResponseTypeDef,
    ListRoutesResponseTypeDef,
    ListServicesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    UriPathRouteInputTypeDef,
    UrlEndpointInputTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("MigrationHubRefactorSpacesClient",)


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
    InvalidResourcePolicyException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class MigrationHubRefactorSpacesClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MigrationHubRefactorSpacesClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/#can_paginate)
        """

    async def create_application(
        self,
        *,
        EnvironmentIdentifier: str,
        Name: str,
        ProxyType: Literal["API_GATEWAY"],
        VpcId: str,
        ApiGatewayProxy: "ApiGatewayProxyInputTypeDef" = ...,
        ClientToken: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateApplicationResponseTypeDef:
        """
        Creates an Amazon Web Services Migration Hub Refactor Spaces application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.create_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/#create_application)
        """

    async def create_environment(
        self,
        *,
        Name: str,
        NetworkFabricType: Literal["TRANSIT_GATEWAY"],
        ClientToken: str = ...,
        Description: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateEnvironmentResponseTypeDef:
        """
        Creates an Amazon Web Services Migration Hub Refactor Spaces environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.create_environment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/#create_environment)
        """

    async def create_route(
        self,
        *,
        ApplicationIdentifier: str,
        EnvironmentIdentifier: str,
        RouteType: RouteTypeType,
        ServiceIdentifier: str,
        ClientToken: str = ...,
        Tags: Mapping[str, str] = ...,
        UriPathRoute: "UriPathRouteInputTypeDef" = ...
    ) -> CreateRouteResponseTypeDef:
        """
        Creates an Amazon Web Services Migration Hub Refactor Spaces route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.create_route)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/#create_route)
        """

    async def create_service(
        self,
        *,
        ApplicationIdentifier: str,
        EndpointType: ServiceEndpointTypeType,
        EnvironmentIdentifier: str,
        Name: str,
        ClientToken: str = ...,
        Description: str = ...,
        LambdaEndpoint: "LambdaEndpointInputTypeDef" = ...,
        Tags: Mapping[str, str] = ...,
        UrlEndpoint: "UrlEndpointInputTypeDef" = ...,
        VpcId: str = ...
    ) -> CreateServiceResponseTypeDef:
        """
        Creates an Amazon Web Services Migration Hub Refactor Spaces service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.create_service)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/#create_service)
        """

    async def delete_application(
        self, *, ApplicationIdentifier: str, EnvironmentIdentifier: str
    ) -> DeleteApplicationResponseTypeDef:
        """
        Deletes an Amazon Web Services Migration Hub Refactor Spaces application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.delete_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/#delete_application)
        """

    async def delete_environment(
        self, *, EnvironmentIdentifier: str
    ) -> DeleteEnvironmentResponseTypeDef:
        """
        Deletes an Amazon Web Services Migration Hub Refactor Spaces environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.delete_environment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/#delete_environment)
        """

    async def delete_resource_policy(self, *, Identifier: str) -> Dict[str, Any]:
        """
        Deletes the resource policy set for the environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.delete_resource_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/#delete_resource_policy)
        """

    async def delete_route(
        self, *, ApplicationIdentifier: str, EnvironmentIdentifier: str, RouteIdentifier: str
    ) -> DeleteRouteResponseTypeDef:
        """
        Deletes an Amazon Web Services Migration Hub Refactor Spaces route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.delete_route)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/#delete_route)
        """

    async def delete_service(
        self, *, ApplicationIdentifier: str, EnvironmentIdentifier: str, ServiceIdentifier: str
    ) -> DeleteServiceResponseTypeDef:
        """
        Deletes an Amazon Web Services Migration Hub Refactor Spaces service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.delete_service)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/#delete_service)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/#generate_presigned_url)
        """

    async def get_application(
        self, *, ApplicationIdentifier: str, EnvironmentIdentifier: str
    ) -> GetApplicationResponseTypeDef:
        """
        Gets an Amazon Web Services Migration Hub Refactor Spaces application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.get_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/#get_application)
        """

    async def get_environment(self, *, EnvironmentIdentifier: str) -> GetEnvironmentResponseTypeDef:
        """
        Gets an Amazon Web Services Migration Hub Refactor Spaces environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.get_environment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/#get_environment)
        """

    async def get_resource_policy(self, *, Identifier: str) -> GetResourcePolicyResponseTypeDef:
        """
        Gets the resource-based permission policy that is set for the given environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.get_resource_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/#get_resource_policy)
        """

    async def get_route(
        self, *, ApplicationIdentifier: str, EnvironmentIdentifier: str, RouteIdentifier: str
    ) -> GetRouteResponseTypeDef:
        """
        Gets an Amazon Web Services Migration Hub Refactor Spaces route.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.get_route)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/#get_route)
        """

    async def get_service(
        self, *, ApplicationIdentifier: str, EnvironmentIdentifier: str, ServiceIdentifier: str
    ) -> GetServiceResponseTypeDef:
        """
        Gets an Amazon Web Services Migration Hub Refactor Spaces service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.get_service)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/#get_service)
        """

    async def list_applications(
        self, *, EnvironmentIdentifier: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListApplicationsResponseTypeDef:
        """
        Lists all the Amazon Web Services Migration Hub Refactor Spaces applications
        within an environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.list_applications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/#list_applications)
        """

    async def list_environment_vpcs(
        self, *, EnvironmentIdentifier: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListEnvironmentVpcsResponseTypeDef:
        """
        Lists all Amazon Web Services Migration Hub Refactor Spaces service virtual
        private clouds (VPCs) that are part of the environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.list_environment_vpcs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/#list_environment_vpcs)
        """

    async def list_environments(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListEnvironmentsResponseTypeDef:
        """
        Lists Amazon Web Services Migration Hub Refactor Spaces environments owned by a
        caller account or shared with the caller account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.list_environments)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/#list_environments)
        """

    async def list_routes(
        self,
        *,
        ApplicationIdentifier: str,
        EnvironmentIdentifier: str,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListRoutesResponseTypeDef:
        """
        Lists all the Amazon Web Services Migration Hub Refactor Spaces routes within an
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.list_routes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/#list_routes)
        """

    async def list_services(
        self,
        *,
        ApplicationIdentifier: str,
        EnvironmentIdentifier: str,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListServicesResponseTypeDef:
        """
        Lists all the Amazon Web Services Migration Hub Refactor Spaces services within
        an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.list_services)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/#list_services)
        """

    async def list_tags_for_resource(
        self, *, ResourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags of a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/#list_tags_for_resource)
        """

    async def put_resource_policy(self, *, Policy: str, ResourceArn: str) -> Dict[str, Any]:
        """
        Attaches a resource-based permission policy to the Amazon Web Services Migration
        Hub Refactor Spaces environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.put_resource_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/#put_resource_policy)
        """

    async def tag_resource(self, *, ResourceArn: str, Tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Removes the tags of a given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/#tag_resource)
        """

    async def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Adds to or modifies the tags of the given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/#untag_resource)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_applications"]
    ) -> ListApplicationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_environment_vpcs"]
    ) -> ListEnvironmentVpcsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_environments"]
    ) -> ListEnvironmentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_routes"]) -> ListRoutesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_services"]) -> ListServicesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/#get_paginator)
        """

    async def __aenter__(self) -> "MigrationHubRefactorSpacesClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces.html#MigrationHubRefactorSpaces.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/client/)
        """
