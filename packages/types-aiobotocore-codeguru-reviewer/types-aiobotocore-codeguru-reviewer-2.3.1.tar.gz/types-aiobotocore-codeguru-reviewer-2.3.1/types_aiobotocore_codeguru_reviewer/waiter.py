"""
Type annotations for codeguru-reviewer service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_codeguru_reviewer.client import CodeGuruReviewerClient
    from types_aiobotocore_codeguru_reviewer.waiter import (
        CodeReviewCompletedWaiter,
        RepositoryAssociationSucceededWaiter,
    )

    session = get_session()
    async with session.create_client("codeguru-reviewer") as client:
        client: CodeGuruReviewerClient

        code_review_completed_waiter: CodeReviewCompletedWaiter = client.get_waiter("code_review_completed")
        repository_association_succeeded_waiter: RepositoryAssociationSucceededWaiter = client.get_waiter("repository_association_succeeded")
    ```
"""
from aiobotocore.waiter import AIOWaiter

from .type_defs import WaiterConfigTypeDef

__all__ = ("CodeReviewCompletedWaiter", "RepositoryAssociationSucceededWaiter")


class CodeReviewCompletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Waiter.CodeReviewCompleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/waiters/#codereviewcompletedwaiter)
    """

    async def wait(self, *, CodeReviewArn: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Waiter.CodeReviewCompleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/waiters/#codereviewcompletedwaiter)
        """


class RepositoryAssociationSucceededWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Waiter.RepositoryAssociationSucceeded)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/waiters/#repositoryassociationsucceededwaiter)
    """

    async def wait(self, *, AssociationArn: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Waiter.RepositoryAssociationSucceeded.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/waiters/#repositoryassociationsucceededwaiter)
        """
