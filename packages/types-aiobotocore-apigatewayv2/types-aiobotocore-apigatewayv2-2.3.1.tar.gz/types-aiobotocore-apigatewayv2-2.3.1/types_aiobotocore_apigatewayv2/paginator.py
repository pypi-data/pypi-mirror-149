"""
Type annotations for apigatewayv2 service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_apigatewayv2.client import ApiGatewayV2Client
    from types_aiobotocore_apigatewayv2.paginator import (
        GetApisPaginator,
        GetAuthorizersPaginator,
        GetDeploymentsPaginator,
        GetDomainNamesPaginator,
        GetIntegrationResponsesPaginator,
        GetIntegrationsPaginator,
        GetModelsPaginator,
        GetRouteResponsesPaginator,
        GetRoutesPaginator,
        GetStagesPaginator,
    )

    session = get_session()
    with session.create_client("apigatewayv2") as client:
        client: ApiGatewayV2Client

        get_apis_paginator: GetApisPaginator = client.get_paginator("get_apis")
        get_authorizers_paginator: GetAuthorizersPaginator = client.get_paginator("get_authorizers")
        get_deployments_paginator: GetDeploymentsPaginator = client.get_paginator("get_deployments")
        get_domain_names_paginator: GetDomainNamesPaginator = client.get_paginator("get_domain_names")
        get_integration_responses_paginator: GetIntegrationResponsesPaginator = client.get_paginator("get_integration_responses")
        get_integrations_paginator: GetIntegrationsPaginator = client.get_paginator("get_integrations")
        get_models_paginator: GetModelsPaginator = client.get_paginator("get_models")
        get_route_responses_paginator: GetRouteResponsesPaginator = client.get_paginator("get_route_responses")
        get_routes_paginator: GetRoutesPaginator = client.get_paginator("get_routes")
        get_stages_paginator: GetStagesPaginator = client.get_paginator("get_stages")
    ```
"""
import sys
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GetApisResponseTypeDef,
    GetAuthorizersResponseTypeDef,
    GetDeploymentsResponseTypeDef,
    GetDomainNamesResponseTypeDef,
    GetIntegrationResponsesResponseTypeDef,
    GetIntegrationsResponseTypeDef,
    GetModelsResponseTypeDef,
    GetRouteResponsesResponseTypeDef,
    GetRoutesResponseTypeDef,
    GetStagesResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator


__all__ = (
    "GetApisPaginator",
    "GetAuthorizersPaginator",
    "GetDeploymentsPaginator",
    "GetDomainNamesPaginator",
    "GetIntegrationResponsesPaginator",
    "GetIntegrationsPaginator",
    "GetModelsPaginator",
    "GetRouteResponsesPaginator",
    "GetRoutesPaginator",
    "GetStagesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetApisPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetApis)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getapispaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetApisResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetApis.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getapispaginator)
        """


class GetAuthorizersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetAuthorizers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getauthorizerspaginator)
    """

    def paginate(
        self, *, ApiId: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetAuthorizersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetAuthorizers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getauthorizerspaginator)
        """


class GetDeploymentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetDeployments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getdeploymentspaginator)
    """

    def paginate(
        self, *, ApiId: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetDeploymentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetDeployments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getdeploymentspaginator)
        """


class GetDomainNamesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetDomainNames)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getdomainnamespaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetDomainNamesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetDomainNames.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getdomainnamespaginator)
        """


class GetIntegrationResponsesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetIntegrationResponses)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getintegrationresponsespaginator)
    """

    def paginate(
        self, *, ApiId: str, IntegrationId: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetIntegrationResponsesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetIntegrationResponses.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getintegrationresponsespaginator)
        """


class GetIntegrationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetIntegrations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getintegrationspaginator)
    """

    def paginate(
        self, *, ApiId: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetIntegrationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetIntegrations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getintegrationspaginator)
        """


class GetModelsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetModels)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getmodelspaginator)
    """

    def paginate(
        self, *, ApiId: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetModelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetModels.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getmodelspaginator)
        """


class GetRouteResponsesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetRouteResponses)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getrouteresponsespaginator)
    """

    def paginate(
        self, *, ApiId: str, RouteId: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetRouteResponsesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetRouteResponses.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getrouteresponsespaginator)
        """


class GetRoutesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetRoutes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getroutespaginator)
    """

    def paginate(
        self, *, ApiId: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetRoutesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetRoutes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getroutespaginator)
        """


class GetStagesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetStages)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getstagespaginator)
    """

    def paginate(
        self, *, ApiId: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetStagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html#ApiGatewayV2.Paginator.GetStages.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apigatewayv2/paginators/#getstagespaginator)
        """
