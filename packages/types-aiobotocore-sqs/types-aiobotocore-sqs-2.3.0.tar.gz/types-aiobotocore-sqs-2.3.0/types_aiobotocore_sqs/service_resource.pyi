"""
Type annotations for sqs service ServiceResource

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_sqs.service_resource import SQSServiceResource
    import types_aiobotocore_sqs.service_resource as sqs_resources

    session = get_session()
    async with session.resource("sqs") as resource:
        resource: SQSServiceResource

        my_message: sqs_resources.Message = resource.Message(...)
        my_queue: sqs_resources.Queue = resource.Queue(...)
```
"""
import sys
from typing import Dict, Iterator, List, Mapping, Sequence

from boto3.resources.base import ResourceMeta
from boto3.resources.base import ServiceResource as Boto3ServiceResource
from boto3.resources.collection import ResourceCollection

from .client import SQSClient
from .literals import MessageSystemAttributeNameType, QueueAttributeNameType
from .type_defs import (
    ChangeMessageVisibilityBatchRequestEntryTypeDef,
    ChangeMessageVisibilityBatchResultTypeDef,
    DeleteMessageBatchRequestEntryTypeDef,
    DeleteMessageBatchResultTypeDef,
    MessageAttributeValueTypeDef,
    MessageSystemAttributeValueTypeDef,
    SendMessageBatchRequestEntryTypeDef,
    SendMessageBatchResultTypeDef,
    SendMessageResultTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "SQSServiceResource",
    "Message",
    "Queue",
    "ServiceResourceQueuesCollection",
    "QueueDeadLetterSourceQueuesCollection",
)

class ServiceResourceQueuesCollection(ResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.ServiceResource.queues)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#serviceresourcequeuescollection)
    """

    async def all(self) -> "ServiceResourceQueuesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.ServiceResource.queues)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#serviceresourcequeuescollection)
        """
    async def filter(  # type: ignore
        self, *, QueueNamePrefix: str = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> "ServiceResourceQueuesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.ServiceResource.queues)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#serviceresourcequeuescollection)
        """
    async def limit(self, count: int) -> "ServiceResourceQueuesCollection":
        """
        Return at most this many Queues.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.ServiceResource.queues)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#serviceresourcequeuescollection)
        """
    async def page_size(self, count: int) -> "ServiceResourceQueuesCollection":
        """
        Fetch at most this many Queues per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.ServiceResource.queues)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#serviceresourcequeuescollection)
        """
    async def pages(self) -> Iterator[List["Queue"]]:
        """
        A generator which yields pages of Queues.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.ServiceResource.queues)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#serviceresourcequeuescollection)
        """
    async def __iter__(self) -> Iterator["Queue"]:
        """
        A generator which yields Queues.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.ServiceResource.queues)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#serviceresourcequeuescollection)
        """

class QueueDeadLetterSourceQueuesCollection(ResourceCollection):
    async def all(self) -> "QueueDeadLetterSourceQueuesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """
    async def filter(  # type: ignore
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> "QueueDeadLetterSourceQueuesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """
    async def limit(self, count: int) -> "QueueDeadLetterSourceQueuesCollection":
        """
        Return at most this many Queues.
        """
    async def page_size(self, count: int) -> "QueueDeadLetterSourceQueuesCollection":
        """
        Fetch at most this many Queues per service request.
        """
    async def pages(self) -> Iterator[List["Queue"]]:
        """
        A generator which yields pages of Queues.
        """
    async def __iter__(self) -> Iterator["Queue"]:
        """
        A generator which yields Queues.
        """

class Message(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.ServiceResource.Message)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#message)
    """

    message_id: str
    md5_of_body: str
    body: str
    attributes: Dict[MessageSystemAttributeNameType, str]
    md5_of_message_attributes: str
    message_attributes: Dict[str, "MessageAttributeValueTypeDef"]
    queue_url: str
    receipt_handle: str

    async def Queue(self) -> "_Queue":
        """
        Creates a Queue resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Message.Queue)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#messagequeue-method)
        """
    async def change_visibility(self, *, VisibilityTimeout: int) -> None:
        """
        Changes the visibility timeout of a specified message in a queue to a new value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Message.change_visibility)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#messagechange_visibility-method)
        """
    async def delete(self) -> None:
        """
        Deletes the specified message from the specified queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Message.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#messagedelete-method)
        """
    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Message.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#messageget_available_subresources-method)
        """

_Message = Message

