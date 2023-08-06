"""
Type annotations for connectparticipant service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_connectparticipant.client import ConnectParticipantClient

    session = get_session()
    async with session.create_client("connectparticipant") as client:
        client: ConnectParticipantClient
    ```
"""
from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import ConnectionTypeType, ScanDirectionType, SortKeyType
from .type_defs import (
    CreateParticipantConnectionResponseTypeDef,
    GetAttachmentResponseTypeDef,
    GetTranscriptResponseTypeDef,
    SendEventResponseTypeDef,
    SendMessageResponseTypeDef,
    StartAttachmentUploadResponseTypeDef,
    StartPositionTypeDef,
)

__all__ = ("ConnectParticipantClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class ConnectParticipantClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant.html#ConnectParticipant.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ConnectParticipantClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant.html#ConnectParticipant.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant.html#ConnectParticipant.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/#can_paginate)
        """

    async def complete_attachment_upload(
        self, *, AttachmentIds: Sequence[str], ClientToken: str, ConnectionToken: str
    ) -> Dict[str, Any]:
        """
        Allows you to confirm that the attachment has been uploaded using the pre-signed
        URL provided in StartAttachmentUpload API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant.html#ConnectParticipant.Client.complete_attachment_upload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/#complete_attachment_upload)
        """

    async def create_participant_connection(
        self,
        *,
        Type: Sequence[ConnectionTypeType],
        ParticipantToken: str,
        ConnectParticipant: bool = ...
    ) -> CreateParticipantConnectionResponseTypeDef:
        """
        Creates the participant's connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant.html#ConnectParticipant.Client.create_participant_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/#create_participant_connection)
        """

    async def disconnect_participant(
        self, *, ConnectionToken: str, ClientToken: str = ...
    ) -> Dict[str, Any]:
        """
        Disconnects a participant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant.html#ConnectParticipant.Client.disconnect_participant)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/#disconnect_participant)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant.html#ConnectParticipant.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/#generate_presigned_url)
        """

    async def get_attachment(
        self, *, AttachmentId: str, ConnectionToken: str
    ) -> GetAttachmentResponseTypeDef:
        """
        Provides a pre-signed URL for download of a completed attachment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant.html#ConnectParticipant.Client.get_attachment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/#get_attachment)
        """

    async def get_transcript(
        self,
        *,
        ConnectionToken: str,
        ContactId: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        ScanDirection: ScanDirectionType = ...,
        SortOrder: SortKeyType = ...,
        StartPosition: "StartPositionTypeDef" = ...
    ) -> GetTranscriptResponseTypeDef:
        """
        Retrieves a transcript of the session, including details about any attachments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant.html#ConnectParticipant.Client.get_transcript)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/#get_transcript)
        """

    async def send_event(
        self, *, ContentType: str, ConnectionToken: str, Content: str = ..., ClientToken: str = ...
    ) -> SendEventResponseTypeDef:
        """
        Sends an event.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant.html#ConnectParticipant.Client.send_event)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/#send_event)
        """

    async def send_message(
        self, *, ContentType: str, Content: str, ConnectionToken: str, ClientToken: str = ...
    ) -> SendMessageResponseTypeDef:
        """
        Sends a message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant.html#ConnectParticipant.Client.send_message)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/#send_message)
        """

    async def start_attachment_upload(
        self,
        *,
        ContentType: str,
        AttachmentSizeInBytes: int,
        AttachmentName: str,
        ClientToken: str,
        ConnectionToken: str
    ) -> StartAttachmentUploadResponseTypeDef:
        """
        Provides a pre-signed Amazon S3 URL in response for uploading the file directly
        to S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant.html#ConnectParticipant.Client.start_attachment_upload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/#start_attachment_upload)
        """

    async def __aenter__(self) -> "ConnectParticipantClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant.html#ConnectParticipant.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant.html#ConnectParticipant.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/)
        """
