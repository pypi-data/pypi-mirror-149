"""
Main interface for route53 service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_route53 import (
        Client,
        ListHealthChecksPaginator,
        ListHostedZonesPaginator,
        ListQueryLoggingConfigsPaginator,
        ListResourceRecordSetsPaginator,
        ListVPCAssociationAuthorizationsPaginator,
        ResourceRecordSetsChangedWaiter,
        Route53Client,
    )

    session = get_session()
    async with session.create_client("route53") as client:
        client: Route53Client
        ...


    resource_record_sets_changed_waiter: ResourceRecordSetsChangedWaiter = client.get_waiter("resource_record_sets_changed")

    list_health_checks_paginator: ListHealthChecksPaginator = client.get_paginator("list_health_checks")
    list_hosted_zones_paginator: ListHostedZonesPaginator = client.get_paginator("list_hosted_zones")
    list_query_logging_configs_paginator: ListQueryLoggingConfigsPaginator = client.get_paginator("list_query_logging_configs")
    list_resource_record_sets_paginator: ListResourceRecordSetsPaginator = client.get_paginator("list_resource_record_sets")
    list_vpc_association_authorizations_paginator: ListVPCAssociationAuthorizationsPaginator = client.get_paginator("list_vpc_association_authorizations")
    ```
"""
from .client import Route53Client
from .paginator import (
    ListHealthChecksPaginator,
    ListHostedZonesPaginator,
    ListQueryLoggingConfigsPaginator,
    ListResourceRecordSetsPaginator,
    ListVPCAssociationAuthorizationsPaginator,
)
from .waiter import ResourceRecordSetsChangedWaiter

Client = Route53Client

__all__ = (
    "Client",
    "ListHealthChecksPaginator",
    "ListHostedZonesPaginator",
    "ListQueryLoggingConfigsPaginator",
    "ListResourceRecordSetsPaginator",
    "ListVPCAssociationAuthorizationsPaginator",
    "ResourceRecordSetsChangedWaiter",
    "Route53Client",
)