class Queue(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.ServiceResource.Queue)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#queue)
    """

    attributes: Dict[QueueAttributeNameType, str]
    url: str
    dead_letter_source_queues: QueueDeadLetterSourceQueuesCollection

    async def Message(self, receipt_handle: str) -> _Message:
        """
        Creates a Message resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.Message)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#queuemessage-method)
        """
    async def add_permission(
        self, *, Label: str, AWSAccountIds: Sequence[str], Actions: Sequence[str]
    ) -> None:
        """
        Adds a permission to a queue for a specific
        [principal](https://docs.aws.amazon.com/general/latest/gr/glos-chap.html#P)_.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.add_permission)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#queueadd_permission-method)
        """
    async def change_message_visibility_batch(
        self, *, Entries: Sequence["ChangeMessageVisibilityBatchRequestEntryTypeDef"]
    ) -> ChangeMessageVisibilityBatchResultTypeDef:
        """
        Changes the visibility timeout of multiple messages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.change_message_visibility_batch)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#queuechange_message_visibility_batch-method)
        """
    async def delete(self) -> None:
        """
        Deletes the queue specified by the `QueueUrl` , regardless of the queue's
        contents.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#queuedelete-method)
        """
    async def delete_messages(
        self, *, Entries: Sequence["DeleteMessageBatchRequestEntryTypeDef"]
    ) -> DeleteMessageBatchResultTypeDef:
        """
        Deletes up to ten messages from the specified queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.delete_messages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#queuedelete_messages-method)
        """
    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#queueget_available_subresources-method)
        """
    async def load(self) -> None:
        """
        Calls :py:meth:`SQS.Client.get_queue_attributes` to update the attributes of the
        Queue resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#queueload-method)
        """
    async def purge(self) -> None:
        """
        Deletes the messages in a queue specified by the `QueueURL` parameter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.purge)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#queuepurge-method)
        """
    async def receive_messages(
        self,
        *,
        AttributeNames: Sequence[QueueAttributeNameType] = ...,
        MessageAttributeNames: Sequence[str] = ...,
        MaxNumberOfMessages: int = ...,
        VisibilityTimeout: int = ...,
        WaitTimeSeconds: int = ...,
        ReceiveRequestAttemptId: str = ...
    ) -> List[_Message]:
        """
        Retrieves one or more messages (up to 10), from the specified queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.receive_messages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#queuereceive_messages-method)
        """
    async def reload(self) -> None:
        """
        Calls :py:meth:`SQS.Client.get_queue_attributes` to update the attributes of the
        Queue resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#queuereload-method)
        """
    async def remove_permission(self, *, Label: str) -> None:
        """
        Revokes any permissions in the queue policy that matches the specified `Label`
        parameter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.remove_permission)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#queueremove_permission-method)
        """
    async def send_message(
        self,
        *,
        MessageBody: str,
        DelaySeconds: int = ...,
        MessageAttributes: Mapping[str, "MessageAttributeValueTypeDef"] = ...,
        MessageSystemAttributes: Mapping[
            Literal["AWSTraceHeader"], "MessageSystemAttributeValueTypeDef"
        ] = ...,
        MessageDeduplicationId: str = ...,
        MessageGroupId: str = ...
    ) -> SendMessageResultTypeDef:
        """
        Delivers a message to the specified queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.send_message)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#queuesend_message-method)
        """
    async def send_messages(
        self, *, Entries: Sequence["SendMessageBatchRequestEntryTypeDef"]
    ) -> SendMessageBatchResultTypeDef:
        """
        Delivers up to ten messages to the specified queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.send_messages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#queuesend_messages-method)
        """
    async def set_attributes(self, *, Attributes: Mapping[QueueAttributeNameType, str]) -> None:
        """
        Sets the value of one or more queue attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.set_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#queueset_attributes-method)
        """

_Queue = Queue

class SQSResourceMeta(ResourceMeta):
    client: SQSClient

class SQSServiceResource(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.ServiceResource)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/)
    """

    meta: "SQSResourceMeta"
    queues: ServiceResourceQueuesCollection

    async def Message(self, queue_url: str, receipt_handle: str) -> _Message:
        """
        Creates a Message resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.ServiceResource.Message)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#sqsserviceresourcemessage-method)
        """
    async def Queue(self, url: str) -> _Queue:
        """
        Creates a Queue resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.ServiceResource.Queue)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#sqsserviceresourcequeue-method)
        """
    async def create_queue(
        self,
        *,
        QueueName: str,
        Attributes: Mapping[QueueAttributeNameType, str] = ...,
        tags: Mapping[str, str] = ...
    ) -> _Queue:
        """
        Creates a new standard or FIFO queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.ServiceResource.create_queue)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#sqsserviceresourcecreate_queue-method)
        """
    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.ServiceResource.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#sqsserviceresourceget_available_subresources-method)
        """
    async def get_queue_by_name(
        self, *, QueueName: str, QueueOwnerAWSAccountId: str = ...
    ) -> _Queue:
        """
        Returns the URL of an existing Amazon SQS queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.ServiceResource.get_queue_by_name)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#sqsserviceresourceget_queue_by_name-method)
        """
