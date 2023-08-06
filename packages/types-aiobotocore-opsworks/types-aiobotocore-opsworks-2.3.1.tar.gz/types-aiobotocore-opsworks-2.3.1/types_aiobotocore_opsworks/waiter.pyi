"""
Type annotations for opsworks service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_opsworks.client import OpsWorksClient
    from types_aiobotocore_opsworks.waiter import (
        AppExistsWaiter,
        DeploymentSuccessfulWaiter,
        InstanceOnlineWaiter,
        InstanceRegisteredWaiter,
        InstanceStoppedWaiter,
        InstanceTerminatedWaiter,
    )

    session = get_session()
    async with session.create_client("opsworks") as client:
        client: OpsWorksClient

        app_exists_waiter: AppExistsWaiter = client.get_waiter("app_exists")
        deployment_successful_waiter: DeploymentSuccessfulWaiter = client.get_waiter("deployment_successful")
        instance_online_waiter: InstanceOnlineWaiter = client.get_waiter("instance_online")
        instance_registered_waiter: InstanceRegisteredWaiter = client.get_waiter("instance_registered")
        instance_stopped_waiter: InstanceStoppedWaiter = client.get_waiter("instance_stopped")
        instance_terminated_waiter: InstanceTerminatedWaiter = client.get_waiter("instance_terminated")
    ```
"""
from typing import Sequence

from aiobotocore.waiter import AIOWaiter

from .type_defs import WaiterConfigTypeDef

__all__ = (
    "AppExistsWaiter",
    "DeploymentSuccessfulWaiter",
    "InstanceOnlineWaiter",
    "InstanceRegisteredWaiter",
    "InstanceStoppedWaiter",
    "InstanceTerminatedWaiter",
)

class AppExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Waiter.AppExists)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/waiters/#appexistswaiter)
    """

    async def wait(
        self,
        *,
        StackId: str = ...,
        AppIds: Sequence[str] = ...,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Waiter.AppExists.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/waiters/#appexistswaiter)
        """

class DeploymentSuccessfulWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Waiter.DeploymentSuccessful)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/waiters/#deploymentsuccessfulwaiter)
    """

    async def wait(
        self,
        *,
        StackId: str = ...,
        AppId: str = ...,
        DeploymentIds: Sequence[str] = ...,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Waiter.DeploymentSuccessful.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/waiters/#deploymentsuccessfulwaiter)
        """

class InstanceOnlineWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Waiter.InstanceOnline)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/waiters/#instanceonlinewaiter)
    """

    async def wait(
        self,
        *,
        StackId: str = ...,
        LayerId: str = ...,
        InstanceIds: Sequence[str] = ...,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Waiter.InstanceOnline.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/waiters/#instanceonlinewaiter)
        """

class InstanceRegisteredWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Waiter.InstanceRegistered)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/waiters/#instanceregisteredwaiter)
    """

    async def wait(
        self,
        *,
        StackId: str = ...,
        LayerId: str = ...,
        InstanceIds: Sequence[str] = ...,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Waiter.InstanceRegistered.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/waiters/#instanceregisteredwaiter)
        """

class InstanceStoppedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Waiter.InstanceStopped)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/waiters/#instancestoppedwaiter)
    """

    async def wait(
        self,
        *,
        StackId: str = ...,
        LayerId: str = ...,
        InstanceIds: Sequence[str] = ...,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Waiter.InstanceStopped.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/waiters/#instancestoppedwaiter)
        """

class InstanceTerminatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Waiter.InstanceTerminated)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/waiters/#instanceterminatedwaiter)
    """

    async def wait(
        self,
        *,
        StackId: str = ...,
        LayerId: str = ...,
        InstanceIds: Sequence[str] = ...,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks.html#OpsWorks.Waiter.InstanceTerminated.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/waiters/#instanceterminatedwaiter)
        """
