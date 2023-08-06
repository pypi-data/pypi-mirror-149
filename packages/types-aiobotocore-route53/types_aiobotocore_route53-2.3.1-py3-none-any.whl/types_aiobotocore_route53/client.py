"""
Type annotations for route53 service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_route53.client import Route53Client

    session = get_session()
    async with session.create_client("route53") as client:
        client: Route53Client
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    AccountLimitTypeType,
    HealthCheckRegionType,
    HostedZoneLimitTypeType,
    InsufficientDataHealthStatusType,
    ResettableElementNameType,
    RRTypeType,
    TagResourceTypeType,
    VPCRegionType,
)
from .paginator import (
    ListHealthChecksPaginator,
    ListHostedZonesPaginator,
    ListQueryLoggingConfigsPaginator,
    ListResourceRecordSetsPaginator,
    ListVPCAssociationAuthorizationsPaginator,
)
from .type_defs import (
    ActivateKeySigningKeyResponseTypeDef,
    AlarmIdentifierTypeDef,
    AssociateVPCWithHostedZoneResponseTypeDef,
    ChangeBatchTypeDef,
    ChangeResourceRecordSetsResponseTypeDef,
    CreateHealthCheckResponseTypeDef,
    CreateHostedZoneResponseTypeDef,
    CreateKeySigningKeyResponseTypeDef,
    CreateQueryLoggingConfigResponseTypeDef,
    CreateReusableDelegationSetResponseTypeDef,
    CreateTrafficPolicyInstanceResponseTypeDef,
    CreateTrafficPolicyResponseTypeDef,
    CreateTrafficPolicyVersionResponseTypeDef,
    CreateVPCAssociationAuthorizationResponseTypeDef,
    DeactivateKeySigningKeyResponseTypeDef,
    DeleteHostedZoneResponseTypeDef,
    DeleteKeySigningKeyResponseTypeDef,
    DisableHostedZoneDNSSECResponseTypeDef,
    DisassociateVPCFromHostedZoneResponseTypeDef,
    EnableHostedZoneDNSSECResponseTypeDef,
    GetAccountLimitResponseTypeDef,
    GetChangeResponseTypeDef,
    GetCheckerIpRangesResponseTypeDef,
    GetDNSSECResponseTypeDef,
    GetGeoLocationResponseTypeDef,
    GetHealthCheckCountResponseTypeDef,
    GetHealthCheckLastFailureReasonResponseTypeDef,
    GetHealthCheckResponseTypeDef,
    GetHealthCheckStatusResponseTypeDef,
    GetHostedZoneCountResponseTypeDef,
    GetHostedZoneLimitResponseTypeDef,
    GetHostedZoneResponseTypeDef,
    GetQueryLoggingConfigResponseTypeDef,
    GetReusableDelegationSetLimitResponseTypeDef,
    GetReusableDelegationSetResponseTypeDef,
    GetTrafficPolicyInstanceCountResponseTypeDef,
    GetTrafficPolicyInstanceResponseTypeDef,
    GetTrafficPolicyResponseTypeDef,
    HealthCheckConfigTypeDef,
    HostedZoneConfigTypeDef,
    ListGeoLocationsResponseTypeDef,
    ListHealthChecksResponseTypeDef,
    ListHostedZonesByNameResponseTypeDef,
    ListHostedZonesByVPCResponseTypeDef,
    ListHostedZonesResponseTypeDef,
    ListQueryLoggingConfigsResponseTypeDef,
    ListResourceRecordSetsResponseTypeDef,
    ListReusableDelegationSetsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTagsForResourcesResponseTypeDef,
    ListTrafficPoliciesResponseTypeDef,
    ListTrafficPolicyInstancesByHostedZoneResponseTypeDef,
    ListTrafficPolicyInstancesByPolicyResponseTypeDef,
    ListTrafficPolicyInstancesResponseTypeDef,
    ListTrafficPolicyVersionsResponseTypeDef,
    ListVPCAssociationAuthorizationsResponseTypeDef,
    TagTypeDef,
    TestDNSAnswerResponseTypeDef,
    UpdateHealthCheckResponseTypeDef,
    UpdateHostedZoneCommentResponseTypeDef,
    UpdateTrafficPolicyCommentResponseTypeDef,
    UpdateTrafficPolicyInstanceResponseTypeDef,
    VPCTypeDef,
)
from .waiter import ResourceRecordSetsChangedWaiter

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("Route53Client",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConcurrentModification: Type[BotocoreClientError]
    ConflictingDomainExists: Type[BotocoreClientError]
    ConflictingTypes: Type[BotocoreClientError]
    DNSSECNotFound: Type[BotocoreClientError]
    DelegationSetAlreadyCreated: Type[BotocoreClientError]
    DelegationSetAlreadyReusable: Type[BotocoreClientError]
    DelegationSetInUse: Type[BotocoreClientError]
    DelegationSetNotAvailable: Type[BotocoreClientError]
    DelegationSetNotReusable: Type[BotocoreClientError]
    HealthCheckAlreadyExists: Type[BotocoreClientError]
    HealthCheckInUse: Type[BotocoreClientError]
    HealthCheckVersionMismatch: Type[BotocoreClientError]
    HostedZoneAlreadyExists: Type[BotocoreClientError]
    HostedZoneNotEmpty: Type[BotocoreClientError]
    HostedZoneNotFound: Type[BotocoreClientError]
    HostedZoneNotPrivate: Type[BotocoreClientError]
    HostedZonePartiallyDelegated: Type[BotocoreClientError]
    IncompatibleVersion: Type[BotocoreClientError]
    InsufficientCloudWatchLogsResourcePolicy: Type[BotocoreClientError]
    InvalidArgument: Type[BotocoreClientError]
    InvalidChangeBatch: Type[BotocoreClientError]
    InvalidDomainName: Type[BotocoreClientError]
    InvalidInput: Type[BotocoreClientError]
    InvalidKMSArn: Type[BotocoreClientError]
    InvalidKeySigningKeyName: Type[BotocoreClientError]
    InvalidKeySigningKeyStatus: Type[BotocoreClientError]
    InvalidPaginationToken: Type[BotocoreClientError]
    InvalidSigningStatus: Type[BotocoreClientError]
    InvalidTrafficPolicyDocument: Type[BotocoreClientError]
    InvalidVPCId: Type[BotocoreClientError]
    KeySigningKeyAlreadyExists: Type[BotocoreClientError]
    KeySigningKeyInParentDSRecord: Type[BotocoreClientError]
    KeySigningKeyInUse: Type[BotocoreClientError]
    KeySigningKeyWithActiveStatusNotFound: Type[BotocoreClientError]
    LastVPCAssociation: Type[BotocoreClientError]
    LimitsExceeded: Type[BotocoreClientError]
    NoSuchChange: Type[BotocoreClientError]
    NoSuchCloudWatchLogsLogGroup: Type[BotocoreClientError]
    NoSuchDelegationSet: Type[BotocoreClientError]
    NoSuchGeoLocation: Type[BotocoreClientError]
    NoSuchHealthCheck: Type[BotocoreClientError]
    NoSuchHostedZone: Type[BotocoreClientError]
    NoSuchKeySigningKey: Type[BotocoreClientError]
    NoSuchQueryLoggingConfig: Type[BotocoreClientError]
    NoSuchTrafficPolicy: Type[BotocoreClientError]
    NoSuchTrafficPolicyInstance: Type[BotocoreClientError]
    NotAuthorizedException: Type[BotocoreClientError]
    PriorRequestNotComplete: Type[BotocoreClientError]
    PublicZoneVPCAssociation: Type[BotocoreClientError]
    QueryLoggingConfigAlreadyExists: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TooManyHealthChecks: Type[BotocoreClientError]
    TooManyHostedZones: Type[BotocoreClientError]
    TooManyKeySigningKeys: Type[BotocoreClientError]
    TooManyTrafficPolicies: Type[BotocoreClientError]
    TooManyTrafficPolicyInstances: Type[BotocoreClientError]
    TooManyTrafficPolicyVersionsForCurrentPolicy: Type[BotocoreClientError]
    TooManyVPCAssociationAuthorizations: Type[BotocoreClientError]
    TrafficPolicyAlreadyExists: Type[BotocoreClientError]
    TrafficPolicyInUse: Type[BotocoreClientError]
    TrafficPolicyInstanceAlreadyExists: Type[BotocoreClientError]
    VPCAssociationAuthorizationNotFound: Type[BotocoreClientError]
    VPCAssociationNotFound: Type[BotocoreClientError]


class Route53Client(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        Route53Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#exceptions)
        """

    async def activate_key_signing_key(
        self, *, HostedZoneId: str, Name: str
    ) -> ActivateKeySigningKeyResponseTypeDef:
        """
        Activates a key-signing key (KSK) so that it can be used for signing by DNSSEC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.activate_key_signing_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#activate_key_signing_key)
        """

    async def associate_vpc_with_hosted_zone(
        self, *, HostedZoneId: str, VPC: "VPCTypeDef", Comment: str = ...
    ) -> AssociateVPCWithHostedZoneResponseTypeDef:
        """
        Associates an Amazon VPC with a private hosted zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.associate_vpc_with_hosted_zone)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#associate_vpc_with_hosted_zone)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#can_paginate)
        """

    async def change_resource_record_sets(
        self, *, HostedZoneId: str, ChangeBatch: "ChangeBatchTypeDef"
    ) -> ChangeResourceRecordSetsResponseTypeDef:
        """
        Creates, changes, or deletes a resource record set, which contains authoritative
        DNS information for a specified domain name or subdomain name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.change_resource_record_sets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#change_resource_record_sets)
        """

    async def change_tags_for_resource(
        self,
        *,
        ResourceType: TagResourceTypeType,
        ResourceId: str,
        AddTags: Sequence["TagTypeDef"] = ...,
        RemoveTagKeys: Sequence[str] = ...
    ) -> Dict[str, Any]:
        """
        Adds, edits, or deletes tags for a health check or a hosted zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.change_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#change_tags_for_resource)
        """

    async def create_health_check(
        self, *, CallerReference: str, HealthCheckConfig: "HealthCheckConfigTypeDef"
    ) -> CreateHealthCheckResponseTypeDef:
        """
        Creates a new health check.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.create_health_check)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#create_health_check)
        """

    async def create_hosted_zone(
        self,
        *,
        Name: str,
        CallerReference: str,
        VPC: "VPCTypeDef" = ...,
        HostedZoneConfig: "HostedZoneConfigTypeDef" = ...,
        DelegationSetId: str = ...
    ) -> CreateHostedZoneResponseTypeDef:
        """
        Creates a new public or private hosted zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.create_hosted_zone)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#create_hosted_zone)
        """

    async def create_key_signing_key(
        self,
        *,
        CallerReference: str,
        HostedZoneId: str,
        KeyManagementServiceArn: str,
        Name: str,
        Status: str
    ) -> CreateKeySigningKeyResponseTypeDef:
        """
        Creates a new key-signing key (KSK) associated with a hosted zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.create_key_signing_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#create_key_signing_key)
        """

    async def create_query_logging_config(
        self, *, HostedZoneId: str, CloudWatchLogsLogGroupArn: str
    ) -> CreateQueryLoggingConfigResponseTypeDef:
        """
        Creates a configuration for DNS query logging.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.create_query_logging_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#create_query_logging_config)
        """

    async def create_reusable_delegation_set(
        self, *, CallerReference: str, HostedZoneId: str = ...
    ) -> CreateReusableDelegationSetResponseTypeDef:
        """
        Creates a delegation set (a group of four name servers) that can be reused by
        multiple hosted zones that were created by the same Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.create_reusable_delegation_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#create_reusable_delegation_set)
        """

    async def create_traffic_policy(
        self, *, Name: str, Document: str, Comment: str = ...
    ) -> CreateTrafficPolicyResponseTypeDef:
        """
        Creates a traffic policy, which you use to create multiple DNS resource record
        sets for one domain name (such as example.com) or one subdomain name (such as
        www.example.com).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.create_traffic_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#create_traffic_policy)
        """

    async def create_traffic_policy_instance(
        self,
        *,
        HostedZoneId: str,
        Name: str,
        TTL: int,
        TrafficPolicyId: str,
        TrafficPolicyVersion: int
    ) -> CreateTrafficPolicyInstanceResponseTypeDef:
        """
        Creates resource record sets in a specified hosted zone based on the settings in
        a specified traffic policy version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.create_traffic_policy_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#create_traffic_policy_instance)
        """

    async def create_traffic_policy_version(
        self, *, Id: str, Document: str, Comment: str = ...
    ) -> CreateTrafficPolicyVersionResponseTypeDef:
        """
        Creates a new version of an existing traffic policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.create_traffic_policy_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#create_traffic_policy_version)
        """

    async def create_vpc_association_authorization(
        self, *, HostedZoneId: str, VPC: "VPCTypeDef"
    ) -> CreateVPCAssociationAuthorizationResponseTypeDef:
        """
        Authorizes the Amazon Web Services account that created a specified VPC to
        submit an `AssociateVPCWithHostedZone` request to associate the VPC with a
        specified hosted zone that was created by a different account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.create_vpc_association_authorization)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#create_vpc_association_authorization)
        """

    async def deactivate_key_signing_key(
        self, *, HostedZoneId: str, Name: str
    ) -> DeactivateKeySigningKeyResponseTypeDef:
        """
        Deactivates a key-signing key (KSK) so that it will not be used for signing by
        DNSSEC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.deactivate_key_signing_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#deactivate_key_signing_key)
        """

    async def delete_health_check(self, *, HealthCheckId: str) -> Dict[str, Any]:
        """
        Deletes a health check.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.delete_health_check)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#delete_health_check)
        """

    async def delete_hosted_zone(self, *, Id: str) -> DeleteHostedZoneResponseTypeDef:
        """
        Deletes a hosted zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.delete_hosted_zone)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#delete_hosted_zone)
        """

    async def delete_key_signing_key(
        self, *, HostedZoneId: str, Name: str
    ) -> DeleteKeySigningKeyResponseTypeDef:
        """
        Deletes a key-signing key (KSK).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.delete_key_signing_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#delete_key_signing_key)
        """

    async def delete_query_logging_config(self, *, Id: str) -> Dict[str, Any]:
        """
        Deletes a configuration for DNS query logging.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.delete_query_logging_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#delete_query_logging_config)
        """

    async def delete_reusable_delegation_set(self, *, Id: str) -> Dict[str, Any]:
        """
        Deletes a reusable delegation set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.delete_reusable_delegation_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#delete_reusable_delegation_set)
        """

    async def delete_traffic_policy(self, *, Id: str, Version: int) -> Dict[str, Any]:
        """
        Deletes a traffic policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.delete_traffic_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#delete_traffic_policy)
        """

    async def delete_traffic_policy_instance(self, *, Id: str) -> Dict[str, Any]:
        """
        Deletes a traffic policy instance and all of the resource record sets that
        Amazon Route 53 created when you created the instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.delete_traffic_policy_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#delete_traffic_policy_instance)
        """

    async def delete_vpc_association_authorization(
        self, *, HostedZoneId: str, VPC: "VPCTypeDef"
    ) -> Dict[str, Any]:
        """
        Removes authorization to submit an `AssociateVPCWithHostedZone` request to
        associate a specified VPC with a hosted zone that was created by a different
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.delete_vpc_association_authorization)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#delete_vpc_association_authorization)
        """

    async def disable_hosted_zone_dnssec(
        self, *, HostedZoneId: str
    ) -> DisableHostedZoneDNSSECResponseTypeDef:
        """
        Disables DNSSEC signing in a specific hosted zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.disable_hosted_zone_dnssec)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#disable_hosted_zone_dnssec)
        """

    async def disassociate_vpc_from_hosted_zone(
        self, *, HostedZoneId: str, VPC: "VPCTypeDef", Comment: str = ...
    ) -> DisassociateVPCFromHostedZoneResponseTypeDef:
        """
        Disassociates an Amazon Virtual Private Cloud (Amazon VPC) from an Amazon Route
        53 private hosted zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.disassociate_vpc_from_hosted_zone)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#disassociate_vpc_from_hosted_zone)
        """

    async def enable_hosted_zone_dnssec(
        self, *, HostedZoneId: str
    ) -> EnableHostedZoneDNSSECResponseTypeDef:
        """
        Enables DNSSEC signing in a specific hosted zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.enable_hosted_zone_dnssec)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#enable_hosted_zone_dnssec)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#generate_presigned_url)
        """

    async def get_account_limit(
        self, *, Type: AccountLimitTypeType
    ) -> GetAccountLimitResponseTypeDef:
        """
        Gets the specified limit for the current account, for example, the maximum
        number of health checks that you can create using the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.get_account_limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_account_limit)
        """

    async def get_change(self, *, Id: str) -> GetChangeResponseTypeDef:
        """
        Returns the current status of a change batch request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.get_change)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_change)
        """

    async def get_checker_ip_ranges(self) -> GetCheckerIpRangesResponseTypeDef:
        """
        Route 53 does not perform authorization for this API because it retrieves
        information that is already available to the public.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.get_checker_ip_ranges)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_checker_ip_ranges)
        """

    async def get_dnssec(self, *, HostedZoneId: str) -> GetDNSSECResponseTypeDef:
        """
        Returns information about DNSSEC for a specific hosted zone, including the key-
        signing keys (KSKs) in the hosted zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.get_dnssec)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_dnssec)
        """

    async def get_geo_location(
        self, *, ContinentCode: str = ..., CountryCode: str = ..., SubdivisionCode: str = ...
    ) -> GetGeoLocationResponseTypeDef:
        """
        Gets information about whether a specified geographic location is supported for
        Amazon Route 53 geolocation resource record sets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.get_geo_location)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_geo_location)
        """

    async def get_health_check(self, *, HealthCheckId: str) -> GetHealthCheckResponseTypeDef:
        """
        Gets information about a specified health check.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.get_health_check)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_health_check)
        """

    async def get_health_check_count(self) -> GetHealthCheckCountResponseTypeDef:
        """
        Retrieves the number of health checks that are associated with the current
        Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.get_health_check_count)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_health_check_count)
        """

    async def get_health_check_last_failure_reason(
        self, *, HealthCheckId: str
    ) -> GetHealthCheckLastFailureReasonResponseTypeDef:
        """
        Gets the reason that a specified health check failed most recently.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.get_health_check_last_failure_reason)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_health_check_last_failure_reason)
        """

    async def get_health_check_status(
        self, *, HealthCheckId: str
    ) -> GetHealthCheckStatusResponseTypeDef:
        """
        Gets status of a specified health check.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.get_health_check_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_health_check_status)
        """

    async def get_hosted_zone(self, *, Id: str) -> GetHostedZoneResponseTypeDef:
        """
        Gets information about a specified hosted zone including the four name servers
        assigned to the hosted zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.get_hosted_zone)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_hosted_zone)
        """

    async def get_hosted_zone_count(self) -> GetHostedZoneCountResponseTypeDef:
        """
        Retrieves the number of hosted zones that are associated with the current Amazon
        Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.get_hosted_zone_count)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_hosted_zone_count)
        """

    async def get_hosted_zone_limit(
        self, *, Type: HostedZoneLimitTypeType, HostedZoneId: str
    ) -> GetHostedZoneLimitResponseTypeDef:
        """
        Gets the specified limit for a specified hosted zone, for example, the maximum
        number of records that you can create in the hosted zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.get_hosted_zone_limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_hosted_zone_limit)
        """

    async def get_query_logging_config(self, *, Id: str) -> GetQueryLoggingConfigResponseTypeDef:
        """
        Gets information about a specified configuration for DNS query logging.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.get_query_logging_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_query_logging_config)
        """

    async def get_reusable_delegation_set(
        self, *, Id: str
    ) -> GetReusableDelegationSetResponseTypeDef:
        """
        Retrieves information about a specified reusable delegation set, including the
        four name servers that are assigned to the delegation set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.get_reusable_delegation_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_reusable_delegation_set)
        """

    async def get_reusable_delegation_set_limit(
        self, *, Type: Literal["MAX_ZONES_BY_REUSABLE_DELEGATION_SET"], DelegationSetId: str
    ) -> GetReusableDelegationSetLimitResponseTypeDef:
        """
        Gets the maximum number of hosted zones that you can associate with the
        specified reusable delegation set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.get_reusable_delegation_set_limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_reusable_delegation_set_limit)
        """

    async def get_traffic_policy(self, *, Id: str, Version: int) -> GetTrafficPolicyResponseTypeDef:
        """
        Gets information about a specific traffic policy version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.get_traffic_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_traffic_policy)
        """

    async def get_traffic_policy_instance(
        self, *, Id: str
    ) -> GetTrafficPolicyInstanceResponseTypeDef:
        """
        Gets information about a specified traffic policy instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.get_traffic_policy_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_traffic_policy_instance)
        """

    async def get_traffic_policy_instance_count(
        self,
    ) -> GetTrafficPolicyInstanceCountResponseTypeDef:
        """
        Gets the number of traffic policy instances that are associated with the current
        Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.get_traffic_policy_instance_count)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_traffic_policy_instance_count)
        """

    async def list_geo_locations(
        self,
        *,
        StartContinentCode: str = ...,
        StartCountryCode: str = ...,
        StartSubdivisionCode: str = ...,
        MaxItems: str = ...
    ) -> ListGeoLocationsResponseTypeDef:
        """
        Retrieves a list of supported geographic locations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.list_geo_locations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_geo_locations)
        """

    async def list_health_checks(
        self, *, Marker: str = ..., MaxItems: str = ...
    ) -> ListHealthChecksResponseTypeDef:
        """
        Retrieve a list of the health checks that are associated with the current Amazon
        Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.list_health_checks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_health_checks)
        """

    async def list_hosted_zones(
        self, *, Marker: str = ..., MaxItems: str = ..., DelegationSetId: str = ...
    ) -> ListHostedZonesResponseTypeDef:
        """
        Retrieves a list of the public and private hosted zones that are associated with
        the current Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.list_hosted_zones)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_hosted_zones)
        """

    async def list_hosted_zones_by_name(
        self, *, DNSName: str = ..., HostedZoneId: str = ..., MaxItems: str = ...
    ) -> ListHostedZonesByNameResponseTypeDef:
        """
        Retrieves a list of your hosted zones in lexicographic order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.list_hosted_zones_by_name)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_hosted_zones_by_name)
        """

    async def list_hosted_zones_by_vpc(
        self, *, VPCId: str, VPCRegion: VPCRegionType, MaxItems: str = ..., NextToken: str = ...
    ) -> ListHostedZonesByVPCResponseTypeDef:
        """
        Lists all the private hosted zones that a specified VPC is associated with,
        regardless of which Amazon Web Services account or Amazon Web Services service
        owns the hosted zones.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.list_hosted_zones_by_vpc)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_hosted_zones_by_vpc)
        """

    async def list_query_logging_configs(
        self, *, HostedZoneId: str = ..., NextToken: str = ..., MaxResults: str = ...
    ) -> ListQueryLoggingConfigsResponseTypeDef:
        """
        Lists the configurations for DNS query logging that are associated with the
        current Amazon Web Services account or the configuration that is associated with
        a specified hosted zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.list_query_logging_configs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_query_logging_configs)
        """

    async def list_resource_record_sets(
        self,
        *,
        HostedZoneId: str,
        StartRecordName: str = ...,
        StartRecordType: RRTypeType = ...,
        StartRecordIdentifier: str = ...,
        MaxItems: str = ...
    ) -> ListResourceRecordSetsResponseTypeDef:
        """
        Lists the resource record sets in a specified hosted zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.list_resource_record_sets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_resource_record_sets)
        """

    async def list_reusable_delegation_sets(
        self, *, Marker: str = ..., MaxItems: str = ...
    ) -> ListReusableDelegationSetsResponseTypeDef:
        """
        Retrieves a list of the reusable delegation sets that are associated with the
        current Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.list_reusable_delegation_sets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_reusable_delegation_sets)
        """

    async def list_tags_for_resource(
        self, *, ResourceType: TagResourceTypeType, ResourceId: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists tags for one health check or hosted zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_tags_for_resource)
        """

    async def list_tags_for_resources(
        self, *, ResourceType: TagResourceTypeType, ResourceIds: Sequence[str]
    ) -> ListTagsForResourcesResponseTypeDef:
        """
        Lists tags for up to 10 health checks or hosted zones.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.list_tags_for_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_tags_for_resources)
        """

    async def list_traffic_policies(
        self, *, TrafficPolicyIdMarker: str = ..., MaxItems: str = ...
    ) -> ListTrafficPoliciesResponseTypeDef:
        """
        Gets information about the latest version for every traffic policy that is
        associated with the current Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.list_traffic_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_traffic_policies)
        """

    async def list_traffic_policy_instances(
        self,
        *,
        HostedZoneIdMarker: str = ...,
        TrafficPolicyInstanceNameMarker: str = ...,
        TrafficPolicyInstanceTypeMarker: RRTypeType = ...,
        MaxItems: str = ...
    ) -> ListTrafficPolicyInstancesResponseTypeDef:
        """
        Gets information about the traffic policy instances that you created by using
        the current Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.list_traffic_policy_instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_traffic_policy_instances)
        """

    async def list_traffic_policy_instances_by_hosted_zone(
        self,
        *,
        HostedZoneId: str,
        TrafficPolicyInstanceNameMarker: str = ...,
        TrafficPolicyInstanceTypeMarker: RRTypeType = ...,
        MaxItems: str = ...
    ) -> ListTrafficPolicyInstancesByHostedZoneResponseTypeDef:
        """
        Gets information about the traffic policy instances that you created in a
        specified hosted zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.list_traffic_policy_instances_by_hosted_zone)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_traffic_policy_instances_by_hosted_zone)
        """

    async def list_traffic_policy_instances_by_policy(
        self,
        *,
        TrafficPolicyId: str,
        TrafficPolicyVersion: int,
        HostedZoneIdMarker: str = ...,
        TrafficPolicyInstanceNameMarker: str = ...,
        TrafficPolicyInstanceTypeMarker: RRTypeType = ...,
        MaxItems: str = ...
    ) -> ListTrafficPolicyInstancesByPolicyResponseTypeDef:
        """
        Gets information about the traffic policy instances that you created by using a
        specify traffic policy version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.list_traffic_policy_instances_by_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_traffic_policy_instances_by_policy)
        """

    async def list_traffic_policy_versions(
        self, *, Id: str, TrafficPolicyVersionMarker: str = ..., MaxItems: str = ...
    ) -> ListTrafficPolicyVersionsResponseTypeDef:
        """
        Gets information about all of the versions for a specified traffic policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.list_traffic_policy_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_traffic_policy_versions)
        """

    async def list_vpc_association_authorizations(
        self, *, HostedZoneId: str, NextToken: str = ..., MaxResults: str = ...
    ) -> ListVPCAssociationAuthorizationsResponseTypeDef:
        """
        Gets a list of the VPCs that were created by other accounts and that can be
        associated with a specified hosted zone because you've submitted one or more
        `CreateVPCAssociationAuthorization` requests.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.list_vpc_association_authorizations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#list_vpc_association_authorizations)
        """

    async def test_dns_answer(
        self,
        *,
        HostedZoneId: str,
        RecordName: str,
        RecordType: RRTypeType,
        ResolverIP: str = ...,
        EDNS0ClientSubnetIP: str = ...,
        EDNS0ClientSubnetMask: str = ...
    ) -> TestDNSAnswerResponseTypeDef:
        """
        Gets the value that Amazon Route 53 returns in response to a DNS request for a
        specified record name and type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.test_dns_answer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#test_dns_answer)
        """

    async def update_health_check(
        self,
        *,
        HealthCheckId: str,
        HealthCheckVersion: int = ...,
        IPAddress: str = ...,
        Port: int = ...,
        ResourcePath: str = ...,
        FullyQualifiedDomainName: str = ...,
        SearchString: str = ...,
        FailureThreshold: int = ...,
        Inverted: bool = ...,
        Disabled: bool = ...,
        HealthThreshold: int = ...,
        ChildHealthChecks: Sequence[str] = ...,
        EnableSNI: bool = ...,
        Regions: Sequence[HealthCheckRegionType] = ...,
        AlarmIdentifier: "AlarmIdentifierTypeDef" = ...,
        InsufficientDataHealthStatus: InsufficientDataHealthStatusType = ...,
        ResetElements: Sequence[ResettableElementNameType] = ...
    ) -> UpdateHealthCheckResponseTypeDef:
        """
        Updates an existing health check.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.update_health_check)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#update_health_check)
        """

    async def update_hosted_zone_comment(
        self, *, Id: str, Comment: str = ...
    ) -> UpdateHostedZoneCommentResponseTypeDef:
        """
        Updates the comment for a specified hosted zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.update_hosted_zone_comment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#update_hosted_zone_comment)
        """

    async def update_traffic_policy_comment(
        self, *, Id: str, Version: int, Comment: str
    ) -> UpdateTrafficPolicyCommentResponseTypeDef:
        """
        Updates the comment for a specified traffic policy version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.update_traffic_policy_comment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#update_traffic_policy_comment)
        """

    async def update_traffic_policy_instance(
        self, *, Id: str, TTL: int, TrafficPolicyId: str, TrafficPolicyVersion: int
    ) -> UpdateTrafficPolicyInstanceResponseTypeDef:
        """
        Updates the resource record sets in a specified hosted zone that were created
        based on the settings in a specified traffic policy version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.update_traffic_policy_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#update_traffic_policy_instance)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_health_checks"]
    ) -> ListHealthChecksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_hosted_zones"]
    ) -> ListHostedZonesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_query_logging_configs"]
    ) -> ListQueryLoggingConfigsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_record_sets"]
    ) -> ListResourceRecordSetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_vpc_association_authorizations"]
    ) -> ListVPCAssociationAuthorizationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_paginator)
        """

    def get_waiter(
        self, waiter_name: Literal["resource_record_sets_changed"]
    ) -> ResourceRecordSetsChangedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/#get_waiter)
        """

    async def __aenter__(self) -> "Route53Client":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53.html#Route53.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/client/)
        """
