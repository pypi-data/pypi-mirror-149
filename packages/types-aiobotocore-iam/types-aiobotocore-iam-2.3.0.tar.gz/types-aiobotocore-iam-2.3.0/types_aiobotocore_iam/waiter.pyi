"""
Type annotations for iam service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_iam.client import IAMClient
    from types_aiobotocore_iam.waiter import (
        InstanceProfileExistsWaiter,
        PolicyExistsWaiter,
        RoleExistsWaiter,
        UserExistsWaiter,
    )

    session = get_session()
    async with session.create_client("iam") as client:
        client: IAMClient

        instance_profile_exists_waiter: InstanceProfileExistsWaiter = client.get_waiter("instance_profile_exists")
        policy_exists_waiter: PolicyExistsWaiter = client.get_waiter("policy_exists")
        role_exists_waiter: RoleExistsWaiter = client.get_waiter("role_exists")
        user_exists_waiter: UserExistsWaiter = client.get_waiter("user_exists")
    ```
"""
from aiobotocore.waiter import AIOWaiter

from .type_defs import WaiterConfigTypeDef

__all__ = (
    "InstanceProfileExistsWaiter",
    "PolicyExistsWaiter",
    "RoleExistsWaiter",
    "UserExistsWaiter",
)

class InstanceProfileExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Waiter.InstanceProfileExists)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/waiters/#instanceprofileexistswaiter)
    """

    async def wait(
        self, *, InstanceProfileName: str, WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Waiter.InstanceProfileExists.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/waiters/#instanceprofileexistswaiter)
        """

class PolicyExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Waiter.PolicyExists)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/waiters/#policyexistswaiter)
    """

    async def wait(self, *, PolicyArn: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Waiter.PolicyExists.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/waiters/#policyexistswaiter)
        """

class RoleExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Waiter.RoleExists)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/waiters/#roleexistswaiter)
    """

    async def wait(self, *, RoleName: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Waiter.RoleExists.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/waiters/#roleexistswaiter)
        """

class UserExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Waiter.UserExists)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/waiters/#userexistswaiter)
    """

    async def wait(self, *, UserName: str = ..., WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Waiter.UserExists.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iam/waiters/#userexistswaiter)
        """
