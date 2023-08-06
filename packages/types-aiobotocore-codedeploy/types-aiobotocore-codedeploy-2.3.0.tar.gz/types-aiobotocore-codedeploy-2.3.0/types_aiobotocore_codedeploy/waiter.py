"""
Type annotations for codedeploy service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_codedeploy.client import CodeDeployClient
    from types_aiobotocore_codedeploy.waiter import (
        DeploymentSuccessfulWaiter,
    )

    session = get_session()
    async with session.create_client("codedeploy") as client:
        client: CodeDeployClient

        deployment_successful_waiter: DeploymentSuccessfulWaiter = client.get_waiter("deployment_successful")
    ```
"""
from aiobotocore.waiter import AIOWaiter

from .type_defs import WaiterConfigTypeDef

__all__ = ("DeploymentSuccessfulWaiter",)


class DeploymentSuccessfulWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Waiter.DeploymentSuccessful)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/waiters/#deploymentsuccessfulwaiter)
    """

    async def wait(self, *, deploymentId: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy.html#CodeDeploy.Waiter.DeploymentSuccessful.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/waiters/#deploymentsuccessfulwaiter)
        """
