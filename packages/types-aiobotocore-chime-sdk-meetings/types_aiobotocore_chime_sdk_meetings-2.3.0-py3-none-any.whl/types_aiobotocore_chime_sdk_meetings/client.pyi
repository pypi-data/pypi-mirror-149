"""
Type annotations for chime-sdk-meetings service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_chime_sdk_meetings.client import ChimeSDKMeetingsClient

    session = get_session()
    async with session.create_client("chime-sdk-meetings") as client:
        client: ChimeSDKMeetingsClient
    ```
"""
from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .type_defs import (
    BatchCreateAttendeeResponseTypeDef,
    CreateAttendeeRequestItemTypeDef,
    CreateAttendeeResponseTypeDef,
    CreateMeetingResponseTypeDef,
    CreateMeetingWithAttendeesResponseTypeDef,
    GetAttendeeResponseTypeDef,
    GetMeetingResponseTypeDef,
    ListAttendeesResponseTypeDef,
    MeetingFeaturesConfigurationTypeDef,
    NotificationsConfigurationTypeDef,
    TranscriptionConfigurationTypeDef,
)

__all__ = ("ChimeSDKMeetingsClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]
    UnprocessableEntityException: Type[BotocoreClientError]

class ChimeSDKMeetingsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ChimeSDKMeetingsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#exceptions)
        """
    async def batch_create_attendee(
        self, *, MeetingId: str, Attendees: Sequence["CreateAttendeeRequestItemTypeDef"]
    ) -> BatchCreateAttendeeResponseTypeDef:
        """
        Creates up to 100 attendees for an active Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client.batch_create_attendee)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#batch_create_attendee)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#can_paginate)
        """
    async def create_attendee(
        self, *, MeetingId: str, ExternalUserId: str
    ) -> CreateAttendeeResponseTypeDef:
        """
        Creates a new attendee for an active Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client.create_attendee)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#create_attendee)
        """
    async def create_meeting(
        self,
        *,
        ClientRequestToken: str,
        MediaRegion: str,
        ExternalMeetingId: str,
        MeetingHostId: str = ...,
        NotificationsConfiguration: "NotificationsConfigurationTypeDef" = ...,
        MeetingFeatures: "MeetingFeaturesConfigurationTypeDef" = ...
    ) -> CreateMeetingResponseTypeDef:
        """
        Creates a new Amazon Chime SDK meeting in the specified media Region with no
        initial attendees.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client.create_meeting)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#create_meeting)
        """
    async def create_meeting_with_attendees(
        self,
        *,
        ClientRequestToken: str,
        MediaRegion: str,
        ExternalMeetingId: str,
        Attendees: Sequence["CreateAttendeeRequestItemTypeDef"],
        MeetingHostId: str = ...,
        MeetingFeatures: "MeetingFeaturesConfigurationTypeDef" = ...,
        NotificationsConfiguration: "NotificationsConfigurationTypeDef" = ...
    ) -> CreateMeetingWithAttendeesResponseTypeDef:
        """
        Creates a new Amazon Chime SDK meeting in the specified media Region, with
        attendees.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client.create_meeting_with_attendees)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#create_meeting_with_attendees)
        """
    async def delete_attendee(self, *, MeetingId: str, AttendeeId: str) -> None:
        """
        Deletes an attendee from the specified Amazon Chime SDK meeting and deletes
        their `JoinToken`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client.delete_attendee)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#delete_attendee)
        """
    async def delete_meeting(self, *, MeetingId: str) -> None:
        """
        Deletes the specified Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client.delete_meeting)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#delete_meeting)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#generate_presigned_url)
        """
    async def get_attendee(self, *, MeetingId: str, AttendeeId: str) -> GetAttendeeResponseTypeDef:
        """
        Gets the Amazon Chime SDK attendee details for a specified meeting ID and
        attendee ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client.get_attendee)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#get_attendee)
        """
    async def get_meeting(self, *, MeetingId: str) -> GetMeetingResponseTypeDef:
        """
        Gets the Amazon Chime SDK meeting details for the specified meeting ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client.get_meeting)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#get_meeting)
        """
    async def list_attendees(
        self, *, MeetingId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListAttendeesResponseTypeDef:
        """
        Lists the attendees for the specified Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client.list_attendees)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#list_attendees)
        """
    async def start_meeting_transcription(
        self, *, MeetingId: str, TranscriptionConfiguration: "TranscriptionConfigurationTypeDef"
    ) -> None:
        """
        Starts transcription for the specified `meetingId` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client.start_meeting_transcription)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#start_meeting_transcription)
        """
    async def stop_meeting_transcription(self, *, MeetingId: str) -> None:
        """
        Stops transcription for the specified `meetingId` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client.stop_meeting_transcription)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/#stop_meeting_transcription)
        """
    async def __aenter__(self) -> "ChimeSDKMeetingsClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime-sdk-meetings.html#ChimeSDKMeetings.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_meetings/client/)
        """
