"""
Type annotations for ses service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ses/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ses.client import SESClient
    from types_aiobotocore_ses.waiter import (
        IdentityExistsWaiter,
    )

    session = get_session()
    async with session.create_client("ses") as client:
        client: SESClient

        identity_exists_waiter: IdentityExistsWaiter = client.get_waiter("identity_exists")
    ```
"""
from typing import Sequence

from aiobotocore.waiter import AIOWaiter

from .type_defs import WaiterConfigTypeDef

__all__ = ("IdentityExistsWaiter",)

class IdentityExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses.html#SES.Waiter.IdentityExists)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ses/waiters/#identityexistswaiter)
    """

    async def wait(
        self, *, Identities: Sequence[str], WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses.html#SES.Waiter.IdentityExists.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ses/waiters/#identityexistswaiter)
        """
