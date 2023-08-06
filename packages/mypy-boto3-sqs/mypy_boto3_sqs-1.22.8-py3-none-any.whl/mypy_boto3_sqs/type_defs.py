"""
Type annotations for sqs service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sqs/type_defs/)

Usage::

    ```python
    from mypy_boto3_sqs.type_defs import AddPermissionRequestQueueAddPermissionTypeDef

    data: AddPermissionRequestQueueAddPermissionTypeDef = {...}
    ```
"""
import sys
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import MessageSystemAttributeNameType, QueueAttributeNameType

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AddPermissionRequestQueueAddPermissionTypeDef",
    "AddPermissionRequestRequestTypeDef",
    "BatchResultErrorEntryTypeDef",
    "ChangeMessageVisibilityBatchRequestEntryTypeDef",
    "ChangeMessageVisibilityBatchRequestQueueChangeMessageVisibilityBatchTypeDef",
    "ChangeMessageVisibilityBatchRequestRequestTypeDef",
    "ChangeMessageVisibilityBatchResultEntryTypeDef",
    "ChangeMessageVisibilityBatchResultTypeDef",
    "ChangeMessageVisibilityRequestMessageChangeVisibilityTypeDef",
    "ChangeMessageVisibilityRequestRequestTypeDef",
    "CreateQueueRequestRequestTypeDef",
    "CreateQueueRequestServiceResourceCreateQueueTypeDef",
    "CreateQueueResultTypeDef",
    "DeleteMessageBatchRequestEntryTypeDef",
    "DeleteMessageBatchRequestQueueDeleteMessagesTypeDef",
    "DeleteMessageBatchRequestRequestTypeDef",
    "DeleteMessageBatchResultEntryTypeDef",
    "DeleteMessageBatchResultTypeDef",
    "DeleteMessageRequestRequestTypeDef",
    "DeleteQueueRequestRequestTypeDef",
    "GetQueueAttributesRequestRequestTypeDef",
    "GetQueueAttributesResultTypeDef",
    "GetQueueUrlRequestRequestTypeDef",
    "GetQueueUrlRequestServiceResourceGetQueueByNameTypeDef",
    "GetQueueUrlResultTypeDef",
    "ListDeadLetterSourceQueuesRequestListDeadLetterSourceQueuesPaginateTypeDef",
    "ListDeadLetterSourceQueuesRequestRequestTypeDef",
    "ListDeadLetterSourceQueuesResultTypeDef",
    "ListQueueTagsRequestRequestTypeDef",
    "ListQueueTagsResultTypeDef",
    "ListQueuesRequestListQueuesPaginateTypeDef",
    "ListQueuesRequestRequestTypeDef",
    "ListQueuesResultTypeDef",
    "MessageAttributeValueTypeDef",
    "MessageSystemAttributeValueTypeDef",
    "MessageTypeDef",
    "PaginatorConfigTypeDef",
    "PurgeQueueRequestRequestTypeDef",
    "QueueMessageRequestTypeDef",
    "ReceiveMessageRequestQueueReceiveMessagesTypeDef",
    "ReceiveMessageRequestRequestTypeDef",
    "ReceiveMessageResultTypeDef",
    "RemovePermissionRequestQueueRemovePermissionTypeDef",
    "RemovePermissionRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "SendMessageBatchRequestEntryTypeDef",
    "SendMessageBatchRequestQueueSendMessagesTypeDef",
    "SendMessageBatchRequestRequestTypeDef",
    "SendMessageBatchResultEntryTypeDef",
    "SendMessageBatchResultTypeDef",
    "SendMessageRequestQueueSendMessageTypeDef",
    "SendMessageRequestRequestTypeDef",
    "SendMessageResultTypeDef",
    "ServiceResourceMessageRequestTypeDef",
    "ServiceResourceQueueRequestTypeDef",
    "SetQueueAttributesRequestQueueSetAttributesTypeDef",
    "SetQueueAttributesRequestRequestTypeDef",
    "TagQueueRequestRequestTypeDef",
    "UntagQueueRequestRequestTypeDef",
)

AddPermissionRequestQueueAddPermissionTypeDef = TypedDict(
    "AddPermissionRequestQueueAddPermissionTypeDef",
    {
        "Label": str,
        "AWSAccountIds": Sequence[str],
        "Actions": Sequence[str],
    },
)

