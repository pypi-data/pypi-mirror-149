"""
Type annotations for elbv2 service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_elbv2.client import ElasticLoadBalancingv2Client
    from types_aiobotocore_elbv2.waiter import (
        LoadBalancerAvailableWaiter,
        LoadBalancerExistsWaiter,
        LoadBalancersDeletedWaiter,
        TargetDeregisteredWaiter,
        TargetInServiceWaiter,
    )

    session = get_session()
    async with session.create_client("elbv2") as client:
        client: ElasticLoadBalancingv2Client

        load_balancer_available_waiter: LoadBalancerAvailableWaiter = client.get_waiter("load_balancer_available")
        load_balancer_exists_waiter: LoadBalancerExistsWaiter = client.get_waiter("load_balancer_exists")
        load_balancers_deleted_waiter: LoadBalancersDeletedWaiter = client.get_waiter("load_balancers_deleted")
        target_deregistered_waiter: TargetDeregisteredWaiter = client.get_waiter("target_deregistered")
        target_in_service_waiter: TargetInServiceWaiter = client.get_waiter("target_in_service")
    ```
"""
from typing import Sequence

from aiobotocore.waiter import AIOWaiter

from .type_defs import TargetDescriptionTypeDef, WaiterConfigTypeDef

__all__ = (
    "LoadBalancerAvailableWaiter",
    "LoadBalancerExistsWaiter",
    "LoadBalancersDeletedWaiter",
    "TargetDeregisteredWaiter",
    "TargetInServiceWaiter",
)


class LoadBalancerAvailableWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Waiter.LoadBalancerAvailable)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/waiters/#loadbalanceravailablewaiter)
    """

    async def wait(
        self,
        *,
        LoadBalancerArns: Sequence[str] = ...,
        Names: Sequence[str] = ...,
        Marker: str = ...,
        PageSize: int = ...,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Waiter.LoadBalancerAvailable.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/waiters/#loadbalanceravailablewaiter)
        """


class LoadBalancerExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Waiter.LoadBalancerExists)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/waiters/#loadbalancerexistswaiter)
    """

    async def wait(
        self,
        *,
        LoadBalancerArns: Sequence[str] = ...,
        Names: Sequence[str] = ...,
        Marker: str = ...,
        PageSize: int = ...,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Waiter.LoadBalancerExists.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/waiters/#loadbalancerexistswaiter)
        """


class LoadBalancersDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Waiter.LoadBalancersDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/waiters/#loadbalancersdeletedwaiter)
    """

    async def wait(
        self,
        *,
        LoadBalancerArns: Sequence[str] = ...,
        Names: Sequence[str] = ...,
        Marker: str = ...,
        PageSize: int = ...,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Waiter.LoadBalancersDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/waiters/#loadbalancersdeletedwaiter)
        """


class TargetDeregisteredWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Waiter.TargetDeregistered)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/waiters/#targetderegisteredwaiter)
    """

    async def wait(
        self,
        *,
        TargetGroupArn: str,
        Targets: Sequence["TargetDescriptionTypeDef"] = ...,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Waiter.TargetDeregistered.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/waiters/#targetderegisteredwaiter)
        """


class TargetInServiceWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Waiter.TargetInService)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/waiters/#targetinservicewaiter)
    """

    async def wait(
        self,
        *,
        TargetGroupArn: str,
        Targets: Sequence["TargetDescriptionTypeDef"] = ...,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2.html#ElasticLoadBalancingv2.Waiter.TargetInService.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/waiters/#targetinservicewaiter)
        """
