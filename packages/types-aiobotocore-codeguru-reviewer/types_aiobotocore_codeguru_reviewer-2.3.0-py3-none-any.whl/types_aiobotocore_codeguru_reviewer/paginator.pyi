"""
Type annotations for codeguru-reviewer service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_codeguru_reviewer.client import CodeGuruReviewerClient
    from types_aiobotocore_codeguru_reviewer.paginator import (
        ListRepositoryAssociationsPaginator,
    )

    session = get_session()
    with session.create_client("codeguru-reviewer") as client:
        client: CodeGuruReviewerClient

        list_repository_associations_paginator: ListRepositoryAssociationsPaginator = client.get_paginator("list_repository_associations")
    ```
"""
import sys
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import ProviderTypeType, RepositoryAssociationStateType
from .type_defs import ListRepositoryAssociationsResponseTypeDef, PaginatorConfigTypeDef

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator

__all__ = ("ListRepositoryAssociationsPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListRepositoryAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Paginator.ListRepositoryAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/paginators/#listrepositoryassociationspaginator)
    """

    def paginate(
        self,
        *,
        ProviderTypes: Sequence[ProviderTypeType] = ...,
        States: Sequence[RepositoryAssociationStateType] = ...,
        Names: Sequence[str] = ...,
        Owners: Sequence[str] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListRepositoryAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Paginator.ListRepositoryAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/paginators/#listrepositoryassociationspaginator)
        """