AddPermissionRequestRequestTypeDef = TypedDict(
    "AddPermissionRequestRequestTypeDef",
    {
        "QueueUrl": str,
        "Label": str,
        "AWSAccountIds": Sequence[str],
        "Actions": Sequence[str],
    },
)

_RequiredBatchResultErrorEntryTypeDef = TypedDict(
    "_RequiredBatchResultErrorEntryTypeDef",
    {
        "Id": str,
        "SenderFault": bool,
        "Code": str,
    },
)
_OptionalBatchResultErrorEntryTypeDef = TypedDict(
    "_OptionalBatchResultErrorEntryTypeDef",
    {
        "Message": str,
    },
    total=False,
)


class BatchResultErrorEntryTypeDef(
    _RequiredBatchResultErrorEntryTypeDef, _OptionalBatchResultErrorEntryTypeDef
):
    pass


_RequiredChangeMessageVisibilityBatchRequestEntryTypeDef = TypedDict(
    "_RequiredChangeMessageVisibilityBatchRequestEntryTypeDef",
    {
        "Id": str,
        "ReceiptHandle": str,
    },
)
_OptionalChangeMessageVisibilityBatchRequestEntryTypeDef = TypedDict(
    "_OptionalChangeMessageVisibilityBatchRequestEntryTypeDef",
    {
        "VisibilityTimeout": int,
    },
    total=False,
)


class ChangeMessageVisibilityBatchRequestEntryTypeDef(
    _RequiredChangeMessageVisibilityBatchRequestEntryTypeDef,
    _OptionalChangeMessageVisibilityBatchRequestEntryTypeDef,
):
    pass


ChangeMessageVisibilityBatchRequestQueueChangeMessageVisibilityBatchTypeDef = TypedDict(
    "ChangeMessageVisibilityBatchRequestQueueChangeMessageVisibilityBatchTypeDef",
    {
        "Entries": Sequence["ChangeMessageVisibilityBatchRequestEntryTypeDef"],
    },
)

ChangeMessageVisibilityBatchRequestRequestTypeDef = TypedDict(
    "ChangeMessageVisibilityBatchRequestRequestTypeDef",
    {
        "QueueUrl": str,
        "Entries": Sequence["ChangeMessageVisibilityBatchRequestEntryTypeDef"],
    },
)

ChangeMessageVisibilityBatchResultEntryTypeDef = TypedDict(
    "ChangeMessageVisibilityBatchResultEntryTypeDef",
    {
        "Id": str,
    },
)

