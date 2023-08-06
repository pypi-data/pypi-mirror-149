"""
Type annotations for cloudfront service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cloudfront.client import CloudFrontClient
    from types_aiobotocore_cloudfront.waiter import (
        DistributionDeployedWaiter,
        InvalidationCompletedWaiter,
        StreamingDistributionDeployedWaiter,
    )

    session = get_session()
    async with session.create_client("cloudfront") as client:
        client: CloudFrontClient

        distribution_deployed_waiter: DistributionDeployedWaiter = client.get_waiter("distribution_deployed")
        invalidation_completed_waiter: InvalidationCompletedWaiter = client.get_waiter("invalidation_completed")
        streaming_distribution_deployed_waiter: StreamingDistributionDeployedWaiter = client.get_waiter("streaming_distribution_deployed")
    ```
"""
from aiobotocore.waiter import AIOWaiter

from .type_defs import WaiterConfigTypeDef

__all__ = (
    "DistributionDeployedWaiter",
    "InvalidationCompletedWaiter",
    "StreamingDistributionDeployedWaiter",
)

class DistributionDeployedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront.html#CloudFront.Waiter.DistributionDeployed)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/waiters/#distributiondeployedwaiter)
    """

    async def wait(self, *, Id: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront.html#CloudFront.Waiter.DistributionDeployed.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/waiters/#distributiondeployedwaiter)
        """

class InvalidationCompletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront.html#CloudFront.Waiter.InvalidationCompleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/waiters/#invalidationcompletedwaiter)
    """

    async def wait(
        self, *, DistributionId: str, Id: str, WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront.html#CloudFront.Waiter.InvalidationCompleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/waiters/#invalidationcompletedwaiter)
        """

class StreamingDistributionDeployedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront.html#CloudFront.Waiter.StreamingDistributionDeployed)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/waiters/#streamingdistributiondeployedwaiter)
    """

    async def wait(self, *, Id: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront.html#CloudFront.Waiter.StreamingDistributionDeployed.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/waiters/#streamingdistributiondeployedwaiter)
        """
