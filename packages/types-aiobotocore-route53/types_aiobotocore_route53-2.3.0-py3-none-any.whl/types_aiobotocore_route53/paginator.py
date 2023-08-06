"""
Type annotations for route53 service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_route53.client import Route53Client
    from types_aiobotocore_route53.paginator import (
        ListHealthChecksPaginator,
        ListHostedZonesPaginator,
        ListQueryLoggingConfigsPaginator,
        ListResourceRecordSetsPaginator,
        ListVPCAssociationAuthorizationsPaginator,
    )

    session = get_session()
    with session.create_client("route53") as client:
        client: Route53Client

        list_health_checks_paginator: ListHealthChecksPaginator = client.get_paginator("list_health_checks")
        list_hosted_zones_paginator: ListHostedZonesPaginator = client.get_paginator("list_hosted_zones")
        list_query_logging_configs_paginator: ListQueryLoggingConfigsPaginator = client.get_paginator("list_query_logging_configs")
        list_resource_record_sets_paginator: ListResourceRecordSetsPaginator = client.get_paginator("list_resource_record_sets")
        list_vpc_association_authorizations_paginator: ListVPCAssociationAuthorizationsPaginator = client.get_paginator("list_vpc_association_authorizations")
    ```
"""
import sys
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListHealthChecksResponseTypeDef,
    ListHostedZonesResponseTypeDef,
    ListQueryLoggingConfigsResponseTypeDef,
    ListResourceRecordSetsResponseTypeDef,
    ListVPCAssociationAuthorizationsResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator


__all__ = (
    "ListHealthChecksPaginator",
    "ListHostedZonesPaginator",
    "ListQueryLoggingConfigsPaginator",
    "ListResourceRecordSetsPaginator",
    "ListVPCAssociationAuthorizationsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListHealthChecksPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Paginator.ListHealthChecks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/paginators/#listhealthcheckspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListHealthChecksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Paginator.ListHealthChecks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/paginators/#listhealthcheckspaginator)
        """


class ListHostedZonesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Paginator.ListHostedZones)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/paginators/#listhostedzonespaginator)
    """

    def paginate(
        self, *, DelegationSetId: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListHostedZonesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Paginator.ListHostedZones.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/paginators/#listhostedzonespaginator)
        """


class ListQueryLoggingConfigsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Paginator.ListQueryLoggingConfigs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/paginators/#listqueryloggingconfigspaginator)
    """

    def paginate(
        self, *, HostedZoneId: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListQueryLoggingConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Paginator.ListQueryLoggingConfigs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/paginators/#listqueryloggingconfigspaginator)
        """


class ListResourceRecordSetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Paginator.ListResourceRecordSets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/paginators/#listresourcerecordsetspaginator)
    """

    def paginate(
        self, *, HostedZoneId: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListResourceRecordSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Paginator.ListResourceRecordSets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/paginators/#listresourcerecordsetspaginator)
        """


class ListVPCAssociationAuthorizationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Paginator.ListVPCAssociationAuthorizations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/paginators/#listvpcassociationauthorizationspaginator)
    """

    def paginate(
        self,
        *,
        HostedZoneId: str,
        MaxResults: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListVPCAssociationAuthorizationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Paginator.ListVPCAssociationAuthorizations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/paginators/#listvpcassociationauthorizationspaginator)
        """
