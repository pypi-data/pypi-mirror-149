"""
Type annotations for acm service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_acm.client import ACMClient
    from types_aiobotocore_acm.paginator import (
        ListCertificatesPaginator,
    )

    session = get_session()
    with session.create_client("acm") as client:
        client: ACMClient

        list_certificates_paginator: ListCertificatesPaginator = client.get_paginator("list_certificates")
    ```
"""
import sys
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import CertificateStatusType
from .type_defs import FiltersTypeDef, ListCertificatesResponseTypeDef, PaginatorConfigTypeDef

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator

__all__ = ("ListCertificatesPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListCertificatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Paginator.ListCertificates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/paginators/#listcertificatespaginator)
    """

    def paginate(
        self,
        *,
        CertificateStatuses: Sequence[CertificateStatusType] = ...,
        Includes: "FiltersTypeDef" = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Paginator.ListCertificates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/paginators/#listcertificatespaginator)
        """
