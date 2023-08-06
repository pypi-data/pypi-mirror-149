"""
Type annotations for ssm service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ssm.client import SSMClient
    from types_aiobotocore_ssm.waiter import (
        CommandExecutedWaiter,
    )

    session = get_session()
    async with session.create_client("ssm") as client:
        client: SSMClient

        command_executed_waiter: CommandExecutedWaiter = client.get_waiter("command_executed")
    ```
"""
from aiobotocore.waiter import AIOWaiter

from .type_defs import WaiterConfigTypeDef

__all__ = ("CommandExecutedWaiter",)

class CommandExecutedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Waiter.CommandExecuted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/waiters/#commandexecutedwaiter)
    """

    async def wait(
        self,
        *,
        CommandId: str,
        InstanceId: str,
        PluginName: str = ...,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Waiter.CommandExecuted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/waiters/#commandexecutedwaiter)
        """
