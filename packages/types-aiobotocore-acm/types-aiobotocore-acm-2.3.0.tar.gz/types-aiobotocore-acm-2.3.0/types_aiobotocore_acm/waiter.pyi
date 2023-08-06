"""
Type annotations for acm service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_acm.client import ACMClient
    from types_aiobotocore_acm.waiter import (
        CertificateValidatedWaiter,
    )

    session = get_session()
    async with session.create_client("acm") as client:
        client: ACMClient

        certificate_validated_waiter: CertificateValidatedWaiter = client.get_waiter("certificate_validated")
    ```
"""
from aiobotocore.waiter import AIOWaiter

from .type_defs import WaiterConfigTypeDef

__all__ = ("CertificateValidatedWaiter",)

class CertificateValidatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Waiter.CertificateValidated)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/waiters/#certificatevalidatedwaiter)
    """

    async def wait(self, *, CertificateArn: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Waiter.CertificateValidated.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/waiters/#certificatevalidatedwaiter)
        """
