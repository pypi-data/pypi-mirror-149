"""
Type annotations for sqs service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_sqs.client import SQSClient
    from types_aiobotocore_sqs.paginator import (
        ListDeadLetterSourceQueuesPaginator,
        ListQueuesPaginator,
    )

    session = get_session()
    with session.create_client("sqs") as client:
        client: SQSClient

        list_dead_letter_source_queues_paginator: ListDeadLetterSourceQueuesPaginator = client.get_paginator("list_dead_letter_source_queues")
        list_queues_paginator: ListQueuesPaginator = client.get_paginator("list_queues")
    ```
"""
import sys
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListDeadLetterSourceQueuesResultTypeDef,
    ListQueuesResultTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator

__all__ = ("ListDeadLetterSourceQueuesPaginator", "ListQueuesPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListDeadLetterSourceQueuesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Paginator.ListDeadLetterSourceQueues)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/paginators/#listdeadlettersourcequeuespaginator)
    """

    def paginate(
        self, *, QueueUrl: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListDeadLetterSourceQueuesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Paginator.ListDeadLetterSourceQueues.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/paginators/#listdeadlettersourcequeuespaginator)
        """

class ListQueuesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Paginator.ListQueues)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/paginators/#listqueuespaginator)
    """

    def paginate(
        self, *, QueueNamePrefix: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListQueuesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Paginator.ListQueues.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/paginators/#listqueuespaginator)
        """
