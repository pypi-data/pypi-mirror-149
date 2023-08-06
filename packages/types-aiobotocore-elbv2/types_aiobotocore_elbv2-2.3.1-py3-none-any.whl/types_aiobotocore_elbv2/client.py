"""
Type annotations for elbv2 service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_elbv2.client import ElasticLoadBalancingv2Client

    session = get_session()
    async with session.create_client("elbv2") as client:
        client: ElasticLoadBalancingv2Client
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    IpAddressTypeType,
    LoadBalancerSchemeEnumType,
    LoadBalancerTypeEnumType,
    ProtocolEnumType,
    TargetGroupIpAddressTypeEnumType,
    TargetTypeEnumType,
)
from .paginator import (
    DescribeAccountLimitsPaginator,
    DescribeListenerCertificatesPaginator,
    DescribeListenersPaginator,
    DescribeLoadBalancersPaginator,
    DescribeRulesPaginator,
    DescribeSSLPoliciesPaginator,
    DescribeTargetGroupsPaginator,
)
from .type_defs import (
    ActionTypeDef,
    AddListenerCertificatesOutputTypeDef,
    CertificateTypeDef,
    CreateListenerOutputTypeDef,
    CreateLoadBalancerOutputTypeDef,
    CreateRuleOutputTypeDef,
    CreateTargetGroupOutputTypeDef,
    DescribeAccountLimitsOutputTypeDef,
    DescribeListenerCertificatesOutputTypeDef,
    DescribeListenersOutputTypeDef,
    DescribeLoadBalancerAttributesOutputTypeDef,
    DescribeLoadBalancersOutputTypeDef,
    DescribeRulesOutputTypeDef,
    DescribeSSLPoliciesOutputTypeDef,
    DescribeTagsOutputTypeDef,
    DescribeTargetGroupAttributesOutputTypeDef,
    DescribeTargetGroupsOutputTypeDef,
    DescribeTargetHealthOutputTypeDef,
    LoadBalancerAttributeTypeDef,
    MatcherTypeDef,
    ModifyListenerOutputTypeDef,
    ModifyLoadBalancerAttributesOutputTypeDef,
    ModifyRuleOutputTypeDef,
    ModifyTargetGroupAttributesOutputTypeDef,
    ModifyTargetGroupOutputTypeDef,
    RuleConditionTypeDef,
    RulePriorityPairTypeDef,
    SetIpAddressTypeOutputTypeDef,
    SetRulePrioritiesOutputTypeDef,
    SetSecurityGroupsOutputTypeDef,
    SetSubnetsOutputTypeDef,
    SubnetMappingTypeDef,
    TagTypeDef,
    TargetDescriptionTypeDef,
    TargetGroupAttributeTypeDef,
)
from .waiter import (
    LoadBalancerAvailableWaiter,
    LoadBalancerExistsWaiter,
    LoadBalancersDeletedWaiter,
    TargetDeregisteredWaiter,
    TargetInServiceWaiter,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ElasticLoadBalancingv2Client",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ALPNPolicyNotSupportedException: Type[BotocoreClientError]
    AllocationIdNotFoundException: Type[BotocoreClientError]
    AvailabilityZoneNotSupportedException: Type[BotocoreClientError]
    CertificateNotFoundException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DuplicateListenerException: Type[BotocoreClientError]
    DuplicateLoadBalancerNameException: Type[BotocoreClientError]
    DuplicateTagKeysException: Type[BotocoreClientError]
    DuplicateTargetGroupNameException: Type[BotocoreClientError]
    HealthUnavailableException: Type[BotocoreClientError]
    IncompatibleProtocolsException: Type[BotocoreClientError]
    InvalidConfigurationRequestException: Type[BotocoreClientError]
    InvalidLoadBalancerActionException: Type[BotocoreClientError]
    InvalidSchemeException: Type[BotocoreClientError]
    InvalidSecurityGroupException: Type[BotocoreClientError]
    InvalidSubnetException: Type[BotocoreClientError]
    InvalidTargetException: Type[BotocoreClientError]
    ListenerNotFoundException: Type[BotocoreClientError]
    LoadBalancerNotFoundException: Type[BotocoreClientError]
    OperationNotPermittedException: Type[BotocoreClientError]
    PriorityInUseException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    RuleNotFoundException: Type[BotocoreClientError]
    SSLPolicyNotFoundException: Type[BotocoreClientError]
    SubnetNotFoundException: Type[BotocoreClientError]
    TargetGroupAssociationLimitException: Type[BotocoreClientError]
    TargetGroupNotFoundException: Type[BotocoreClientError]
    TooManyActionsException: Type[BotocoreClientError]
    TooManyCertificatesException: Type[BotocoreClientError]
    TooManyListenersException: Type[BotocoreClientError]
    TooManyLoadBalancersException: Type[BotocoreClientError]
    TooManyRegistrationsForTargetIdException: Type[BotocoreClientError]
    TooManyRulesException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    TooManyTargetGroupsException: Type[BotocoreClientError]
    TooManyTargetsException: Type[BotocoreClientError]
    TooManyUniqueTargetGroupsPerLoadBalancerException: Type[BotocoreClientError]
    UnsupportedProtocolException: Type[BotocoreClientError]


class ElasticLoadBalancingv2Client(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ElasticLoadBalancingv2Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#exceptions)
        """

    async def add_listener_certificates(
        self, *, ListenerArn: str, Certificates: Sequence["CertificateTypeDef"]
    ) -> AddListenerCertificatesOutputTypeDef:
        """
        Adds the specified SSL server certificate to the certificate list for the
        specified HTTPS or TLS listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.add_listener_certificates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#add_listener_certificates)
        """

    async def add_tags(
        self, *, ResourceArns: Sequence[str], Tags: Sequence["TagTypeDef"]
    ) -> Dict[str, Any]:
        """
        Adds the specified tags to the specified Elastic Load Balancing resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.add_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#add_tags)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#can_paginate)
        """

    async def create_listener(
        self,
        *,
        LoadBalancerArn: str,
        DefaultActions: Sequence["ActionTypeDef"],
        Protocol: ProtocolEnumType = ...,
        Port: int = ...,
        SslPolicy: str = ...,
        Certificates: Sequence["CertificateTypeDef"] = ...,
        AlpnPolicy: Sequence[str] = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateListenerOutputTypeDef:
        """
        Creates a listener for the specified Application Load Balancer, Network Load
        Balancer, or Gateway Load Balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.create_listener)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#create_listener)
        """

    async def create_load_balancer(
        self,
        *,
        Name: str,
        Subnets: Sequence[str] = ...,
        SubnetMappings: Sequence["SubnetMappingTypeDef"] = ...,
        SecurityGroups: Sequence[str] = ...,
        Scheme: LoadBalancerSchemeEnumType = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        Type: LoadBalancerTypeEnumType = ...,
        IpAddressType: IpAddressTypeType = ...,
        CustomerOwnedIpv4Pool: str = ...
    ) -> CreateLoadBalancerOutputTypeDef:
        """
        Creates an Application Load Balancer, Network Load Balancer, or Gateway Load
        Balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.create_load_balancer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#create_load_balancer)
        """

    async def create_rule(
        self,
        *,
        ListenerArn: str,
        Conditions: Sequence["RuleConditionTypeDef"],
        Priority: int,
        Actions: Sequence["ActionTypeDef"],
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateRuleOutputTypeDef:
        """
        Creates a rule for the specified listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.create_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#create_rule)
        """

    async def create_target_group(
        self,
        *,
        Name: str,
        Protocol: ProtocolEnumType = ...,
        ProtocolVersion: str = ...,
        Port: int = ...,
        VpcId: str = ...,
        HealthCheckProtocol: ProtocolEnumType = ...,
        HealthCheckPort: str = ...,
        HealthCheckEnabled: bool = ...,
        HealthCheckPath: str = ...,
        HealthCheckIntervalSeconds: int = ...,
        HealthCheckTimeoutSeconds: int = ...,
        HealthyThresholdCount: int = ...,
        UnhealthyThresholdCount: int = ...,
        Matcher: "MatcherTypeDef" = ...,
        TargetType: TargetTypeEnumType = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        IpAddressType: TargetGroupIpAddressTypeEnumType = ...
    ) -> CreateTargetGroupOutputTypeDef:
        """
        Creates a target group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.create_target_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#create_target_group)
        """

    async def delete_listener(self, *, ListenerArn: str) -> Dict[str, Any]:
        """
        Deletes the specified listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.delete_listener)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#delete_listener)
        """

    async def delete_load_balancer(self, *, LoadBalancerArn: str) -> Dict[str, Any]:
        """
        Deletes the specified Application Load Balancer, Network Load Balancer, or
        Gateway Load Balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.delete_load_balancer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#delete_load_balancer)
        """

    async def delete_rule(self, *, RuleArn: str) -> Dict[str, Any]:
        """
        Deletes the specified rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.delete_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#delete_rule)
        """

    async def delete_target_group(self, *, TargetGroupArn: str) -> Dict[str, Any]:
        """
        Deletes the specified target group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.delete_target_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#delete_target_group)
        """

    async def deregister_targets(
        self, *, TargetGroupArn: str, Targets: Sequence["TargetDescriptionTypeDef"]
    ) -> Dict[str, Any]:
        """
        Deregisters the specified targets from the specified target group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.deregister_targets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#deregister_targets)
        """

    async def describe_account_limits(
        self, *, Marker: str = ..., PageSize: int = ...
    ) -> DescribeAccountLimitsOutputTypeDef:
        """
        Describes the current Elastic Load Balancing resource limits for your Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.describe_account_limits)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#describe_account_limits)
        """

    async def describe_listener_certificates(
        self, *, ListenerArn: str, Marker: str = ..., PageSize: int = ...
    ) -> DescribeListenerCertificatesOutputTypeDef:
        """
        Describes the default certificate and the certificate list for the specified
        HTTPS or TLS listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.describe_listener_certificates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#describe_listener_certificates)
        """

    async def describe_listeners(
        self,
        *,
        LoadBalancerArn: str = ...,
        ListenerArns: Sequence[str] = ...,
        Marker: str = ...,
        PageSize: int = ...
    ) -> DescribeListenersOutputTypeDef:
        """
        Describes the specified listeners or the listeners for the specified Application
        Load Balancer, Network Load Balancer, or Gateway Load Balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.describe_listeners)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#describe_listeners)
        """

    async def describe_load_balancer_attributes(
        self, *, LoadBalancerArn: str
    ) -> DescribeLoadBalancerAttributesOutputTypeDef:
        """
        Describes the attributes for the specified Application Load Balancer, Network
        Load Balancer, or Gateway Load Balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.describe_load_balancer_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#describe_load_balancer_attributes)
        """

    async def describe_load_balancers(
        self,
        *,
        LoadBalancerArns: Sequence[str] = ...,
        Names: Sequence[str] = ...,
        Marker: str = ...,
        PageSize: int = ...
    ) -> DescribeLoadBalancersOutputTypeDef:
        """
        Describes the specified load balancers or all of your load balancers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.describe_load_balancers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#describe_load_balancers)
        """

    async def describe_rules(
        self,
        *,
        ListenerArn: str = ...,
        RuleArns: Sequence[str] = ...,
        Marker: str = ...,
        PageSize: int = ...
    ) -> DescribeRulesOutputTypeDef:
        """
        Describes the specified rules or the rules for the specified listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.describe_rules)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#describe_rules)
        """

    async def describe_ssl_policies(
        self,
        *,
        Names: Sequence[str] = ...,
        Marker: str = ...,
        PageSize: int = ...,
        LoadBalancerType: LoadBalancerTypeEnumType = ...
    ) -> DescribeSSLPoliciesOutputTypeDef:
        """
        Describes the specified policies or all policies used for SSL negotiation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.describe_ssl_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#describe_ssl_policies)
        """

    async def describe_tags(self, *, ResourceArns: Sequence[str]) -> DescribeTagsOutputTypeDef:
        """
        Describes the tags for the specified Elastic Load Balancing resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.describe_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#describe_tags)
        """

    async def describe_target_group_attributes(
        self, *, TargetGroupArn: str
    ) -> DescribeTargetGroupAttributesOutputTypeDef:
        """
        Describes the attributes for the specified target group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.describe_target_group_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#describe_target_group_attributes)
        """

    async def describe_target_groups(
        self,
        *,
        LoadBalancerArn: str = ...,
        TargetGroupArns: Sequence[str] = ...,
        Names: Sequence[str] = ...,
        Marker: str = ...,
        PageSize: int = ...
    ) -> DescribeTargetGroupsOutputTypeDef:
        """
        Describes the specified target groups or all of your target groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.describe_target_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#describe_target_groups)
        """

    async def describe_target_health(
        self, *, TargetGroupArn: str, Targets: Sequence["TargetDescriptionTypeDef"] = ...
    ) -> DescribeTargetHealthOutputTypeDef:
        """
        Describes the health of the specified targets or all of your targets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.describe_target_health)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#describe_target_health)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#generate_presigned_url)
        """

    async def modify_listener(
        self,
        *,
        ListenerArn: str,
        Port: int = ...,
        Protocol: ProtocolEnumType = ...,
        SslPolicy: str = ...,
        Certificates: Sequence["CertificateTypeDef"] = ...,
        DefaultActions: Sequence["ActionTypeDef"] = ...,
        AlpnPolicy: Sequence[str] = ...
    ) -> ModifyListenerOutputTypeDef:
        """
        Replaces the specified properties of the specified listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.modify_listener)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#modify_listener)
        """

    async def modify_load_balancer_attributes(
        self, *, LoadBalancerArn: str, Attributes: Sequence["LoadBalancerAttributeTypeDef"]
    ) -> ModifyLoadBalancerAttributesOutputTypeDef:
        """
        Modifies the specified attributes of the specified Application Load Balancer,
        Network Load Balancer, or Gateway Load Balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.modify_load_balancer_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#modify_load_balancer_attributes)
        """

    async def modify_rule(
        self,
        *,
        RuleArn: str,
        Conditions: Sequence["RuleConditionTypeDef"] = ...,
        Actions: Sequence["ActionTypeDef"] = ...
    ) -> ModifyRuleOutputTypeDef:
        """
        Replaces the specified properties of the specified rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.modify_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#modify_rule)
        """

    async def modify_target_group(
        self,
        *,
        TargetGroupArn: str,
        HealthCheckProtocol: ProtocolEnumType = ...,
        HealthCheckPort: str = ...,
        HealthCheckPath: str = ...,
        HealthCheckEnabled: bool = ...,
        HealthCheckIntervalSeconds: int = ...,
        HealthCheckTimeoutSeconds: int = ...,
        HealthyThresholdCount: int = ...,
        UnhealthyThresholdCount: int = ...,
        Matcher: "MatcherTypeDef" = ...
    ) -> ModifyTargetGroupOutputTypeDef:
        """
        Modifies the health checks used when evaluating the health state of the targets
        in the specified target group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.modify_target_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#modify_target_group)
        """

    async def modify_target_group_attributes(
        self, *, TargetGroupArn: str, Attributes: Sequence["TargetGroupAttributeTypeDef"]
    ) -> ModifyTargetGroupAttributesOutputTypeDef:
        """
        Modifies the specified attributes of the specified target group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.modify_target_group_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#modify_target_group_attributes)
        """

    async def register_targets(
        self, *, TargetGroupArn: str, Targets: Sequence["TargetDescriptionTypeDef"]
    ) -> Dict[str, Any]:
        """
        Registers the specified targets with the specified target group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.register_targets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#register_targets)
        """

    async def remove_listener_certificates(
        self, *, ListenerArn: str, Certificates: Sequence["CertificateTypeDef"]
    ) -> Dict[str, Any]:
        """
        Removes the specified certificate from the certificate list for the specified
        HTTPS or TLS listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.remove_listener_certificates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#remove_listener_certificates)
        """

    async def remove_tags(
        self, *, ResourceArns: Sequence[str], TagKeys: Sequence[str]
    ) -> Dict[str, Any]:
        """
        Removes the specified tags from the specified Elastic Load Balancing resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.remove_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#remove_tags)
        """

    async def set_ip_address_type(
        self, *, LoadBalancerArn: str, IpAddressType: IpAddressTypeType
    ) -> SetIpAddressTypeOutputTypeDef:
        """
        Sets the type of IP addresses used by the subnets of the specified Application
        Load Balancer or Network Load Balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.set_ip_address_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#set_ip_address_type)
        """

    async def set_rule_priorities(
        self, *, RulePriorities: Sequence["RulePriorityPairTypeDef"]
    ) -> SetRulePrioritiesOutputTypeDef:
        """
        Sets the priorities of the specified rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.set_rule_priorities)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#set_rule_priorities)
        """

    async def set_security_groups(
        self, *, LoadBalancerArn: str, SecurityGroups: Sequence[str]
    ) -> SetSecurityGroupsOutputTypeDef:
        """
        Associates the specified security groups with the specified Application Load
        Balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.set_security_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#set_security_groups)
        """

    async def set_subnets(
        self,
        *,
        LoadBalancerArn: str,
        Subnets: Sequence[str] = ...,
        SubnetMappings: Sequence["SubnetMappingTypeDef"] = ...,
        IpAddressType: IpAddressTypeType = ...
    ) -> SetSubnetsOutputTypeDef:
        """
        Enables the Availability Zones for the specified public subnets for the
        specified Application Load Balancer or Network Load Balancer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.set_subnets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#set_subnets)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_account_limits"]
    ) -> DescribeAccountLimitsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_listener_certificates"]
    ) -> DescribeListenerCertificatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_listeners"]
    ) -> DescribeListenersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_load_balancers"]
    ) -> DescribeLoadBalancersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_rules"]) -> DescribeRulesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_ssl_policies"]
    ) -> DescribeSSLPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_target_groups"]
    ) -> DescribeTargetGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#get_paginator)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["load_balancer_available"]
    ) -> LoadBalancerAvailableWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["load_balancer_exists"]) -> LoadBalancerExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["load_balancers_deleted"]
    ) -> LoadBalancersDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["target_deregistered"]) -> TargetDeregisteredWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["target_in_service"]) -> TargetInServiceWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/#get_waiter)
        """

    async def __aenter__(self) -> "ElasticLoadBalancingv2Client":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/client/)
        """
