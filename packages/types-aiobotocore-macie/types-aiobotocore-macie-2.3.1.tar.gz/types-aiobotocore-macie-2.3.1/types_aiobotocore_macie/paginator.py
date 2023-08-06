"""
Type annotations for macie service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_macie.client import MacieClient
    from types_aiobotocore_macie.paginator import (
        ListMemberAccountsPaginator,
        ListS3ResourcesPaginator,
    )

    session = get_session()
    with session.create_client("macie") as client:
        client: MacieClient

        list_member_accounts_paginator: ListMemberAccountsPaginator = client.get_paginator("list_member_accounts")
        list_s3_resources_paginator: ListS3ResourcesPaginator = client.get_paginator("list_s3_resources")
    ```
"""
import sys
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListMemberAccountsResultTypeDef,
    ListS3ResourcesResultTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator


__all__ = ("ListMemberAccountsPaginator", "ListS3ResourcesPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListMemberAccountsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie.Paginator.ListMemberAccounts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie/paginators/#listmemberaccountspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListMemberAccountsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie.Paginator.ListMemberAccounts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie/paginators/#listmemberaccountspaginator)
        """


class ListS3ResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie.Paginator.ListS3Resources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie/paginators/#lists3resourcespaginator)
    """

    def paginate(
        self, *, memberAccountId: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListS3ResourcesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie.Paginator.ListS3Resources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie/paginators/#lists3resourcespaginator)
        """
