"""
Type annotations for chime service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_chime.client import ChimeClient

    session = get_session()
    async with session.create_client("chime") as client:
        client: ChimeClient
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    CapabilityType,
    ChannelMembershipTypeType,
    ChannelMessagePersistenceTypeType,
    ChannelMessageTypeType,
    ChannelModeType,
    ChannelPrivacyType,
    GeoMatchLevelType,
    LicenseType,
    NumberSelectionBehaviorType,
    PhoneNumberAssociationNameType,
    PhoneNumberProductTypeType,
    PhoneNumberStatusType,
    PhoneNumberTypeType,
    ProxySessionStatusType,
    RoomMembershipRoleType,
    SipRuleTriggerTypeType,
    SortOrderType,
    UserTypeType,
    VoiceConnectorAwsRegionType,
)
from .paginator import ListAccountsPaginator, ListUsersPaginator
from .type_defs import (
    AccountSettingsTypeDef,
    AlexaForBusinessMetadataTypeDef,
    AppInstanceRetentionSettingsTypeDef,
    AppInstanceStreamingConfigurationTypeDef,
    AssociatePhoneNumbersWithVoiceConnectorGroupResponseTypeDef,
    AssociatePhoneNumbersWithVoiceConnectorResponseTypeDef,
    BatchCreateAttendeeResponseTypeDef,
    BatchCreateChannelMembershipResponseTypeDef,
    BatchCreateRoomMembershipResponseTypeDef,
    BatchDeletePhoneNumberResponseTypeDef,
    BatchSuspendUserResponseTypeDef,
    BatchUnsuspendUserResponseTypeDef,
    BatchUpdatePhoneNumberResponseTypeDef,
    BatchUpdateUserResponseTypeDef,
    BusinessCallingSettingsTypeDef,
    ChimeSdkMeetingConfigurationTypeDef,
    CreateAccountResponseTypeDef,
    CreateAppInstanceAdminResponseTypeDef,
    CreateAppInstanceResponseTypeDef,
    CreateAppInstanceUserResponseTypeDef,
    CreateAttendeeRequestItemTypeDef,
    CreateAttendeeResponseTypeDef,
    CreateBotResponseTypeDef,
    CreateChannelBanResponseTypeDef,
    CreateChannelMembershipResponseTypeDef,
    CreateChannelModeratorResponseTypeDef,
    CreateChannelResponseTypeDef,
    CreateMediaCapturePipelineResponseTypeDef,
    CreateMeetingDialOutResponseTypeDef,
    CreateMeetingResponseTypeDef,
    CreateMeetingWithAttendeesResponseTypeDef,
    CreatePhoneNumberOrderResponseTypeDef,
    CreateProxySessionResponseTypeDef,
    CreateRoomMembershipResponseTypeDef,
    CreateRoomResponseTypeDef,
    CreateSipMediaApplicationCallResponseTypeDef,
    CreateSipMediaApplicationResponseTypeDef,
    CreateSipRuleResponseTypeDef,
    CreateUserResponseTypeDef,
    CreateVoiceConnectorGroupResponseTypeDef,
    CreateVoiceConnectorResponseTypeDef,
    CredentialTypeDef,
    DescribeAppInstanceAdminResponseTypeDef,
    DescribeAppInstanceResponseTypeDef,
    DescribeAppInstanceUserResponseTypeDef,
    DescribeChannelBanResponseTypeDef,
    DescribeChannelMembershipForAppInstanceUserResponseTypeDef,
    DescribeChannelMembershipResponseTypeDef,
    DescribeChannelModeratedByAppInstanceUserResponseTypeDef,
    DescribeChannelModeratorResponseTypeDef,
    DescribeChannelResponseTypeDef,
    DisassociatePhoneNumbersFromVoiceConnectorGroupResponseTypeDef,
    DisassociatePhoneNumbersFromVoiceConnectorResponseTypeDef,
    EmergencyCallingConfigurationTypeDef,
    GeoMatchParamsTypeDef,
    GetAccountResponseTypeDef,
    GetAccountSettingsResponseTypeDef,
    GetAppInstanceRetentionSettingsResponseTypeDef,
    GetAppInstanceStreamingConfigurationsResponseTypeDef,
    GetAttendeeResponseTypeDef,
    GetBotResponseTypeDef,
    GetChannelMessageResponseTypeDef,
    GetEventsConfigurationResponseTypeDef,
    GetGlobalSettingsResponseTypeDef,
    GetMediaCapturePipelineResponseTypeDef,
    GetMeetingResponseTypeDef,
    GetMessagingSessionEndpointResponseTypeDef,
    GetPhoneNumberOrderResponseTypeDef,
    GetPhoneNumberResponseTypeDef,
    GetPhoneNumberSettingsResponseTypeDef,
    GetProxySessionResponseTypeDef,
    GetRetentionSettingsResponseTypeDef,
    GetRoomResponseTypeDef,
    GetSipMediaApplicationLoggingConfigurationResponseTypeDef,
    GetSipMediaApplicationResponseTypeDef,
    GetSipRuleResponseTypeDef,
    GetUserResponseTypeDef,
    GetUserSettingsResponseTypeDef,
    GetVoiceConnectorEmergencyCallingConfigurationResponseTypeDef,
    GetVoiceConnectorGroupResponseTypeDef,
    GetVoiceConnectorLoggingConfigurationResponseTypeDef,
    GetVoiceConnectorOriginationResponseTypeDef,
    GetVoiceConnectorProxyResponseTypeDef,
    GetVoiceConnectorResponseTypeDef,
    GetVoiceConnectorStreamingConfigurationResponseTypeDef,
    GetVoiceConnectorTerminationHealthResponseTypeDef,
    GetVoiceConnectorTerminationResponseTypeDef,
    InviteUsersResponseTypeDef,
    ListAccountsResponseTypeDef,
    ListAppInstanceAdminsResponseTypeDef,
    ListAppInstancesResponseTypeDef,
    ListAppInstanceUsersResponseTypeDef,
    ListAttendeesResponseTypeDef,
    ListAttendeeTagsResponseTypeDef,
    ListBotsResponseTypeDef,
    ListChannelBansResponseTypeDef,
    ListChannelMembershipsForAppInstanceUserResponseTypeDef,
    ListChannelMembershipsResponseTypeDef,
    ListChannelMessagesResponseTypeDef,
    ListChannelModeratorsResponseTypeDef,
    ListChannelsModeratedByAppInstanceUserResponseTypeDef,
    ListChannelsResponseTypeDef,
    ListMediaCapturePipelinesResponseTypeDef,
    ListMeetingsResponseTypeDef,
    ListMeetingTagsResponseTypeDef,
    ListPhoneNumberOrdersResponseTypeDef,
    ListPhoneNumbersResponseTypeDef,
    ListProxySessionsResponseTypeDef,
    ListRoomMembershipsResponseTypeDef,
    ListRoomsResponseTypeDef,
    ListSipMediaApplicationsResponseTypeDef,
    ListSipRulesResponseTypeDef,
    ListSupportedPhoneNumberCountriesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListUsersResponseTypeDef,
    ListVoiceConnectorGroupsResponseTypeDef,
    ListVoiceConnectorsResponseTypeDef,
    ListVoiceConnectorTerminationCredentialsResponseTypeDef,
    LoggingConfigurationTypeDef,
    MeetingNotificationConfigurationTypeDef,
    MembershipItemTypeDef,
    OriginationTypeDef,
    PutAppInstanceRetentionSettingsResponseTypeDef,
    PutAppInstanceStreamingConfigurationsResponseTypeDef,
    PutEventsConfigurationResponseTypeDef,
    PutRetentionSettingsResponseTypeDef,
    PutSipMediaApplicationLoggingConfigurationResponseTypeDef,
    PutVoiceConnectorEmergencyCallingConfigurationResponseTypeDef,
    PutVoiceConnectorLoggingConfigurationResponseTypeDef,
    PutVoiceConnectorOriginationResponseTypeDef,
    PutVoiceConnectorProxyResponseTypeDef,
    PutVoiceConnectorStreamingConfigurationResponseTypeDef,
    PutVoiceConnectorTerminationResponseTypeDef,
    RedactChannelMessageResponseTypeDef,
    RegenerateSecurityTokenResponseTypeDef,
    ResetPersonalPINResponseTypeDef,
    RestorePhoneNumberResponseTypeDef,
    RetentionSettingsTypeDef,
    SearchAvailablePhoneNumbersResponseTypeDef,
    SendChannelMessageResponseTypeDef,
    SigninDelegateGroupTypeDef,
    SipMediaApplicationEndpointTypeDef,
    SipMediaApplicationLoggingConfigurationTypeDef,
    SipRuleTargetApplicationTypeDef,
    StreamingConfigurationTypeDef,
    TagTypeDef,
    TerminationTypeDef,
    TranscriptionConfigurationTypeDef,
    UpdateAccountResponseTypeDef,
    UpdateAppInstanceResponseTypeDef,
    UpdateAppInstanceUserResponseTypeDef,
    UpdateBotResponseTypeDef,
    UpdateChannelMessageResponseTypeDef,
    UpdateChannelReadMarkerResponseTypeDef,
    UpdateChannelResponseTypeDef,
    UpdatePhoneNumberRequestItemTypeDef,
    UpdatePhoneNumberResponseTypeDef,
    UpdateProxySessionResponseTypeDef,
    UpdateRoomMembershipResponseTypeDef,
    UpdateRoomResponseTypeDef,
    UpdateSipMediaApplicationCallResponseTypeDef,
    UpdateSipMediaApplicationResponseTypeDef,
    UpdateSipRuleResponseTypeDef,
    UpdateUserRequestItemTypeDef,
    UpdateUserResponseTypeDef,
    UpdateVoiceConnectorGroupResponseTypeDef,
    UpdateVoiceConnectorResponseTypeDef,
    UserSettingsTypeDef,
    VoiceConnectorItemTypeDef,
    VoiceConnectorSettingsTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ChimeClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ResourceLimitExceededException: Type[BotocoreClientError]
    ServiceFailureException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottledClientException: Type[BotocoreClientError]
    UnauthorizedClientException: Type[BotocoreClientError]
    UnprocessableEntityException: Type[BotocoreClientError]


class ChimeClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ChimeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#exceptions)
        """

    async def associate_phone_number_with_user(
        self, *, AccountId: str, UserId: str, E164PhoneNumber: str
    ) -> Dict[str, Any]:
        """
        Associates a phone number with the specified Amazon Chime user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.associate_phone_number_with_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#associate_phone_number_with_user)
        """

    async def associate_phone_numbers_with_voice_connector(
        self, *, VoiceConnectorId: str, E164PhoneNumbers: Sequence[str], ForceAssociate: bool = ...
    ) -> AssociatePhoneNumbersWithVoiceConnectorResponseTypeDef:
        """
        Associates phone numbers with the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.associate_phone_numbers_with_voice_connector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#associate_phone_numbers_with_voice_connector)
        """

    async def associate_phone_numbers_with_voice_connector_group(
        self,
        *,
        VoiceConnectorGroupId: str,
        E164PhoneNumbers: Sequence[str],
        ForceAssociate: bool = ...
    ) -> AssociatePhoneNumbersWithVoiceConnectorGroupResponseTypeDef:
        """
        Associates phone numbers with the specified Amazon Chime Voice Connector group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.associate_phone_numbers_with_voice_connector_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#associate_phone_numbers_with_voice_connector_group)
        """

    async def associate_signin_delegate_groups_with_account(
        self, *, AccountId: str, SigninDelegateGroups: Sequence["SigninDelegateGroupTypeDef"]
    ) -> Dict[str, Any]:
        """
        Associates the specified sign-in delegate groups with the specified Amazon Chime
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.associate_signin_delegate_groups_with_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#associate_signin_delegate_groups_with_account)
        """

    async def batch_create_attendee(
        self, *, MeetingId: str, Attendees: Sequence["CreateAttendeeRequestItemTypeDef"]
    ) -> BatchCreateAttendeeResponseTypeDef:
        """
        Creates up to 100 new attendees for an active Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.batch_create_attendee)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#batch_create_attendee)
        """

    async def batch_create_channel_membership(
        self,
        *,
        ChannelArn: str,
        MemberArns: Sequence[str],
        Type: ChannelMembershipTypeType = ...,
        ChimeBearer: str = ...
    ) -> BatchCreateChannelMembershipResponseTypeDef:
        """
        Adds a specified number of users to a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.batch_create_channel_membership)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#batch_create_channel_membership)
        """

    async def batch_create_room_membership(
        self, *, AccountId: str, RoomId: str, MembershipItemList: Sequence["MembershipItemTypeDef"]
    ) -> BatchCreateRoomMembershipResponseTypeDef:
        """
        Adds up to 50 members to a chat room in an Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.batch_create_room_membership)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#batch_create_room_membership)
        """

    async def batch_delete_phone_number(
        self, *, PhoneNumberIds: Sequence[str]
    ) -> BatchDeletePhoneNumberResponseTypeDef:
        """
        Moves phone numbers into the **Deletion queue**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.batch_delete_phone_number)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#batch_delete_phone_number)
        """

    async def batch_suspend_user(
        self, *, AccountId: str, UserIdList: Sequence[str]
    ) -> BatchSuspendUserResponseTypeDef:
        """
        Suspends up to 50 users from a `Team` or `EnterpriseLWA` Amazon Chime account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.batch_suspend_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#batch_suspend_user)
        """

    async def batch_unsuspend_user(
        self, *, AccountId: str, UserIdList: Sequence[str]
    ) -> BatchUnsuspendUserResponseTypeDef:
        """
        Removes the suspension from up to 50 previously suspended users for the
        specified Amazon Chime `EnterpriseLWA` account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.batch_unsuspend_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#batch_unsuspend_user)
        """

    async def batch_update_phone_number(
        self, *, UpdatePhoneNumberRequestItems: Sequence["UpdatePhoneNumberRequestItemTypeDef"]
    ) -> BatchUpdatePhoneNumberResponseTypeDef:
        """
        Updates phone number product types or calling names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.batch_update_phone_number)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#batch_update_phone_number)
        """

    async def batch_update_user(
        self, *, AccountId: str, UpdateUserRequestItems: Sequence["UpdateUserRequestItemTypeDef"]
    ) -> BatchUpdateUserResponseTypeDef:
        """
        Updates user details within the  UpdateUserRequestItem object for up to 20 users
        for the specified Amazon Chime account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.batch_update_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#batch_update_user)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#can_paginate)
        """

    async def create_account(self, *, Name: str) -> CreateAccountResponseTypeDef:
        """
        Creates an Amazon Chime account under the administrator's AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.create_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#create_account)
        """

    async def create_app_instance(
        self,
        *,
        Name: str,
        ClientRequestToken: str,
        Metadata: str = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateAppInstanceResponseTypeDef:
        """
        Creates an Amazon Chime SDK messaging `AppInstance` under an AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.create_app_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#create_app_instance)
        """

    async def create_app_instance_admin(
        self, *, AppInstanceAdminArn: str, AppInstanceArn: str
    ) -> CreateAppInstanceAdminResponseTypeDef:
        """
        Promotes an `AppInstanceUser` to an `AppInstanceAdmin`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.create_app_instance_admin)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#create_app_instance_admin)
        """

    async def create_app_instance_user(
        self,
        *,
        AppInstanceArn: str,
        AppInstanceUserId: str,
        Name: str,
        ClientRequestToken: str,
        Metadata: str = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateAppInstanceUserResponseTypeDef:
        """
        Creates a user under an Amazon Chime `AppInstance`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.create_app_instance_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#create_app_instance_user)
        """

    async def create_attendee(
        self, *, MeetingId: str, ExternalUserId: str, Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateAttendeeResponseTypeDef:
        """
        Creates a new attendee for an active Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.create_attendee)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#create_attendee)
        """

    async def create_bot(
        self, *, AccountId: str, DisplayName: str, Domain: str = ...
    ) -> CreateBotResponseTypeDef:
        """
        Creates a bot for an Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.create_bot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#create_bot)
        """

    async def create_channel(
        self,
        *,
        AppInstanceArn: str,
        Name: str,
        ClientRequestToken: str,
        Mode: ChannelModeType = ...,
        Privacy: ChannelPrivacyType = ...,
        Metadata: str = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        ChimeBearer: str = ...
    ) -> CreateChannelResponseTypeDef:
        """
        Creates a channel to which you can add users and send messages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.create_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#create_channel)
        """

    async def create_channel_ban(
        self, *, ChannelArn: str, MemberArn: str, ChimeBearer: str = ...
    ) -> CreateChannelBanResponseTypeDef:
        """
        Permanently bans a member from a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.create_channel_ban)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#create_channel_ban)
        """

    async def create_channel_membership(
        self,
        *,
        ChannelArn: str,
        MemberArn: str,
        Type: ChannelMembershipTypeType,
        ChimeBearer: str = ...
    ) -> CreateChannelMembershipResponseTypeDef:
        """
        Adds a user to a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.create_channel_membership)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#create_channel_membership)
        """

    async def create_channel_moderator(
        self, *, ChannelArn: str, ChannelModeratorArn: str, ChimeBearer: str = ...
    ) -> CreateChannelModeratorResponseTypeDef:
        """
        Creates a new `ChannelModerator`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.create_channel_moderator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#create_channel_moderator)
        """

    async def create_media_capture_pipeline(
        self,
        *,
        SourceType: Literal["ChimeSdkMeeting"],
        SourceArn: str,
        SinkType: Literal["S3Bucket"],
        SinkArn: str,
        ClientRequestToken: str = ...,
        ChimeSdkMeetingConfiguration: "ChimeSdkMeetingConfigurationTypeDef" = ...
    ) -> CreateMediaCapturePipelineResponseTypeDef:
        """
        Creates a media capture pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.create_media_capture_pipeline)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#create_media_capture_pipeline)
        """

    async def create_meeting(
        self,
        *,
        ClientRequestToken: str,
        ExternalMeetingId: str = ...,
        MeetingHostId: str = ...,
        MediaRegion: str = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        NotificationsConfiguration: "MeetingNotificationConfigurationTypeDef" = ...
    ) -> CreateMeetingResponseTypeDef:
        """
        Creates a new Amazon Chime SDK meeting in the specified media Region with no
        initial attendees.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.create_meeting)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#create_meeting)
        """

    async def create_meeting_dial_out(
        self, *, MeetingId: str, FromPhoneNumber: str, ToPhoneNumber: str, JoinToken: str
    ) -> CreateMeetingDialOutResponseTypeDef:
        """
        Uses the join token and call metadata in a meeting request (From number, To
        number, and so forth) to initiate an outbound call to a public switched
        telephone network (PSTN) and join them into a Chime meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.create_meeting_dial_out)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#create_meeting_dial_out)
        """

    async def create_meeting_with_attendees(
        self,
        *,
        ClientRequestToken: str,
        ExternalMeetingId: str = ...,
        MeetingHostId: str = ...,
        MediaRegion: str = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        NotificationsConfiguration: "MeetingNotificationConfigurationTypeDef" = ...,
        Attendees: Sequence["CreateAttendeeRequestItemTypeDef"] = ...
    ) -> CreateMeetingWithAttendeesResponseTypeDef:
        """
        Creates a new Amazon Chime SDK meeting in the specified media Region, with
        attendees.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.create_meeting_with_attendees)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#create_meeting_with_attendees)
        """

    async def create_phone_number_order(
        self, *, ProductType: PhoneNumberProductTypeType, E164PhoneNumbers: Sequence[str]
    ) -> CreatePhoneNumberOrderResponseTypeDef:
        """
        Creates an order for phone numbers to be provisioned.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.create_phone_number_order)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#create_phone_number_order)
        """

    async def create_proxy_session(
        self,
        *,
        VoiceConnectorId: str,
        ParticipantPhoneNumbers: Sequence[str],
        Capabilities: Sequence[CapabilityType],
        Name: str = ...,
        ExpiryMinutes: int = ...,
        NumberSelectionBehavior: NumberSelectionBehaviorType = ...,
        GeoMatchLevel: GeoMatchLevelType = ...,
        GeoMatchParams: "GeoMatchParamsTypeDef" = ...
    ) -> CreateProxySessionResponseTypeDef:
        """
        Creates a proxy session on the specified Amazon Chime Voice Connector for the
        specified participant phone numbers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.create_proxy_session)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#create_proxy_session)
        """

    async def create_room(
        self, *, AccountId: str, Name: str, ClientRequestToken: str = ...
    ) -> CreateRoomResponseTypeDef:
        """
        Creates a chat room for the specified Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.create_room)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#create_room)
        """

    async def create_room_membership(
        self, *, AccountId: str, RoomId: str, MemberId: str, Role: RoomMembershipRoleType = ...
    ) -> CreateRoomMembershipResponseTypeDef:
        """
        Adds a member to a chat room in an Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.create_room_membership)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#create_room_membership)
        """

    async def create_sip_media_application(
        self,
        *,
        AwsRegion: str,
        Name: str,
        Endpoints: Sequence["SipMediaApplicationEndpointTypeDef"]
    ) -> CreateSipMediaApplicationResponseTypeDef:
        """
        Creates a SIP media application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.create_sip_media_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#create_sip_media_application)
        """

    async def create_sip_media_application_call(
        self,
        *,
        FromPhoneNumber: str,
        ToPhoneNumber: str,
        SipMediaApplicationId: str,
        SipHeaders: Mapping[str, str] = ...
    ) -> CreateSipMediaApplicationCallResponseTypeDef:
        """
        Creates an outbound call to a phone number from the phone number specified in
        the request, and it invokes the endpoint of the specified
        `sipMediaApplicationId` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.create_sip_media_application_call)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#create_sip_media_application_call)
        """

    async def create_sip_rule(
        self,
        *,
        Name: str,
        TriggerType: SipRuleTriggerTypeType,
        TriggerValue: str,
        TargetApplications: Sequence["SipRuleTargetApplicationTypeDef"],
        Disabled: bool = ...
    ) -> CreateSipRuleResponseTypeDef:
        """
        Creates a SIP rule which can be used to run a SIP media application as a target
        for a specific trigger type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.create_sip_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#create_sip_rule)
        """

    async def create_user(
        self, *, AccountId: str, Username: str = ..., Email: str = ..., UserType: UserTypeType = ...
    ) -> CreateUserResponseTypeDef:
        """
        Creates a user under the specified Amazon Chime account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.create_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#create_user)
        """

    async def create_voice_connector(
        self, *, Name: str, RequireEncryption: bool, AwsRegion: VoiceConnectorAwsRegionType = ...
    ) -> CreateVoiceConnectorResponseTypeDef:
        """
        Creates an Amazon Chime Voice Connector under the administrator's AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.create_voice_connector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#create_voice_connector)
        """

    async def create_voice_connector_group(
        self, *, Name: str, VoiceConnectorItems: Sequence["VoiceConnectorItemTypeDef"] = ...
    ) -> CreateVoiceConnectorGroupResponseTypeDef:
        """
        Creates an Amazon Chime Voice Connector group under the administrator's AWS
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.create_voice_connector_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#create_voice_connector_group)
        """

    async def delete_account(self, *, AccountId: str) -> Dict[str, Any]:
        """
        Deletes the specified Amazon Chime account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.delete_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#delete_account)
        """

    async def delete_app_instance(self, *, AppInstanceArn: str) -> None:
        """
        Deletes an `AppInstance` and all associated data asynchronously.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.delete_app_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#delete_app_instance)
        """

    async def delete_app_instance_admin(
        self, *, AppInstanceAdminArn: str, AppInstanceArn: str
    ) -> None:
        """
        Demotes an `AppInstanceAdmin` to an `AppInstanceUser`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.delete_app_instance_admin)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#delete_app_instance_admin)
        """

    async def delete_app_instance_streaming_configurations(self, *, AppInstanceArn: str) -> None:
        """
        Deletes the streaming configurations of an `AppInstance` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.delete_app_instance_streaming_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#delete_app_instance_streaming_configurations)
        """

    async def delete_app_instance_user(self, *, AppInstanceUserArn: str) -> None:
        """
        Deletes an `AppInstanceUser` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.delete_app_instance_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#delete_app_instance_user)
        """

    async def delete_attendee(self, *, MeetingId: str, AttendeeId: str) -> None:
        """
        Deletes an attendee from the specified Amazon Chime SDK meeting and deletes
        their `JoinToken`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.delete_attendee)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#delete_attendee)
        """

    async def delete_channel(self, *, ChannelArn: str, ChimeBearer: str = ...) -> None:
        """
        Immediately makes a channel and its memberships inaccessible and marks them for
        deletion.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.delete_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#delete_channel)
        """

    async def delete_channel_ban(
        self, *, ChannelArn: str, MemberArn: str, ChimeBearer: str = ...
    ) -> None:
        """
        Removes a user from a channel's ban list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.delete_channel_ban)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#delete_channel_ban)
        """

    async def delete_channel_membership(
        self, *, ChannelArn: str, MemberArn: str, ChimeBearer: str = ...
    ) -> None:
        """
        Removes a member from a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.delete_channel_membership)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#delete_channel_membership)
        """

    async def delete_channel_message(
        self, *, ChannelArn: str, MessageId: str, ChimeBearer: str = ...
    ) -> None:
        """
        Deletes a channel message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.delete_channel_message)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#delete_channel_message)
        """

    async def delete_channel_moderator(
        self, *, ChannelArn: str, ChannelModeratorArn: str, ChimeBearer: str = ...
    ) -> None:
        """
        Deletes a channel moderator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.delete_channel_moderator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#delete_channel_moderator)
        """

    async def delete_events_configuration(self, *, AccountId: str, BotId: str) -> None:
        """
        Deletes the events configuration that allows a bot to receive outgoing events.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.delete_events_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#delete_events_configuration)
        """

    async def delete_media_capture_pipeline(self, *, MediaPipelineId: str) -> None:
        """
        Deletes the media capture pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.delete_media_capture_pipeline)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#delete_media_capture_pipeline)
        """

    async def delete_meeting(self, *, MeetingId: str) -> None:
        """
        Deletes the specified Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.delete_meeting)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#delete_meeting)
        """

    async def delete_phone_number(self, *, PhoneNumberId: str) -> None:
        """
        Moves the specified phone number into the **Deletion queue**.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.delete_phone_number)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#delete_phone_number)
        """

    async def delete_proxy_session(self, *, VoiceConnectorId: str, ProxySessionId: str) -> None:
        """
        Deletes the specified proxy session from the specified Amazon Chime Voice
        Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.delete_proxy_session)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#delete_proxy_session)
        """

    async def delete_room(self, *, AccountId: str, RoomId: str) -> None:
        """
        Deletes a chat room in an Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.delete_room)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#delete_room)
        """

    async def delete_room_membership(self, *, AccountId: str, RoomId: str, MemberId: str) -> None:
        """
        Removes a member from a chat room in an Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.delete_room_membership)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#delete_room_membership)
        """

    async def delete_sip_media_application(self, *, SipMediaApplicationId: str) -> None:
        """
        Deletes a SIP media application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.delete_sip_media_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#delete_sip_media_application)
        """

    async def delete_sip_rule(self, *, SipRuleId: str) -> None:
        """
        Deletes a SIP rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.delete_sip_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#delete_sip_rule)
        """

    async def delete_voice_connector(self, *, VoiceConnectorId: str) -> None:
        """
        Deletes the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.delete_voice_connector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#delete_voice_connector)
        """

    async def delete_voice_connector_emergency_calling_configuration(
        self, *, VoiceConnectorId: str
    ) -> None:
        """
        Deletes the emergency calling configuration details from the specified Amazon
        Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.delete_voice_connector_emergency_calling_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#delete_voice_connector_emergency_calling_configuration)
        """

    async def delete_voice_connector_group(self, *, VoiceConnectorGroupId: str) -> None:
        """
        Deletes the specified Amazon Chime Voice Connector group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.delete_voice_connector_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#delete_voice_connector_group)
        """

    async def delete_voice_connector_origination(self, *, VoiceConnectorId: str) -> None:
        """
        Deletes the origination settings for the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.delete_voice_connector_origination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#delete_voice_connector_origination)
        """

    async def delete_voice_connector_proxy(self, *, VoiceConnectorId: str) -> None:
        """
        Deletes the proxy configuration from the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.delete_voice_connector_proxy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#delete_voice_connector_proxy)
        """

    async def delete_voice_connector_streaming_configuration(
        self, *, VoiceConnectorId: str
    ) -> None:
        """
        Deletes the streaming configuration for the specified Amazon Chime Voice
        Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.delete_voice_connector_streaming_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#delete_voice_connector_streaming_configuration)
        """

    async def delete_voice_connector_termination(self, *, VoiceConnectorId: str) -> None:
        """
        Deletes the termination settings for the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.delete_voice_connector_termination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#delete_voice_connector_termination)
        """

    async def delete_voice_connector_termination_credentials(
        self, *, VoiceConnectorId: str, Usernames: Sequence[str]
    ) -> None:
        """
        Deletes the specified SIP credentials used by your equipment to authenticate
        during call termination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.delete_voice_connector_termination_credentials)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#delete_voice_connector_termination_credentials)
        """

    async def describe_app_instance(
        self, *, AppInstanceArn: str
    ) -> DescribeAppInstanceResponseTypeDef:
        """
        Returns the full details of an `AppInstance` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.describe_app_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#describe_app_instance)
        """

    async def describe_app_instance_admin(
        self, *, AppInstanceAdminArn: str, AppInstanceArn: str
    ) -> DescribeAppInstanceAdminResponseTypeDef:
        """
        Returns the full details of an `AppInstanceAdmin` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.describe_app_instance_admin)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#describe_app_instance_admin)
        """

    async def describe_app_instance_user(
        self, *, AppInstanceUserArn: str
    ) -> DescribeAppInstanceUserResponseTypeDef:
        """
        Returns the full details of an `AppInstanceUser` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.describe_app_instance_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#describe_app_instance_user)
        """

    async def describe_channel(
        self, *, ChannelArn: str, ChimeBearer: str = ...
    ) -> DescribeChannelResponseTypeDef:
        """
        Returns the full details of a channel in an Amazon Chime `AppInstance` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.describe_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#describe_channel)
        """

    async def describe_channel_ban(
        self, *, ChannelArn: str, MemberArn: str, ChimeBearer: str = ...
    ) -> DescribeChannelBanResponseTypeDef:
        """
        Returns the full details of a channel ban.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.describe_channel_ban)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#describe_channel_ban)
        """

    async def describe_channel_membership(
        self, *, ChannelArn: str, MemberArn: str, ChimeBearer: str = ...
    ) -> DescribeChannelMembershipResponseTypeDef:
        """
        Returns the full details of a user's channel membership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.describe_channel_membership)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#describe_channel_membership)
        """

    async def describe_channel_membership_for_app_instance_user(
        self, *, ChannelArn: str, AppInstanceUserArn: str, ChimeBearer: str = ...
    ) -> DescribeChannelMembershipForAppInstanceUserResponseTypeDef:
        """
        Returns the details of a channel based on the membership of the specified
        `AppInstanceUser` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.describe_channel_membership_for_app_instance_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#describe_channel_membership_for_app_instance_user)
        """

    async def describe_channel_moderated_by_app_instance_user(
        self, *, ChannelArn: str, AppInstanceUserArn: str, ChimeBearer: str = ...
    ) -> DescribeChannelModeratedByAppInstanceUserResponseTypeDef:
        """
        Returns the full details of a channel moderated by the specified
        `AppInstanceUser` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.describe_channel_moderated_by_app_instance_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#describe_channel_moderated_by_app_instance_user)
        """

    async def describe_channel_moderator(
        self, *, ChannelArn: str, ChannelModeratorArn: str, ChimeBearer: str = ...
    ) -> DescribeChannelModeratorResponseTypeDef:
        """
        Returns the full details of a single ChannelModerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.describe_channel_moderator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#describe_channel_moderator)
        """

    async def disassociate_phone_number_from_user(
        self, *, AccountId: str, UserId: str
    ) -> Dict[str, Any]:
        """
        Disassociates the primary provisioned phone number from the specified Amazon
        Chime user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.disassociate_phone_number_from_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#disassociate_phone_number_from_user)
        """

    async def disassociate_phone_numbers_from_voice_connector(
        self, *, VoiceConnectorId: str, E164PhoneNumbers: Sequence[str]
    ) -> DisassociatePhoneNumbersFromVoiceConnectorResponseTypeDef:
        """
        Disassociates the specified phone numbers from the specified Amazon Chime Voice
        Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.disassociate_phone_numbers_from_voice_connector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#disassociate_phone_numbers_from_voice_connector)
        """

    async def disassociate_phone_numbers_from_voice_connector_group(
        self, *, VoiceConnectorGroupId: str, E164PhoneNumbers: Sequence[str]
    ) -> DisassociatePhoneNumbersFromVoiceConnectorGroupResponseTypeDef:
        """
        Disassociates the specified phone numbers from the specified Amazon Chime Voice
        Connector group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.disassociate_phone_numbers_from_voice_connector_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#disassociate_phone_numbers_from_voice_connector_group)
        """

    async def disassociate_signin_delegate_groups_from_account(
        self, *, AccountId: str, GroupNames: Sequence[str]
    ) -> Dict[str, Any]:
        """
        Disassociates the specified sign-in delegate groups from the specified Amazon
        Chime account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.disassociate_signin_delegate_groups_from_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#disassociate_signin_delegate_groups_from_account)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#generate_presigned_url)
        """

    async def get_account(self, *, AccountId: str) -> GetAccountResponseTypeDef:
        """
        Retrieves details for the specified Amazon Chime account, such as account type
        and supported licenses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_account)
        """

    async def get_account_settings(self, *, AccountId: str) -> GetAccountSettingsResponseTypeDef:
        """
        Retrieves account settings for the specified Amazon Chime account ID, such as
        remote control and dialout settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_account_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_account_settings)
        """

    async def get_app_instance_retention_settings(
        self, *, AppInstanceArn: str
    ) -> GetAppInstanceRetentionSettingsResponseTypeDef:
        """
        Gets the retention settings for an `AppInstance` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_app_instance_retention_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_app_instance_retention_settings)
        """

    async def get_app_instance_streaming_configurations(
        self, *, AppInstanceArn: str
    ) -> GetAppInstanceStreamingConfigurationsResponseTypeDef:
        """
        Gets the streaming settings for an `AppInstance` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_app_instance_streaming_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_app_instance_streaming_configurations)
        """

    async def get_attendee(self, *, MeetingId: str, AttendeeId: str) -> GetAttendeeResponseTypeDef:
        """
        Gets the Amazon Chime SDK attendee details for a specified meeting ID and
        attendee ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_attendee)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_attendee)
        """

    async def get_bot(self, *, AccountId: str, BotId: str) -> GetBotResponseTypeDef:
        """
        Retrieves details for the specified bot, such as bot email address, bot type,
        status, and display name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_bot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_bot)
        """

    async def get_channel_message(
        self, *, ChannelArn: str, MessageId: str, ChimeBearer: str = ...
    ) -> GetChannelMessageResponseTypeDef:
        """
        Gets the full details of a channel message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_channel_message)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_channel_message)
        """

    async def get_events_configuration(
        self, *, AccountId: str, BotId: str
    ) -> GetEventsConfigurationResponseTypeDef:
        """
        Gets details for an events configuration that allows a bot to receive outgoing
        events, such as an HTTPS endpoint or Lambda function ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_events_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_events_configuration)
        """

    async def get_global_settings(self) -> GetGlobalSettingsResponseTypeDef:
        """
        Retrieves global settings for the administrator's AWS account, such as Amazon
        Chime Business Calling and Amazon Chime Voice Connector settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_global_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_global_settings)
        """

    async def get_media_capture_pipeline(
        self, *, MediaPipelineId: str
    ) -> GetMediaCapturePipelineResponseTypeDef:
        """
        Gets an existing media capture pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_media_capture_pipeline)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_media_capture_pipeline)
        """

    async def get_meeting(self, *, MeetingId: str) -> GetMeetingResponseTypeDef:
        """
        Gets the Amazon Chime SDK meeting details for the specified meeting ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_meeting)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_meeting)
        """

    async def get_messaging_session_endpoint(self) -> GetMessagingSessionEndpointResponseTypeDef:
        """
        The details of the endpoint for the messaging session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_messaging_session_endpoint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_messaging_session_endpoint)
        """

    async def get_phone_number(self, *, PhoneNumberId: str) -> GetPhoneNumberResponseTypeDef:
        """
        Retrieves details for the specified phone number ID, such as associations,
        capabilities, and product type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_phone_number)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_phone_number)
        """

    async def get_phone_number_order(
        self, *, PhoneNumberOrderId: str
    ) -> GetPhoneNumberOrderResponseTypeDef:
        """
        Retrieves details for the specified phone number order, such as the order
        creation timestamp, phone numbers in E.164 format, product type, and order
        status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_phone_number_order)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_phone_number_order)
        """

    async def get_phone_number_settings(self) -> GetPhoneNumberSettingsResponseTypeDef:
        """
        Retrieves the phone number settings for the administrator's AWS account, such as
        the default outbound calling name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_phone_number_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_phone_number_settings)
        """

    async def get_proxy_session(
        self, *, VoiceConnectorId: str, ProxySessionId: str
    ) -> GetProxySessionResponseTypeDef:
        """
        Gets the specified proxy session details for the specified Amazon Chime Voice
        Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_proxy_session)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_proxy_session)
        """

    async def get_retention_settings(
        self, *, AccountId: str
    ) -> GetRetentionSettingsResponseTypeDef:
        """
        Gets the retention settings for the specified Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_retention_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_retention_settings)
        """

    async def get_room(self, *, AccountId: str, RoomId: str) -> GetRoomResponseTypeDef:
        """
        Retrieves room details, such as the room name, for a room in an Amazon Chime
        Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_room)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_room)
        """

    async def get_sip_media_application(
        self, *, SipMediaApplicationId: str
    ) -> GetSipMediaApplicationResponseTypeDef:
        """
        Retrieves the information for a SIP media application, including name, AWS
        Region, and endpoints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_sip_media_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_sip_media_application)
        """

    async def get_sip_media_application_logging_configuration(
        self, *, SipMediaApplicationId: str
    ) -> GetSipMediaApplicationLoggingConfigurationResponseTypeDef:
        """
        Returns the logging configuration for the specified SIP media application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_sip_media_application_logging_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_sip_media_application_logging_configuration)
        """

    async def get_sip_rule(self, *, SipRuleId: str) -> GetSipRuleResponseTypeDef:
        """
        Retrieves the details of a SIP rule, such as the rule ID, name, triggers, and
        target endpoints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_sip_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_sip_rule)
        """

    async def get_user(self, *, AccountId: str, UserId: str) -> GetUserResponseTypeDef:
        """
        Retrieves details for the specified user ID, such as primary email address,
        license type,and personal meeting PIN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_user)
        """

    async def get_user_settings(
        self, *, AccountId: str, UserId: str
    ) -> GetUserSettingsResponseTypeDef:
        """
        Retrieves settings for the specified user ID, such as any associated phone
        number settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_user_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_user_settings)
        """

    async def get_voice_connector(
        self, *, VoiceConnectorId: str
    ) -> GetVoiceConnectorResponseTypeDef:
        """
        Retrieves details for the specified Amazon Chime Voice Connector, such as
        timestamps,name, outbound host, and encryption requirements.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_voice_connector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_voice_connector)
        """

    async def get_voice_connector_emergency_calling_configuration(
        self, *, VoiceConnectorId: str
    ) -> GetVoiceConnectorEmergencyCallingConfigurationResponseTypeDef:
        """
        Gets the emergency calling configuration details for the specified Amazon Chime
        Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_voice_connector_emergency_calling_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_voice_connector_emergency_calling_configuration)
        """

    async def get_voice_connector_group(
        self, *, VoiceConnectorGroupId: str
    ) -> GetVoiceConnectorGroupResponseTypeDef:
        """
        Retrieves details for the specified Amazon Chime Voice Connector group, such as
        timestamps,name, and associated `VoiceConnectorItems` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_voice_connector_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_voice_connector_group)
        """

    async def get_voice_connector_logging_configuration(
        self, *, VoiceConnectorId: str
    ) -> GetVoiceConnectorLoggingConfigurationResponseTypeDef:
        """
        Retrieves the logging configuration details for the specified Amazon Chime Voice
        Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_voice_connector_logging_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_voice_connector_logging_configuration)
        """

    async def get_voice_connector_origination(
        self, *, VoiceConnectorId: str
    ) -> GetVoiceConnectorOriginationResponseTypeDef:
        """
        Retrieves origination setting details for the specified Amazon Chime Voice
        Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_voice_connector_origination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_voice_connector_origination)
        """

    async def get_voice_connector_proxy(
        self, *, VoiceConnectorId: str
    ) -> GetVoiceConnectorProxyResponseTypeDef:
        """
        Gets the proxy configuration details for the specified Amazon Chime Voice
        Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_voice_connector_proxy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_voice_connector_proxy)
        """

    async def get_voice_connector_streaming_configuration(
        self, *, VoiceConnectorId: str
    ) -> GetVoiceConnectorStreamingConfigurationResponseTypeDef:
        """
        Retrieves the streaming configuration details for the specified Amazon Chime
        Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_voice_connector_streaming_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_voice_connector_streaming_configuration)
        """

    async def get_voice_connector_termination(
        self, *, VoiceConnectorId: str
    ) -> GetVoiceConnectorTerminationResponseTypeDef:
        """
        Retrieves termination setting details for the specified Amazon Chime Voice
        Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_voice_connector_termination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_voice_connector_termination)
        """

    async def get_voice_connector_termination_health(
        self, *, VoiceConnectorId: str
    ) -> GetVoiceConnectorTerminationHealthResponseTypeDef:
        """
        Retrieves information about the last time a SIP `OPTIONS` ping was received from
        your SIP infrastructure for the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_voice_connector_termination_health)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_voice_connector_termination_health)
        """

    async def invite_users(
        self, *, AccountId: str, UserEmailList: Sequence[str], UserType: UserTypeType = ...
    ) -> InviteUsersResponseTypeDef:
        """
        Sends email to a maximum of 50 users, inviting them to the specified Amazon
        Chime `Team` account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.invite_users)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#invite_users)
        """

    async def list_accounts(
        self, *, Name: str = ..., UserEmail: str = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> ListAccountsResponseTypeDef:
        """
        Lists the Amazon Chime accounts under the administrator's AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.list_accounts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#list_accounts)
        """

    async def list_app_instance_admins(
        self, *, AppInstanceArn: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListAppInstanceAdminsResponseTypeDef:
        """
        Returns a list of the administrators in the `AppInstance` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.list_app_instance_admins)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#list_app_instance_admins)
        """

    async def list_app_instance_users(
        self, *, AppInstanceArn: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListAppInstanceUsersResponseTypeDef:
        """
        List all `AppInstanceUsers` created under a single `AppInstance` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.list_app_instance_users)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#list_app_instance_users)
        """

    async def list_app_instances(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListAppInstancesResponseTypeDef:
        """
        Lists all Amazon Chime `AppInstance` s created under a single AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.list_app_instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#list_app_instances)
        """

    async def list_attendee_tags(
        self, *, MeetingId: str, AttendeeId: str
    ) -> ListAttendeeTagsResponseTypeDef:
        """
        Lists the tags applied to an Amazon Chime SDK attendee resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.list_attendee_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#list_attendee_tags)
        """

    async def list_attendees(
        self, *, MeetingId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListAttendeesResponseTypeDef:
        """
        Lists the attendees for the specified Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.list_attendees)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#list_attendees)
        """

    async def list_bots(
        self, *, AccountId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListBotsResponseTypeDef:
        """
        Lists the bots associated with the administrator's Amazon Chime Enterprise
        account ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.list_bots)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#list_bots)
        """

    async def list_channel_bans(
        self,
        *,
        ChannelArn: str,
        MaxResults: int = ...,
        NextToken: str = ...,
        ChimeBearer: str = ...
    ) -> ListChannelBansResponseTypeDef:
        """
        Lists all the users banned from a particular channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.list_channel_bans)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#list_channel_bans)
        """

    async def list_channel_memberships(
        self,
        *,
        ChannelArn: str,
        Type: ChannelMembershipTypeType = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        ChimeBearer: str = ...
    ) -> ListChannelMembershipsResponseTypeDef:
        """
        Lists all channel memberships in a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.list_channel_memberships)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#list_channel_memberships)
        """

    async def list_channel_memberships_for_app_instance_user(
        self,
        *,
        AppInstanceUserArn: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        ChimeBearer: str = ...
    ) -> ListChannelMembershipsForAppInstanceUserResponseTypeDef:
        """
        Lists all channels that a particular `AppInstanceUser` is a part of.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.list_channel_memberships_for_app_instance_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#list_channel_memberships_for_app_instance_user)
        """

    async def list_channel_messages(
        self,
        *,
        ChannelArn: str,
        SortOrder: SortOrderType = ...,
        NotBefore: Union[datetime, str] = ...,
        NotAfter: Union[datetime, str] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        ChimeBearer: str = ...
    ) -> ListChannelMessagesResponseTypeDef:
        """
        List all the messages in a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.list_channel_messages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#list_channel_messages)
        """

    async def list_channel_moderators(
        self,
        *,
        ChannelArn: str,
        MaxResults: int = ...,
        NextToken: str = ...,
        ChimeBearer: str = ...
    ) -> ListChannelModeratorsResponseTypeDef:
        """
        Lists all the moderators for a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.list_channel_moderators)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#list_channel_moderators)
        """

    async def list_channels(
        self,
        *,
        AppInstanceArn: str,
        Privacy: ChannelPrivacyType = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        ChimeBearer: str = ...
    ) -> ListChannelsResponseTypeDef:
        """
        Lists all Channels created under a single Chime App as a paginated list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.list_channels)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#list_channels)
        """

    async def list_channels_moderated_by_app_instance_user(
        self,
        *,
        AppInstanceUserArn: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        ChimeBearer: str = ...
    ) -> ListChannelsModeratedByAppInstanceUserResponseTypeDef:
        """
        A list of the channels moderated by an `AppInstanceUser` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.list_channels_moderated_by_app_instance_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#list_channels_moderated_by_app_instance_user)
        """

    async def list_media_capture_pipelines(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListMediaCapturePipelinesResponseTypeDef:
        """
        Returns a list of media capture pipelines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.list_media_capture_pipelines)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#list_media_capture_pipelines)
        """

    async def list_meeting_tags(self, *, MeetingId: str) -> ListMeetingTagsResponseTypeDef:
        """
        Lists the tags applied to an Amazon Chime SDK meeting resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.list_meeting_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#list_meeting_tags)
        """

    async def list_meetings(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListMeetingsResponseTypeDef:
        """
        Lists up to 100 active Amazon Chime SDK meetings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.list_meetings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#list_meetings)
        """

    async def list_phone_number_orders(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListPhoneNumberOrdersResponseTypeDef:
        """
        Lists the phone number orders for the administrator's Amazon Chime account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.list_phone_number_orders)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#list_phone_number_orders)
        """

    async def list_phone_numbers(
        self,
        *,
        Status: PhoneNumberStatusType = ...,
        ProductType: PhoneNumberProductTypeType = ...,
        FilterName: PhoneNumberAssociationNameType = ...,
        FilterValue: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListPhoneNumbersResponseTypeDef:
        """
        Lists the phone numbers for the specified Amazon Chime account, Amazon Chime
        user, Amazon Chime Voice Connector, or Amazon Chime Voice Connector group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.list_phone_numbers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#list_phone_numbers)
        """

    async def list_proxy_sessions(
        self,
        *,
        VoiceConnectorId: str,
        Status: ProxySessionStatusType = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListProxySessionsResponseTypeDef:
        """
        Lists the proxy sessions for the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.list_proxy_sessions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#list_proxy_sessions)
        """

    async def list_room_memberships(
        self, *, AccountId: str, RoomId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListRoomMembershipsResponseTypeDef:
        """
        Lists the membership details for the specified room in an Amazon Chime
        Enterprise account, such as the members' IDs, email addresses, and names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.list_room_memberships)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#list_room_memberships)
        """

    async def list_rooms(
        self, *, AccountId: str, MemberId: str = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> ListRoomsResponseTypeDef:
        """
        Lists the room details for the specified Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.list_rooms)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#list_rooms)
        """

    async def list_sip_media_applications(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListSipMediaApplicationsResponseTypeDef:
        """
        Lists the SIP media applications under the administrator's AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.list_sip_media_applications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#list_sip_media_applications)
        """

    async def list_sip_rules(
        self, *, SipMediaApplicationId: str = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> ListSipRulesResponseTypeDef:
        """
        Lists the SIP rules under the administrator's AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.list_sip_rules)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#list_sip_rules)
        """

    async def list_supported_phone_number_countries(
        self, *, ProductType: PhoneNumberProductTypeType
    ) -> ListSupportedPhoneNumberCountriesResponseTypeDef:
        """
        Lists supported phone number countries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.list_supported_phone_number_countries)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#list_supported_phone_number_countries)
        """

    async def list_tags_for_resource(
        self, *, ResourceARN: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags applied to an Amazon Chime SDK meeting resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#list_tags_for_resource)
        """

    async def list_users(
        self,
        *,
        AccountId: str,
        UserEmail: str = ...,
        UserType: UserTypeType = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListUsersResponseTypeDef:
        """
        Lists the users that belong to the specified Amazon Chime account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.list_users)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#list_users)
        """

    async def list_voice_connector_groups(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListVoiceConnectorGroupsResponseTypeDef:
        """
        Lists the Amazon Chime Voice Connector groups for the administrator's AWS
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.list_voice_connector_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#list_voice_connector_groups)
        """

    async def list_voice_connector_termination_credentials(
        self, *, VoiceConnectorId: str
    ) -> ListVoiceConnectorTerminationCredentialsResponseTypeDef:
        """
        Lists the SIP credentials for the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.list_voice_connector_termination_credentials)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#list_voice_connector_termination_credentials)
        """

    async def list_voice_connectors(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListVoiceConnectorsResponseTypeDef:
        """
        Lists the Amazon Chime Voice Connectors for the administrator's AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.list_voice_connectors)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#list_voice_connectors)
        """

    async def logout_user(self, *, AccountId: str, UserId: str) -> Dict[str, Any]:
        """
        Logs out the specified user from all of the devices they are currently logged
        into.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.logout_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#logout_user)
        """

    async def put_app_instance_retention_settings(
        self,
        *,
        AppInstanceArn: str,
        AppInstanceRetentionSettings: "AppInstanceRetentionSettingsTypeDef"
    ) -> PutAppInstanceRetentionSettingsResponseTypeDef:
        """
        Sets the amount of time in days that a given `AppInstance` retains data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.put_app_instance_retention_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#put_app_instance_retention_settings)
        """

    async def put_app_instance_streaming_configurations(
        self,
        *,
        AppInstanceArn: str,
        AppInstanceStreamingConfigurations: Sequence["AppInstanceStreamingConfigurationTypeDef"]
    ) -> PutAppInstanceStreamingConfigurationsResponseTypeDef:
        """
        The data streaming configurations of an `AppInstance` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.put_app_instance_streaming_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#put_app_instance_streaming_configurations)
        """

    async def put_events_configuration(
        self,
        *,
        AccountId: str,
        BotId: str,
        OutboundEventsHTTPSEndpoint: str = ...,
        LambdaFunctionArn: str = ...
    ) -> PutEventsConfigurationResponseTypeDef:
        """
        Creates an events configuration that allows a bot to receive outgoing events
        sent by Amazon Chime.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.put_events_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#put_events_configuration)
        """

    async def put_retention_settings(
        self, *, AccountId: str, RetentionSettings: "RetentionSettingsTypeDef"
    ) -> PutRetentionSettingsResponseTypeDef:
        """
        Puts retention settings for the specified Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.put_retention_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#put_retention_settings)
        """

    async def put_sip_media_application_logging_configuration(
        self,
        *,
        SipMediaApplicationId: str,
        SipMediaApplicationLoggingConfiguration: "SipMediaApplicationLoggingConfigurationTypeDef" = ...
    ) -> PutSipMediaApplicationLoggingConfigurationResponseTypeDef:
        """
        Updates the logging configuration for the specified SIP media application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.put_sip_media_application_logging_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#put_sip_media_application_logging_configuration)
        """

    async def put_voice_connector_emergency_calling_configuration(
        self,
        *,
        VoiceConnectorId: str,
        EmergencyCallingConfiguration: "EmergencyCallingConfigurationTypeDef"
    ) -> PutVoiceConnectorEmergencyCallingConfigurationResponseTypeDef:
        """
        Puts emergency calling configuration details to the specified Amazon Chime Voice
        Connector, such as emergency phone numbers and calling countries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.put_voice_connector_emergency_calling_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#put_voice_connector_emergency_calling_configuration)
        """

    async def put_voice_connector_logging_configuration(
        self, *, VoiceConnectorId: str, LoggingConfiguration: "LoggingConfigurationTypeDef"
    ) -> PutVoiceConnectorLoggingConfigurationResponseTypeDef:
        """
        Adds a logging configuration for the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.put_voice_connector_logging_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#put_voice_connector_logging_configuration)
        """

    async def put_voice_connector_origination(
        self, *, VoiceConnectorId: str, Origination: "OriginationTypeDef"
    ) -> PutVoiceConnectorOriginationResponseTypeDef:
        """
        Adds origination settings for the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.put_voice_connector_origination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#put_voice_connector_origination)
        """

    async def put_voice_connector_proxy(
        self,
        *,
        VoiceConnectorId: str,
        DefaultSessionExpiryMinutes: int,
        PhoneNumberPoolCountries: Sequence[str],
        FallBackPhoneNumber: str = ...,
        Disabled: bool = ...
    ) -> PutVoiceConnectorProxyResponseTypeDef:
        """
        Puts the specified proxy configuration to the specified Amazon Chime Voice
        Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.put_voice_connector_proxy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#put_voice_connector_proxy)
        """

    async def put_voice_connector_streaming_configuration(
        self, *, VoiceConnectorId: str, StreamingConfiguration: "StreamingConfigurationTypeDef"
    ) -> PutVoiceConnectorStreamingConfigurationResponseTypeDef:
        """
        Adds a streaming configuration for the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.put_voice_connector_streaming_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#put_voice_connector_streaming_configuration)
        """

    async def put_voice_connector_termination(
        self, *, VoiceConnectorId: str, Termination: "TerminationTypeDef"
    ) -> PutVoiceConnectorTerminationResponseTypeDef:
        """
        Adds termination settings for the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.put_voice_connector_termination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#put_voice_connector_termination)
        """

    async def put_voice_connector_termination_credentials(
        self, *, VoiceConnectorId: str, Credentials: Sequence["CredentialTypeDef"] = ...
    ) -> None:
        """
        Adds termination SIP credentials for the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.put_voice_connector_termination_credentials)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#put_voice_connector_termination_credentials)
        """

    async def redact_channel_message(
        self, *, ChannelArn: str, MessageId: str, ChimeBearer: str = ...
    ) -> RedactChannelMessageResponseTypeDef:
        """
        Redacts message content, but not metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.redact_channel_message)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#redact_channel_message)
        """

    async def redact_conversation_message(
        self, *, AccountId: str, ConversationId: str, MessageId: str
    ) -> Dict[str, Any]:
        """
        Redacts the specified message from the specified Amazon Chime conversation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.redact_conversation_message)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#redact_conversation_message)
        """

    async def redact_room_message(
        self, *, AccountId: str, RoomId: str, MessageId: str
    ) -> Dict[str, Any]:
        """
        Redacts the specified message from the specified Amazon Chime channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.redact_room_message)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#redact_room_message)
        """

    async def regenerate_security_token(
        self, *, AccountId: str, BotId: str
    ) -> RegenerateSecurityTokenResponseTypeDef:
        """
        Regenerates the security token for a bot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.regenerate_security_token)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#regenerate_security_token)
        """

    async def reset_personal_pin(
        self, *, AccountId: str, UserId: str
    ) -> ResetPersonalPINResponseTypeDef:
        """
        Resets the personal meeting PIN for the specified user on an Amazon Chime
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.reset_personal_pin)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#reset_personal_pin)
        """

    async def restore_phone_number(
        self, *, PhoneNumberId: str
    ) -> RestorePhoneNumberResponseTypeDef:
        """
        Moves a phone number from the **Deletion queue** back into the phone number
        **Inventory** .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.restore_phone_number)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#restore_phone_number)
        """

    async def search_available_phone_numbers(
        self,
        *,
        AreaCode: str = ...,
        City: str = ...,
        Country: str = ...,
        State: str = ...,
        TollFreePrefix: str = ...,
        PhoneNumberType: PhoneNumberTypeType = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> SearchAvailablePhoneNumbersResponseTypeDef:
        """
        Searches for phone numbers that can be ordered.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.search_available_phone_numbers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#search_available_phone_numbers)
        """

    async def send_channel_message(
        self,
        *,
        ChannelArn: str,
        Content: str,
        Type: ChannelMessageTypeType,
        Persistence: ChannelMessagePersistenceTypeType,
        ClientRequestToken: str,
        Metadata: str = ...,
        ChimeBearer: str = ...
    ) -> SendChannelMessageResponseTypeDef:
        """
        Sends a message to a particular channel that the member is a part of.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.send_channel_message)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#send_channel_message)
        """

    async def start_meeting_transcription(
        self, *, MeetingId: str, TranscriptionConfiguration: "TranscriptionConfigurationTypeDef"
    ) -> Dict[str, Any]:
        """
        Starts transcription for the specified `meetingId` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.start_meeting_transcription)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#start_meeting_transcription)
        """

    async def stop_meeting_transcription(self, *, MeetingId: str) -> Dict[str, Any]:
        """
        Stops transcription for the specified `meetingId` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.stop_meeting_transcription)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#stop_meeting_transcription)
        """

    async def tag_attendee(
        self, *, MeetingId: str, AttendeeId: str, Tags: Sequence["TagTypeDef"]
    ) -> None:
        """
        Applies the specified tags to the specified Amazon Chime SDK attendee.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.tag_attendee)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#tag_attendee)
        """

    async def tag_meeting(self, *, MeetingId: str, Tags: Sequence["TagTypeDef"]) -> None:
        """
        Applies the specified tags to the specified Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.tag_meeting)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#tag_meeting)
        """

    async def tag_resource(self, *, ResourceARN: str, Tags: Sequence["TagTypeDef"]) -> None:
        """
        Applies the specified tags to the specified Amazon Chime SDK meeting resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#tag_resource)
        """

    async def untag_attendee(
        self, *, MeetingId: str, AttendeeId: str, TagKeys: Sequence[str]
    ) -> None:
        """
        Untags the specified tags from the specified Amazon Chime SDK attendee.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.untag_attendee)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#untag_attendee)
        """

    async def untag_meeting(self, *, MeetingId: str, TagKeys: Sequence[str]) -> None:
        """
        Untags the specified tags from the specified Amazon Chime SDK meeting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.untag_meeting)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#untag_meeting)
        """

    async def untag_resource(self, *, ResourceARN: str, TagKeys: Sequence[str]) -> None:
        """
        Untags the specified tags from the specified Amazon Chime SDK meeting resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#untag_resource)
        """

    async def update_account(
        self, *, AccountId: str, Name: str = ..., DefaultLicense: LicenseType = ...
    ) -> UpdateAccountResponseTypeDef:
        """
        Updates account details for the specified Amazon Chime account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.update_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#update_account)
        """

    async def update_account_settings(
        self, *, AccountId: str, AccountSettings: "AccountSettingsTypeDef"
    ) -> Dict[str, Any]:
        """
        Updates the settings for the specified Amazon Chime account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.update_account_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#update_account_settings)
        """

    async def update_app_instance(
        self, *, AppInstanceArn: str, Name: str, Metadata: str = ...
    ) -> UpdateAppInstanceResponseTypeDef:
        """
        Updates `AppInstance` metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.update_app_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#update_app_instance)
        """

    async def update_app_instance_user(
        self, *, AppInstanceUserArn: str, Name: str, Metadata: str = ...
    ) -> UpdateAppInstanceUserResponseTypeDef:
        """
        Updates the details of an `AppInstanceUser`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.update_app_instance_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#update_app_instance_user)
        """

    async def update_bot(
        self, *, AccountId: str, BotId: str, Disabled: bool = ...
    ) -> UpdateBotResponseTypeDef:
        """
        Updates the status of the specified bot, such as starting or stopping the bot
        from running in your Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.update_bot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#update_bot)
        """

    async def update_channel(
        self,
        *,
        ChannelArn: str,
        Name: str,
        Mode: ChannelModeType,
        Metadata: str = ...,
        ChimeBearer: str = ...
    ) -> UpdateChannelResponseTypeDef:
        """
        Update a channel's attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.update_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#update_channel)
        """

    async def update_channel_message(
        self,
        *,
        ChannelArn: str,
        MessageId: str,
        Content: str = ...,
        Metadata: str = ...,
        ChimeBearer: str = ...
    ) -> UpdateChannelMessageResponseTypeDef:
        """
        Updates the content of a message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.update_channel_message)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#update_channel_message)
        """

    async def update_channel_read_marker(
        self, *, ChannelArn: str, ChimeBearer: str = ...
    ) -> UpdateChannelReadMarkerResponseTypeDef:
        """
        The details of the time when a user last read messages in a channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.update_channel_read_marker)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#update_channel_read_marker)
        """

    async def update_global_settings(
        self,
        *,
        BusinessCalling: "BusinessCallingSettingsTypeDef" = ...,
        VoiceConnector: "VoiceConnectorSettingsTypeDef" = ...
    ) -> None:
        """
        Updates global settings for the administrator's AWS account, such as Amazon
        Chime Business Calling and Amazon Chime Voice Connector settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.update_global_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#update_global_settings)
        """

    async def update_phone_number(
        self,
        *,
        PhoneNumberId: str,
        ProductType: PhoneNumberProductTypeType = ...,
        CallingName: str = ...
    ) -> UpdatePhoneNumberResponseTypeDef:
        """
        Updates phone number details, such as product type or calling name, for the
        specified phone number ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.update_phone_number)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#update_phone_number)
        """

    async def update_phone_number_settings(self, *, CallingName: str) -> None:
        """
        Updates the phone number settings for the administrator's AWS account, such as
        the default outbound calling name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.update_phone_number_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#update_phone_number_settings)
        """

    async def update_proxy_session(
        self,
        *,
        VoiceConnectorId: str,
        ProxySessionId: str,
        Capabilities: Sequence[CapabilityType],
        ExpiryMinutes: int = ...
    ) -> UpdateProxySessionResponseTypeDef:
        """
        Updates the specified proxy session details, such as voice or SMS capabilities.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.update_proxy_session)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#update_proxy_session)
        """

    async def update_room(
        self, *, AccountId: str, RoomId: str, Name: str = ...
    ) -> UpdateRoomResponseTypeDef:
        """
        Updates room details, such as the room name, for a room in an Amazon Chime
        Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.update_room)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#update_room)
        """

    async def update_room_membership(
        self, *, AccountId: str, RoomId: str, MemberId: str, Role: RoomMembershipRoleType = ...
    ) -> UpdateRoomMembershipResponseTypeDef:
        """
        Updates room membership details, such as the member role, for a room in an
        Amazon Chime Enterprise account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.update_room_membership)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#update_room_membership)
        """

    async def update_sip_media_application(
        self,
        *,
        SipMediaApplicationId: str,
        Name: str = ...,
        Endpoints: Sequence["SipMediaApplicationEndpointTypeDef"] = ...
    ) -> UpdateSipMediaApplicationResponseTypeDef:
        """
        Updates the details of the specified SIP media application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.update_sip_media_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#update_sip_media_application)
        """

    async def update_sip_media_application_call(
        self, *, SipMediaApplicationId: str, TransactionId: str, Arguments: Mapping[str, str]
    ) -> UpdateSipMediaApplicationCallResponseTypeDef:
        """
        Invokes the AWS Lambda function associated with the SIP media application and
        transaction ID in an update request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.update_sip_media_application_call)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#update_sip_media_application_call)
        """

    async def update_sip_rule(
        self,
        *,
        SipRuleId: str,
        Name: str,
        Disabled: bool = ...,
        TargetApplications: Sequence["SipRuleTargetApplicationTypeDef"] = ...
    ) -> UpdateSipRuleResponseTypeDef:
        """
        Updates the details of the specified SIP rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.update_sip_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#update_sip_rule)
        """

    async def update_user(
        self,
        *,
        AccountId: str,
        UserId: str,
        LicenseType: LicenseType = ...,
        UserType: UserTypeType = ...,
        AlexaForBusinessMetadata: "AlexaForBusinessMetadataTypeDef" = ...
    ) -> UpdateUserResponseTypeDef:
        """
        Updates user details for a specified user ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.update_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#update_user)
        """

    async def update_user_settings(
        self, *, AccountId: str, UserId: str, UserSettings: "UserSettingsTypeDef"
    ) -> None:
        """
        Updates the settings for the specified user, such as phone number settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.update_user_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#update_user_settings)
        """

    async def update_voice_connector(
        self, *, VoiceConnectorId: str, Name: str, RequireEncryption: bool
    ) -> UpdateVoiceConnectorResponseTypeDef:
        """
        Updates details for the specified Amazon Chime Voice Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.update_voice_connector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#update_voice_connector)
        """

    async def update_voice_connector_group(
        self,
        *,
        VoiceConnectorGroupId: str,
        Name: str,
        VoiceConnectorItems: Sequence["VoiceConnectorItemTypeDef"]
    ) -> UpdateVoiceConnectorGroupResponseTypeDef:
        """
        Updates details of the specified Amazon Chime Voice Connector group, such as the
        name and Amazon Chime Voice Connector priority ranking.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.update_voice_connector_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#update_voice_connector_group)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_accounts"]) -> ListAccountsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_users"]) -> ListUsersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/#get_paginator)
        """

    async def __aenter__(self) -> "ChimeClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/chime.html#Chime.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime/client/)
        """
