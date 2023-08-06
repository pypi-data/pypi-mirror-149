"""
Type annotations for macie service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_macie.client import MacieClient

    session = get_session()
    async with session.create_client("macie") as client:
        client: MacieClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import ListMemberAccountsPaginator, ListS3ResourcesPaginator
from .type_defs import (
    AssociateS3ResourcesResultTypeDef,
    DisassociateS3ResourcesResultTypeDef,
    ListMemberAccountsResultTypeDef,
    ListS3ResourcesResultTypeDef,
    S3ResourceClassificationTypeDef,
    S3ResourceClassificationUpdateTypeDef,
    S3ResourceTypeDef,
    UpdateS3ResourcesResultTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("MacieClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalException: Type[BotocoreClientError]
    InvalidInputException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]

class MacieClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MacieClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie/client/#exceptions)
        """
    async def associate_member_account(self, *, memberAccountId: str) -> None:
        """
        (Discontinued) Associates a specified Amazon Web Services account with Amazon
        Macie Classic as a member account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie.Client.associate_member_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie/client/#associate_member_account)
        """
    async def associate_s3_resources(
        self,
        *,
        s3Resources: Sequence["S3ResourceClassificationTypeDef"],
        memberAccountId: str = ...
    ) -> AssociateS3ResourcesResultTypeDef:
        """
        (Discontinued) Associates specified S3 resources with Amazon Macie Classic for
        monitoring and data classification.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie.Client.associate_s3_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie/client/#associate_s3_resources)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie/client/#can_paginate)
        """
    async def disassociate_member_account(self, *, memberAccountId: str) -> None:
        """
        (Discontinued) Removes the specified member account from Amazon Macie Classic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie.Client.disassociate_member_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie/client/#disassociate_member_account)
        """
    async def disassociate_s3_resources(
        self, *, associatedS3Resources: Sequence["S3ResourceTypeDef"], memberAccountId: str = ...
    ) -> DisassociateS3ResourcesResultTypeDef:
        """
        (Discontinued) Removes specified S3 resources from being monitored by Amazon
        Macie Classic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie.Client.disassociate_s3_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie/client/#disassociate_s3_resources)
        """
    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie/client/#generate_presigned_url)
        """
    async def list_member_accounts(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListMemberAccountsResultTypeDef:
        """
        (Discontinued) Lists all Amazon Macie Classic member accounts for the current
        Macie Classic administrator account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie.Client.list_member_accounts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie/client/#list_member_accounts)
        """
    async def list_s3_resources(
        self, *, memberAccountId: str = ..., nextToken: str = ..., maxResults: int = ...
    ) -> ListS3ResourcesResultTypeDef:
        """
        (Discontinued) Lists all the S3 resources associated with Amazon Macie Classic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie.Client.list_s3_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie/client/#list_s3_resources)
        """
    async def update_s3_resources(
        self,
        *,
        s3ResourcesUpdate: Sequence["S3ResourceClassificationUpdateTypeDef"],
        memberAccountId: str = ...
    ) -> UpdateS3ResourcesResultTypeDef:
        """
        (Discontinued) Updates the classification types for the specified S3 resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie.Client.update_s3_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie/client/#update_s3_resources)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_member_accounts"]
    ) -> ListMemberAccountsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_s3_resources"]
    ) -> ListS3ResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie/client/#get_paginator)
        """
    async def __aenter__(self) -> "MacieClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie.html#Macie.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie/client/)
        """