ChangeMessageVisibilityBatchResultTypeDef = TypedDict(
    "ChangeMessageVisibilityBatchResultTypeDef",
    {
        "Successful": List["ChangeMessageVisibilityBatchResultEntryTypeDef"],
        "Failed": List["BatchResultErrorEntryTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ChangeMessageVisibilityRequestMessageChangeVisibilityTypeDef = TypedDict(
    "ChangeMessageVisibilityRequestMessageChangeVisibilityTypeDef",
    {
        "VisibilityTimeout": int,
    },
)

ChangeMessageVisibilityRequestRequestTypeDef = TypedDict(
    "ChangeMessageVisibilityRequestRequestTypeDef",
    {
        "QueueUrl": str,
        "ReceiptHandle": str,
        "VisibilityTimeout": int,
    },
)

_RequiredCreateQueueRequestRequestTypeDef = TypedDict(
    "_RequiredCreateQueueRequestRequestTypeDef",
    {
        "QueueName": str,
    },
)
_OptionalCreateQueueRequestRequestTypeDef = TypedDict(
    "_OptionalCreateQueueRequestRequestTypeDef",
    {
        "Attributes": Mapping[QueueAttributeNameType, str],
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateQueueRequestRequestTypeDef(
    _RequiredCreateQueueRequestRequestTypeDef, _OptionalCreateQueueRequestRequestTypeDef
):
    pass


_RequiredCreateQueueRequestServiceResourceCreateQueueTypeDef = TypedDict(
    "_RequiredCreateQueueRequestServiceResourceCreateQueueTypeDef",
    {
        "QueueName": str,
    },
)
_OptionalCreateQueueRequestServiceResourceCreateQueueTypeDef = TypedDict(
    "_OptionalCreateQueueRequestServiceResourceCreateQueueTypeDef",
    {
        "Attributes": Mapping[QueueAttributeNameType, str],
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateQueueRequestServiceResourceCreateQueueTypeDef(
    _RequiredCreateQueueRequestServiceResourceCreateQueueTypeDef,
    _OptionalCreateQueueRequestServiceResourceCreateQueueTypeDef,
):
    pass


CreateQueueResultTypeDef = TypedDict(
    "CreateQueueResultTypeDef",
    {
        "QueueUrl": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteMessageBatchRequestEntryTypeDef = TypedDict(
    "DeleteMessageBatchRequestEntryTypeDef",
    {
        "Id": str,
        "ReceiptHandle": str,
    },
)

DeleteMessageBatchRequestQueueDeleteMessagesTypeDef = TypedDict(
    "DeleteMessageBatchRequestQueueDeleteMessagesTypeDef",
    {
        "Entries": Sequence["DeleteMessageBatchRequestEntryTypeDef"],
    },
)

DeleteMessageBatchRequestRequestTypeDef = TypedDict(
    "DeleteMessageBatchRequestRequestTypeDef",
    {
        "QueueUrl": str,
        "Entries": Sequence["DeleteMessageBatchRequestEntryTypeDef"],
    },
)

DeleteMessageBatchResultEntryTypeDef = TypedDict(
    "DeleteMessageBatchResultEntryTypeDef",
    {
        "Id": str,
    },
)

DeleteMessageBatchResultTypeDef = TypedDict(
    "DeleteMessageBatchResultTypeDef",
    {
        "Successful": List["DeleteMessageBatchResultEntryTypeDef"],
        "Failed": List["BatchResultErrorEntryTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteMessageRequestRequestTypeDef = TypedDict(
    "DeleteMessageRequestRequestTypeDef",
    {
        "QueueUrl": str,
        "ReceiptHandle": str,
    },
)

DeleteQueueRequestRequestTypeDef = TypedDict(
    "DeleteQueueRequestRequestTypeDef",
    {
        "QueueUrl": str,
    },
)

_RequiredGetQueueAttributesRequestRequestTypeDef = TypedDict(
    "_RequiredGetQueueAttributesRequestRequestTypeDef",
    {
        "QueueUrl": str,
    },
)
_OptionalGetQueueAttributesRequestRequestTypeDef = TypedDict(
    "_OptionalGetQueueAttributesRequestRequestTypeDef",
    {
        "AttributeNames": Sequence[QueueAttributeNameType],
    },
    total=False,
)


class GetQueueAttributesRequestRequestTypeDef(
    _RequiredGetQueueAttributesRequestRequestTypeDef,
    _OptionalGetQueueAttributesRequestRequestTypeDef,
):
    pass


GetQueueAttributesResultTypeDef = TypedDict(
    "GetQueueAttributesResultTypeDef",
    {
        "Attributes": Dict[QueueAttributeNameType, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGetQueueUrlRequestRequestTypeDef = TypedDict(
    "_RequiredGetQueueUrlRequestRequestTypeDef",
    {
        "QueueName": str,
    },
)
_OptionalGetQueueUrlRequestRequestTypeDef = TypedDict(
    "_OptionalGetQueueUrlRequestRequestTypeDef",
    {
        "QueueOwnerAWSAccountId": str,
    },
    total=False,
)


class GetQueueUrlRequestRequestTypeDef(
    _RequiredGetQueueUrlRequestRequestTypeDef, _OptionalGetQueueUrlRequestRequestTypeDef
):
    pass


_RequiredGetQueueUrlRequestServiceResourceGetQueueByNameTypeDef = TypedDict(
    "_RequiredGetQueueUrlRequestServiceResourceGetQueueByNameTypeDef",
    {
        "QueueName": str,
    },
)
_OptionalGetQueueUrlRequestServiceResourceGetQueueByNameTypeDef = TypedDict(
    "_OptionalGetQueueUrlRequestServiceResourceGetQueueByNameTypeDef",
    {
        "QueueOwnerAWSAccountId": str,
    },
    total=False,
)


class GetQueueUrlRequestServiceResourceGetQueueByNameTypeDef(
    _RequiredGetQueueUrlRequestServiceResourceGetQueueByNameTypeDef,
    _OptionalGetQueueUrlRequestServiceResourceGetQueueByNameTypeDef,
):
    pass


GetQueueUrlResultTypeDef = TypedDict(
    "GetQueueUrlResultTypeDef",
    {
        "QueueUrl": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListDeadLetterSourceQueuesRequestListDeadLetterSourceQueuesPaginateTypeDef = TypedDict(
    "_RequiredListDeadLetterSourceQueuesRequestListDeadLetterSourceQueuesPaginateTypeDef",
    {
        "QueueUrl": str,
    },
)
_OptionalListDeadLetterSourceQueuesRequestListDeadLetterSourceQueuesPaginateTypeDef = TypedDict(
    "_OptionalListDeadLetterSourceQueuesRequestListDeadLetterSourceQueuesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListDeadLetterSourceQueuesRequestListDeadLetterSourceQueuesPaginateTypeDef(
    _RequiredListDeadLetterSourceQueuesRequestListDeadLetterSourceQueuesPaginateTypeDef,
    _OptionalListDeadLetterSourceQueuesRequestListDeadLetterSourceQueuesPaginateTypeDef,
):
    pass


_RequiredListDeadLetterSourceQueuesRequestRequestTypeDef = TypedDict(
    "_RequiredListDeadLetterSourceQueuesRequestRequestTypeDef",
    {
        "QueueUrl": str,
    },
)
_OptionalListDeadLetterSourceQueuesRequestRequestTypeDef = TypedDict(
    "_OptionalListDeadLetterSourceQueuesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListDeadLetterSourceQueuesRequestRequestTypeDef(
    _RequiredListDeadLetterSourceQueuesRequestRequestTypeDef,
    _OptionalListDeadLetterSourceQueuesRequestRequestTypeDef,
):
    pass


ListDeadLetterSourceQueuesResultTypeDef = TypedDict(
    "ListDeadLetterSourceQueuesResultTypeDef",
    {
        "queueUrls": List[str],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListQueueTagsRequestRequestTypeDef = TypedDict(
    "ListQueueTagsRequestRequestTypeDef",
    {
        "QueueUrl": str,
    },
)

ListQueueTagsResultTypeDef = TypedDict(
    "ListQueueTagsResultTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListQueuesRequestListQueuesPaginateTypeDef = TypedDict(
    "ListQueuesRequestListQueuesPaginateTypeDef",
    {
        "QueueNamePrefix": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListQueuesRequestRequestTypeDef = TypedDict(
    "ListQueuesRequestRequestTypeDef",
    {
        "QueueNamePrefix": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListQueuesResultTypeDef = TypedDict(
    "ListQueuesResultTypeDef",
    {
        "QueueUrls": List[str],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredMessageAttributeValueTypeDef = TypedDict(
    "_RequiredMessageAttributeValueTypeDef",
    {
        "DataType": str,
    },
)
_OptionalMessageAttributeValueTypeDef = TypedDict(
    "_OptionalMessageAttributeValueTypeDef",
    {
        "StringValue": str,
        "BinaryValue": bytes,
        "StringListValues": List[str],
        "BinaryListValues": List[bytes],
    },
    total=False,
)


class MessageAttributeValueTypeDef(
    _RequiredMessageAttributeValueTypeDef, _OptionalMessageAttributeValueTypeDef
):
    pass


_RequiredMessageSystemAttributeValueTypeDef = TypedDict(
    "_RequiredMessageSystemAttributeValueTypeDef",
    {
        "DataType": str,
    },
)
_OptionalMessageSystemAttributeValueTypeDef = TypedDict(
    "_OptionalMessageSystemAttributeValueTypeDef",
    {
        "StringValue": str,
        "BinaryValue": Union[str, bytes, IO[Any], StreamingBody],
        "StringListValues": Sequence[str],
        "BinaryListValues": Sequence[Union[str, bytes, IO[Any], StreamingBody]],
    },
    total=False,
)


class MessageSystemAttributeValueTypeDef(
    _RequiredMessageSystemAttributeValueTypeDef, _OptionalMessageSystemAttributeValueTypeDef
):
    pass


MessageTypeDef = TypedDict(
    "MessageTypeDef",
    {
        "MessageId": str,
        "ReceiptHandle": str,
        "MD5OfBody": str,
        "Body": str,
        "Attributes": Dict[MessageSystemAttributeNameType, str],
        "MD5OfMessageAttributes": str,
        "MessageAttributes": Dict[str, "MessageAttributeValueTypeDef"],
    },
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

PurgeQueueRequestRequestTypeDef = TypedDict(
    "PurgeQueueRequestRequestTypeDef",
    {
        "QueueUrl": str,
    },
)

QueueMessageRequestTypeDef = TypedDict(
    "QueueMessageRequestTypeDef",
    {
        "receipt_handle": str,
    },
)

ReceiveMessageRequestQueueReceiveMessagesTypeDef = TypedDict(
    "ReceiveMessageRequestQueueReceiveMessagesTypeDef",
    {
        "AttributeNames": Sequence[QueueAttributeNameType],
        "MessageAttributeNames": Sequence[str],
        "MaxNumberOfMessages": int,
        "VisibilityTimeout": int,
        "WaitTimeSeconds": int,
        "ReceiveRequestAttemptId": str,
    },
    total=False,
)

_RequiredReceiveMessageRequestRequestTypeDef = TypedDict(
    "_RequiredReceiveMessageRequestRequestTypeDef",
    {
        "QueueUrl": str,
    },
)
_OptionalReceiveMessageRequestRequestTypeDef = TypedDict(
    "_OptionalReceiveMessageRequestRequestTypeDef",
    {
        "AttributeNames": Sequence[QueueAttributeNameType],
        "MessageAttributeNames": Sequence[str],
        "MaxNumberOfMessages": int,
        "VisibilityTimeout": int,
        "WaitTimeSeconds": int,
        "ReceiveRequestAttemptId": str,
    },
    total=False,
)


class ReceiveMessageRequestRequestTypeDef(
    _RequiredReceiveMessageRequestRequestTypeDef, _OptionalReceiveMessageRequestRequestTypeDef
):
    pass


ReceiveMessageResultTypeDef = TypedDict(
    "ReceiveMessageResultTypeDef",
    {
        "Messages": List["MessageTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RemovePermissionRequestQueueRemovePermissionTypeDef = TypedDict(
    "RemovePermissionRequestQueueRemovePermissionTypeDef",
    {
        "Label": str,
    },
)

RemovePermissionRequestRequestTypeDef = TypedDict(
    "RemovePermissionRequestRequestTypeDef",
    {
        "QueueUrl": str,
        "Label": str,
    },
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

_RequiredSendMessageBatchRequestEntryTypeDef = TypedDict(
    "_RequiredSendMessageBatchRequestEntryTypeDef",
    {
        "Id": str,
        "MessageBody": str,
    },
)
_OptionalSendMessageBatchRequestEntryTypeDef = TypedDict(
    "_OptionalSendMessageBatchRequestEntryTypeDef",
    {
        "DelaySeconds": int,
        "MessageAttributes": Mapping[str, "MessageAttributeValueTypeDef"],
        "MessageSystemAttributes": Mapping[
            Literal["AWSTraceHeader"], "MessageSystemAttributeValueTypeDef"
        ],
        "MessageDeduplicationId": str,
        "MessageGroupId": str,
    },
    total=False,
)


class SendMessageBatchRequestEntryTypeDef(
    _RequiredSendMessageBatchRequestEntryTypeDef, _OptionalSendMessageBatchRequestEntryTypeDef
):
    pass


SendMessageBatchRequestQueueSendMessagesTypeDef = TypedDict(
    "SendMessageBatchRequestQueueSendMessagesTypeDef",
    {
        "Entries": Sequence["SendMessageBatchRequestEntryTypeDef"],
    },
)

SendMessageBatchRequestRequestTypeDef = TypedDict(
    "SendMessageBatchRequestRequestTypeDef",
    {
        "QueueUrl": str,
        "Entries": Sequence["SendMessageBatchRequestEntryTypeDef"],
    },
)

_RequiredSendMessageBatchResultEntryTypeDef = TypedDict(
    "_RequiredSendMessageBatchResultEntryTypeDef",
    {
        "Id": str,
        "MessageId": str,
        "MD5OfMessageBody": str,
    },
)
_OptionalSendMessageBatchResultEntryTypeDef = TypedDict(
    "_OptionalSendMessageBatchResultEntryTypeDef",
    {
        "MD5OfMessageAttributes": str,
        "MD5OfMessageSystemAttributes": str,
        "SequenceNumber": str,
    },
    total=False,
)


class SendMessageBatchResultEntryTypeDef(
    _RequiredSendMessageBatchResultEntryTypeDef, _OptionalSendMessageBatchResultEntryTypeDef
):
    pass


SendMessageBatchResultTypeDef = TypedDict(
    "SendMessageBatchResultTypeDef",
    {
        "Successful": List["SendMessageBatchResultEntryTypeDef"],
        "Failed": List["BatchResultErrorEntryTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredSendMessageRequestQueueSendMessageTypeDef = TypedDict(
    "_RequiredSendMessageRequestQueueSendMessageTypeDef",
    {
        "MessageBody": str,
    },
)
_OptionalSendMessageRequestQueueSendMessageTypeDef = TypedDict(
    "_OptionalSendMessageRequestQueueSendMessageTypeDef",
    {
        "DelaySeconds": int,
        "MessageAttributes": Mapping[str, "MessageAttributeValueTypeDef"],
        "MessageSystemAttributes": Mapping[
            Literal["AWSTraceHeader"], "MessageSystemAttributeValueTypeDef"
        ],
        "MessageDeduplicationId": str,
        "MessageGroupId": str,
    },
    total=False,
)


class SendMessageRequestQueueSendMessageTypeDef(
    _RequiredSendMessageRequestQueueSendMessageTypeDef,
    _OptionalSendMessageRequestQueueSendMessageTypeDef,
):
    pass


_RequiredSendMessageRequestRequestTypeDef = TypedDict(
    "_RequiredSendMessageRequestRequestTypeDef",
    {
        "QueueUrl": str,
        "MessageBody": str,
    },
)
_OptionalSendMessageRequestRequestTypeDef = TypedDict(
    "_OptionalSendMessageRequestRequestTypeDef",
    {
        "DelaySeconds": int,
        "MessageAttributes": Mapping[str, "MessageAttributeValueTypeDef"],
        "MessageSystemAttributes": Mapping[
            Literal["AWSTraceHeader"], "MessageSystemAttributeValueTypeDef"
        ],
        "MessageDeduplicationId": str,
        "MessageGroupId": str,
    },
    total=False,
)


class SendMessageRequestRequestTypeDef(
    _RequiredSendMessageRequestRequestTypeDef, _OptionalSendMessageRequestRequestTypeDef
):
    pass


SendMessageResultTypeDef = TypedDict(
    "SendMessageResultTypeDef",
    {
        "MD5OfMessageBody": str,
        "MD5OfMessageAttributes": str,
        "MD5OfMessageSystemAttributes": str,
        "MessageId": str,
        "SequenceNumber": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ServiceResourceMessageRequestTypeDef = TypedDict(
    "ServiceResourceMessageRequestTypeDef",
    {
        "queue_url": str,
        "receipt_handle": str,
    },
)

ServiceResourceQueueRequestTypeDef = TypedDict(
    "ServiceResourceQueueRequestTypeDef",
    {
        "url": str,
    },
)

SetQueueAttributesRequestQueueSetAttributesTypeDef = TypedDict(
    "SetQueueAttributesRequestQueueSetAttributesTypeDef",
    {
        "Attributes": Mapping[QueueAttributeNameType, str],
    },
)

SetQueueAttributesRequestRequestTypeDef = TypedDict(
    "SetQueueAttributesRequestRequestTypeDef",
    {
        "QueueUrl": str,
        "Attributes": Mapping[QueueAttributeNameType, str],
    },
)

TagQueueRequestRequestTypeDef = TypedDict(
    "TagQueueRequestRequestTypeDef",
    {
        "QueueUrl": str,
        "Tags": Mapping[str, str],
    },
)

UntagQueueRequestRequestTypeDef = TypedDict(
    "UntagQueueRequestRequestTypeDef",
    {
        "QueueUrl": str,
        "TagKeys": Sequence[str],
    },
)
