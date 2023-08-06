"""
Type annotations for amplifybackend service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_amplifybackend.client import AmplifyBackendClient
    from types_aiobotocore_amplifybackend.paginator import (
        ListBackendJobsPaginator,
    )

    session = get_session()
    with session.create_client("amplifybackend") as client:
        client: AmplifyBackendClient

        list_backend_jobs_paginator: ListBackendJobsPaginator = client.get_paginator("list_backend_jobs")
    ```
"""
import sys
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import ListBackendJobsResponseTypeDef, PaginatorConfigTypeDef

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator

__all__ = ("ListBackendJobsPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListBackendJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Paginator.ListBackendJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/paginators/#listbackendjobspaginator)
    """

    def paginate(
        self,
        *,
        AppId: str,
        BackendEnvironmentName: str,
        JobId: str = ...,
        Operation: str = ...,
        Status: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListBackendJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Paginator.ListBackendJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/paginators/#listbackendjobspaginator)
        """
