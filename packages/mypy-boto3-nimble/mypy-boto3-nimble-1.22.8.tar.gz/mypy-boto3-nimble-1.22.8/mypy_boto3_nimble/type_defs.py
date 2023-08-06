"""
Type annotations for nimble service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_nimble/type_defs/)

Usage::

    ```python
    from mypy_boto3_nimble.type_defs import AcceptEulasRequestRequestTypeDef

    data: AcceptEulasRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    LaunchProfilePlatformType,
    LaunchProfileStateType,
    LaunchProfileStatusCodeType,
    LaunchProfileValidationStateType,
    LaunchProfileValidationStatusCodeType,
    LaunchProfileValidationTypeType,
    StreamingClipboardModeType,
    StreamingImageStateType,
    StreamingImageStatusCodeType,
    StreamingInstanceTypeType,
    StreamingSessionStateType,
    StreamingSessionStatusCodeType,
    StreamingSessionStreamStateType,
    StreamingSessionStreamStatusCodeType,
    StudioComponentInitializationScriptRunContextType,
    StudioComponentStateType,
    StudioComponentStatusCodeType,
    StudioComponentSubtypeType,
    StudioComponentTypeType,
    StudioEncryptionConfigurationKeyTypeType,
    StudioStateType,
    StudioStatusCodeType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AcceptEulasRequestRequestTypeDef",
    "AcceptEulasResponseTypeDef",
    "ActiveDirectoryComputerAttributeTypeDef",
    "ActiveDirectoryConfigurationTypeDef",
    "ComputeFarmConfigurationTypeDef",
    "CreateLaunchProfileRequestRequestTypeDef",
    "CreateLaunchProfileResponseTypeDef",
    "CreateStreamingImageRequestRequestTypeDef",
    "CreateStreamingImageResponseTypeDef",
    "CreateStreamingSessionRequestRequestTypeDef",
    "CreateStreamingSessionResponseTypeDef",
    "CreateStreamingSessionStreamRequestRequestTypeDef",
    "CreateStreamingSessionStreamResponseTypeDef",
    "CreateStudioComponentRequestRequestTypeDef",
    "CreateStudioComponentResponseTypeDef",
    "CreateStudioRequestRequestTypeDef",
    "CreateStudioResponseTypeDef",
    "DeleteLaunchProfileMemberRequestRequestTypeDef",
    "DeleteLaunchProfileRequestRequestTypeDef",
    "DeleteLaunchProfileResponseTypeDef",
    "DeleteStreamingImageRequestRequestTypeDef",
    "DeleteStreamingImageResponseTypeDef",
    "DeleteStreamingSessionRequestRequestTypeDef",
    "DeleteStreamingSessionResponseTypeDef",
    "DeleteStudioComponentRequestRequestTypeDef",
    "DeleteStudioComponentResponseTypeDef",
    "DeleteStudioMemberRequestRequestTypeDef",
    "DeleteStudioRequestRequestTypeDef",
    "DeleteStudioResponseTypeDef",
    "EulaAcceptanceTypeDef",
    "EulaTypeDef",
    "GetEulaRequestRequestTypeDef",
    "GetEulaResponseTypeDef",
    "GetLaunchProfileDetailsRequestRequestTypeDef",
    "GetLaunchProfileDetailsResponseTypeDef",
    "GetLaunchProfileInitializationRequestRequestTypeDef",
    "GetLaunchProfileInitializationResponseTypeDef",
    "GetLaunchProfileMemberRequestRequestTypeDef",
    "GetLaunchProfileMemberResponseTypeDef",
    "GetLaunchProfileRequestLaunchProfileDeletedWaitTypeDef",
    "GetLaunchProfileRequestLaunchProfileReadyWaitTypeDef",
    "GetLaunchProfileRequestRequestTypeDef",
    "GetLaunchProfileResponseTypeDef",
    "GetStreamingImageRequestRequestTypeDef",
    "GetStreamingImageRequestStreamingImageDeletedWaitTypeDef",
    "GetStreamingImageRequestStreamingImageReadyWaitTypeDef",
    "GetStreamingImageResponseTypeDef",
    "GetStreamingSessionRequestRequestTypeDef",
    "GetStreamingSessionRequestStreamingSessionDeletedWaitTypeDef",
    "GetStreamingSessionRequestStreamingSessionReadyWaitTypeDef",
    "GetStreamingSessionRequestStreamingSessionStoppedWaitTypeDef",
    "GetStreamingSessionResponseTypeDef",
    "GetStreamingSessionStreamRequestRequestTypeDef",
    "GetStreamingSessionStreamRequestStreamingSessionStreamReadyWaitTypeDef",
    "GetStreamingSessionStreamResponseTypeDef",
    "GetStudioComponentRequestRequestTypeDef",
    "GetStudioComponentRequestStudioComponentDeletedWaitTypeDef",
    "GetStudioComponentRequestStudioComponentReadyWaitTypeDef",
    "GetStudioComponentResponseTypeDef",
    "GetStudioMemberRequestRequestTypeDef",
    "GetStudioMemberResponseTypeDef",
    "GetStudioRequestRequestTypeDef",
    "GetStudioRequestStudioDeletedWaitTypeDef",
    "GetStudioRequestStudioReadyWaitTypeDef",
    "GetStudioResponseTypeDef",
    "LaunchProfileInitializationActiveDirectoryTypeDef",
    "LaunchProfileInitializationScriptTypeDef",
    "LaunchProfileInitializationTypeDef",
    "LaunchProfileMembershipTypeDef",
    "LaunchProfileTypeDef",
    "LicenseServiceConfigurationTypeDef",
    "ListEulaAcceptancesRequestListEulaAcceptancesPaginateTypeDef",
    "ListEulaAcceptancesRequestRequestTypeDef",
    "ListEulaAcceptancesResponseTypeDef",
    "ListEulasRequestListEulasPaginateTypeDef",
    "ListEulasRequestRequestTypeDef",
    "ListEulasResponseTypeDef",
    "ListLaunchProfileMembersRequestListLaunchProfileMembersPaginateTypeDef",
    "ListLaunchProfileMembersRequestRequestTypeDef",
    "ListLaunchProfileMembersResponseTypeDef",
    "ListLaunchProfilesRequestListLaunchProfilesPaginateTypeDef",
    "ListLaunchProfilesRequestRequestTypeDef",
    "ListLaunchProfilesResponseTypeDef",
    "ListStreamingImagesRequestListStreamingImagesPaginateTypeDef",
    "ListStreamingImagesRequestRequestTypeDef",
    "ListStreamingImagesResponseTypeDef",
    "ListStreamingSessionsRequestListStreamingSessionsPaginateTypeDef",
    "ListStreamingSessionsRequestRequestTypeDef",
    "ListStreamingSessionsResponseTypeDef",
    "ListStudioComponentsRequestListStudioComponentsPaginateTypeDef",
    "ListStudioComponentsRequestRequestTypeDef",
    "ListStudioComponentsResponseTypeDef",
    "ListStudioMembersRequestListStudioMembersPaginateTypeDef",
    "ListStudioMembersRequestRequestTypeDef",
    "ListStudioMembersResponseTypeDef",
    "ListStudiosRequestListStudiosPaginateTypeDef",
    "ListStudiosRequestRequestTypeDef",
    "ListStudiosResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "NewLaunchProfileMemberTypeDef",
    "NewStudioMemberTypeDef",
    "PaginatorConfigTypeDef",
    "PutLaunchProfileMembersRequestRequestTypeDef",
    "PutStudioMembersRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "ScriptParameterKeyValueTypeDef",
    "SharedFileSystemConfigurationTypeDef",
    "StartStreamingSessionRequestRequestTypeDef",
    "StartStreamingSessionResponseTypeDef",
    "StartStudioSSOConfigurationRepairRequestRequestTypeDef",
    "StartStudioSSOConfigurationRepairResponseTypeDef",
    "StopStreamingSessionRequestRequestTypeDef",
    "StopStreamingSessionResponseTypeDef",
    "StreamConfigurationCreateTypeDef",
    "StreamConfigurationSessionStorageTypeDef",
    "StreamConfigurationTypeDef",
    "StreamingImageEncryptionConfigurationTypeDef",
    "StreamingImageTypeDef",
    "StreamingSessionStorageRootTypeDef",
    "StreamingSessionStreamTypeDef",
    "StreamingSessionTypeDef",
    "StudioComponentConfigurationTypeDef",
    "StudioComponentInitializationScriptTypeDef",
    "StudioComponentSummaryTypeDef",
    "StudioComponentTypeDef",
    "StudioEncryptionConfigurationTypeDef",
    "StudioMembershipTypeDef",
    "StudioTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateLaunchProfileMemberRequestRequestTypeDef",
    "UpdateLaunchProfileMemberResponseTypeDef",
    "UpdateLaunchProfileRequestRequestTypeDef",
    "UpdateLaunchProfileResponseTypeDef",
    "UpdateStreamingImageRequestRequestTypeDef",
    "UpdateStreamingImageResponseTypeDef",
    "UpdateStudioComponentRequestRequestTypeDef",
    "UpdateStudioComponentResponseTypeDef",
    "UpdateStudioRequestRequestTypeDef",
    "UpdateStudioResponseTypeDef",
    "ValidationResultTypeDef",
    "WaiterConfigTypeDef",
)

_RequiredAcceptEulasRequestRequestTypeDef = TypedDict(
    "_RequiredAcceptEulasRequestRequestTypeDef",
    {
        "studioId": str,
    },
)
_OptionalAcceptEulasRequestRequestTypeDef = TypedDict(
    "_OptionalAcceptEulasRequestRequestTypeDef",
    {
        "clientToken": str,
        "eulaIds": Sequence[str],
    },
    total=False,
)


class AcceptEulasRequestRequestTypeDef(
    _RequiredAcceptEulasRequestRequestTypeDef, _OptionalAcceptEulasRequestRequestTypeDef
):
    pass


AcceptEulasResponseTypeDef = TypedDict(
    "AcceptEulasResponseTypeDef",
    {
        "eulaAcceptances": List["EulaAcceptanceTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ActiveDirectoryComputerAttributeTypeDef = TypedDict(
    "ActiveDirectoryComputerAttributeTypeDef",
    {
        "name": str,
        "value": str,
    },
    total=False,
)

ActiveDirectoryConfigurationTypeDef = TypedDict(
    "ActiveDirectoryConfigurationTypeDef",
    {
        "computerAttributes": Sequence["ActiveDirectoryComputerAttributeTypeDef"],
        "directoryId": str,
        "organizationalUnitDistinguishedName": str,
    },
    total=False,
)

ComputeFarmConfigurationTypeDef = TypedDict(
    "ComputeFarmConfigurationTypeDef",
    {
        "activeDirectoryUser": str,
        "endpoint": str,
    },
    total=False,
)

_RequiredCreateLaunchProfileRequestRequestTypeDef = TypedDict(
    "_RequiredCreateLaunchProfileRequestRequestTypeDef",
    {
        "ec2SubnetIds": Sequence[str],
        "launchProfileProtocolVersions": Sequence[str],
        "name": str,
        "streamConfiguration": "StreamConfigurationCreateTypeDef",
        "studioComponentIds": Sequence[str],
        "studioId": str,
    },
)
_OptionalCreateLaunchProfileRequestRequestTypeDef = TypedDict(
    "_OptionalCreateLaunchProfileRequestRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateLaunchProfileRequestRequestTypeDef(
    _RequiredCreateLaunchProfileRequestRequestTypeDef,
    _OptionalCreateLaunchProfileRequestRequestTypeDef,
):
    pass


CreateLaunchProfileResponseTypeDef = TypedDict(
    "CreateLaunchProfileResponseTypeDef",
    {
        "launchProfile": "LaunchProfileTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateStreamingImageRequestRequestTypeDef = TypedDict(
    "_RequiredCreateStreamingImageRequestRequestTypeDef",
    {
        "ec2ImageId": str,
        "name": str,
        "studioId": str,
    },
)
_OptionalCreateStreamingImageRequestRequestTypeDef = TypedDict(
    "_OptionalCreateStreamingImageRequestRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateStreamingImageRequestRequestTypeDef(
    _RequiredCreateStreamingImageRequestRequestTypeDef,
    _OptionalCreateStreamingImageRequestRequestTypeDef,
):
    pass


CreateStreamingImageResponseTypeDef = TypedDict(
    "CreateStreamingImageResponseTypeDef",
    {
        "streamingImage": "StreamingImageTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateStreamingSessionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateStreamingSessionRequestRequestTypeDef",
    {
        "studioId": str,
    },
)
_OptionalCreateStreamingSessionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateStreamingSessionRequestRequestTypeDef",
    {
        "clientToken": str,
        "ec2InstanceType": StreamingInstanceTypeType,
        "launchProfileId": str,
        "ownedBy": str,
        "streamingImageId": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateStreamingSessionRequestRequestTypeDef(
    _RequiredCreateStreamingSessionRequestRequestTypeDef,
    _OptionalCreateStreamingSessionRequestRequestTypeDef,
):
    pass


CreateStreamingSessionResponseTypeDef = TypedDict(
    "CreateStreamingSessionResponseTypeDef",
    {
        "session": "StreamingSessionTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateStreamingSessionStreamRequestRequestTypeDef = TypedDict(
    "_RequiredCreateStreamingSessionStreamRequestRequestTypeDef",
    {
        "sessionId": str,
        "studioId": str,
    },
)
_OptionalCreateStreamingSessionStreamRequestRequestTypeDef = TypedDict(
    "_OptionalCreateStreamingSessionStreamRequestRequestTypeDef",
    {
        "clientToken": str,
        "expirationInSeconds": int,
    },
    total=False,
)


class CreateStreamingSessionStreamRequestRequestTypeDef(
    _RequiredCreateStreamingSessionStreamRequestRequestTypeDef,
    _OptionalCreateStreamingSessionStreamRequestRequestTypeDef,
):
    pass


CreateStreamingSessionStreamResponseTypeDef = TypedDict(
    "CreateStreamingSessionStreamResponseTypeDef",
    {
        "stream": "StreamingSessionStreamTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateStudioComponentRequestRequestTypeDef = TypedDict(
    "_RequiredCreateStudioComponentRequestRequestTypeDef",
    {
        "name": str,
        "studioId": str,
        "type": StudioComponentTypeType,
    },
)
_OptionalCreateStudioComponentRequestRequestTypeDef = TypedDict(
    "_OptionalCreateStudioComponentRequestRequestTypeDef",
    {
        "clientToken": str,
        "configuration": "StudioComponentConfigurationTypeDef",
        "description": str,
        "ec2SecurityGroupIds": Sequence[str],
        "initializationScripts": Sequence["StudioComponentInitializationScriptTypeDef"],
        "scriptParameters": Sequence["ScriptParameterKeyValueTypeDef"],
        "subtype": StudioComponentSubtypeType,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateStudioComponentRequestRequestTypeDef(
    _RequiredCreateStudioComponentRequestRequestTypeDef,
    _OptionalCreateStudioComponentRequestRequestTypeDef,
):
    pass


CreateStudioComponentResponseTypeDef = TypedDict(
    "CreateStudioComponentResponseTypeDef",
    {
        "studioComponent": "StudioComponentTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateStudioRequestRequestTypeDef = TypedDict(
    "_RequiredCreateStudioRequestRequestTypeDef",
    {
        "adminRoleArn": str,
        "displayName": str,
        "studioName": str,
        "userRoleArn": str,
    },
)
_OptionalCreateStudioRequestRequestTypeDef = TypedDict(
    "_OptionalCreateStudioRequestRequestTypeDef",
    {
        "clientToken": str,
        "studioEncryptionConfiguration": "StudioEncryptionConfigurationTypeDef",
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateStudioRequestRequestTypeDef(
    _RequiredCreateStudioRequestRequestTypeDef, _OptionalCreateStudioRequestRequestTypeDef
):
    pass


CreateStudioResponseTypeDef = TypedDict(
    "CreateStudioResponseTypeDef",
    {
        "studio": "StudioTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDeleteLaunchProfileMemberRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteLaunchProfileMemberRequestRequestTypeDef",
    {
        "launchProfileId": str,
        "principalId": str,
        "studioId": str,
    },
)
_OptionalDeleteLaunchProfileMemberRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteLaunchProfileMemberRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeleteLaunchProfileMemberRequestRequestTypeDef(
    _RequiredDeleteLaunchProfileMemberRequestRequestTypeDef,
    _OptionalDeleteLaunchProfileMemberRequestRequestTypeDef,
):
    pass


_RequiredDeleteLaunchProfileRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteLaunchProfileRequestRequestTypeDef",
    {
        "launchProfileId": str,
        "studioId": str,
    },
)
_OptionalDeleteLaunchProfileRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteLaunchProfileRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeleteLaunchProfileRequestRequestTypeDef(
    _RequiredDeleteLaunchProfileRequestRequestTypeDef,
    _OptionalDeleteLaunchProfileRequestRequestTypeDef,
):
    pass


DeleteLaunchProfileResponseTypeDef = TypedDict(
    "DeleteLaunchProfileResponseTypeDef",
    {
        "launchProfile": "LaunchProfileTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDeleteStreamingImageRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteStreamingImageRequestRequestTypeDef",
    {
        "streamingImageId": str,
        "studioId": str,
    },
)
_OptionalDeleteStreamingImageRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteStreamingImageRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeleteStreamingImageRequestRequestTypeDef(
    _RequiredDeleteStreamingImageRequestRequestTypeDef,
    _OptionalDeleteStreamingImageRequestRequestTypeDef,
):
    pass


DeleteStreamingImageResponseTypeDef = TypedDict(
    "DeleteStreamingImageResponseTypeDef",
    {
        "streamingImage": "StreamingImageTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDeleteStreamingSessionRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteStreamingSessionRequestRequestTypeDef",
    {
        "sessionId": str,
        "studioId": str,
    },
)
_OptionalDeleteStreamingSessionRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteStreamingSessionRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeleteStreamingSessionRequestRequestTypeDef(
    _RequiredDeleteStreamingSessionRequestRequestTypeDef,
    _OptionalDeleteStreamingSessionRequestRequestTypeDef,
):
    pass


DeleteStreamingSessionResponseTypeDef = TypedDict(
    "DeleteStreamingSessionResponseTypeDef",
    {
        "session": "StreamingSessionTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDeleteStudioComponentRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteStudioComponentRequestRequestTypeDef",
    {
        "studioComponentId": str,
        "studioId": str,
    },
)
_OptionalDeleteStudioComponentRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteStudioComponentRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeleteStudioComponentRequestRequestTypeDef(
    _RequiredDeleteStudioComponentRequestRequestTypeDef,
    _OptionalDeleteStudioComponentRequestRequestTypeDef,
):
    pass


DeleteStudioComponentResponseTypeDef = TypedDict(
    "DeleteStudioComponentResponseTypeDef",
    {
        "studioComponent": "StudioComponentTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDeleteStudioMemberRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteStudioMemberRequestRequestTypeDef",
    {
        "principalId": str,
        "studioId": str,
    },
)
_OptionalDeleteStudioMemberRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteStudioMemberRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeleteStudioMemberRequestRequestTypeDef(
    _RequiredDeleteStudioMemberRequestRequestTypeDef,
    _OptionalDeleteStudioMemberRequestRequestTypeDef,
):
    pass


_RequiredDeleteStudioRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteStudioRequestRequestTypeDef",
    {
        "studioId": str,
    },
)
_OptionalDeleteStudioRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteStudioRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeleteStudioRequestRequestTypeDef(
    _RequiredDeleteStudioRequestRequestTypeDef, _OptionalDeleteStudioRequestRequestTypeDef
):
    pass


DeleteStudioResponseTypeDef = TypedDict(
    "DeleteStudioResponseTypeDef",
    {
        "studio": "StudioTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

EulaAcceptanceTypeDef = TypedDict(
    "EulaAcceptanceTypeDef",
    {
        "acceptedAt": datetime,
        "acceptedBy": str,
        "accepteeId": str,
        "eulaAcceptanceId": str,
        "eulaId": str,
    },
    total=False,
)

EulaTypeDef = TypedDict(
    "EulaTypeDef",
    {
        "content": str,
        "createdAt": datetime,
        "eulaId": str,
        "name": str,
        "updatedAt": datetime,
    },
    total=False,
)

GetEulaRequestRequestTypeDef = TypedDict(
    "GetEulaRequestRequestTypeDef",
    {
        "eulaId": str,
    },
)

GetEulaResponseTypeDef = TypedDict(
    "GetEulaResponseTypeDef",
    {
        "eula": "EulaTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetLaunchProfileDetailsRequestRequestTypeDef = TypedDict(
    "GetLaunchProfileDetailsRequestRequestTypeDef",
    {
        "launchProfileId": str,
        "studioId": str,
    },
)

GetLaunchProfileDetailsResponseTypeDef = TypedDict(
    "GetLaunchProfileDetailsResponseTypeDef",
    {
        "launchProfile": "LaunchProfileTypeDef",
        "streamingImages": List["StreamingImageTypeDef"],
        "studioComponentSummaries": List["StudioComponentSummaryTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetLaunchProfileInitializationRequestRequestTypeDef = TypedDict(
    "GetLaunchProfileInitializationRequestRequestTypeDef",
    {
        "launchProfileId": str,
        "launchProfileProtocolVersions": Sequence[str],
        "launchPurpose": str,
        "platform": str,
        "studioId": str,
    },
)

GetLaunchProfileInitializationResponseTypeDef = TypedDict(
    "GetLaunchProfileInitializationResponseTypeDef",
    {
        "launchProfileInitialization": "LaunchProfileInitializationTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetLaunchProfileMemberRequestRequestTypeDef = TypedDict(
    "GetLaunchProfileMemberRequestRequestTypeDef",
    {
        "launchProfileId": str,
        "principalId": str,
        "studioId": str,
    },
)

GetLaunchProfileMemberResponseTypeDef = TypedDict(
    "GetLaunchProfileMemberResponseTypeDef",
    {
        "member": "LaunchProfileMembershipTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGetLaunchProfileRequestLaunchProfileDeletedWaitTypeDef = TypedDict(
    "_RequiredGetLaunchProfileRequestLaunchProfileDeletedWaitTypeDef",
    {
        "launchProfileId": str,
        "studioId": str,
    },
)
_OptionalGetLaunchProfileRequestLaunchProfileDeletedWaitTypeDef = TypedDict(
    "_OptionalGetLaunchProfileRequestLaunchProfileDeletedWaitTypeDef",
    {
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)


class GetLaunchProfileRequestLaunchProfileDeletedWaitTypeDef(
    _RequiredGetLaunchProfileRequestLaunchProfileDeletedWaitTypeDef,
    _OptionalGetLaunchProfileRequestLaunchProfileDeletedWaitTypeDef,
):
    pass


_RequiredGetLaunchProfileRequestLaunchProfileReadyWaitTypeDef = TypedDict(
    "_RequiredGetLaunchProfileRequestLaunchProfileReadyWaitTypeDef",
    {
        "launchProfileId": str,
        "studioId": str,
    },
)
_OptionalGetLaunchProfileRequestLaunchProfileReadyWaitTypeDef = TypedDict(
    "_OptionalGetLaunchProfileRequestLaunchProfileReadyWaitTypeDef",
    {
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)


class GetLaunchProfileRequestLaunchProfileReadyWaitTypeDef(
    _RequiredGetLaunchProfileRequestLaunchProfileReadyWaitTypeDef,
    _OptionalGetLaunchProfileRequestLaunchProfileReadyWaitTypeDef,
):
    pass


GetLaunchProfileRequestRequestTypeDef = TypedDict(
    "GetLaunchProfileRequestRequestTypeDef",
    {
        "launchProfileId": str,
        "studioId": str,
    },
)

GetLaunchProfileResponseTypeDef = TypedDict(
    "GetLaunchProfileResponseTypeDef",
    {
        "launchProfile": "LaunchProfileTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetStreamingImageRequestRequestTypeDef = TypedDict(
    "GetStreamingImageRequestRequestTypeDef",
    {
        "streamingImageId": str,
        "studioId": str,
    },
)

_RequiredGetStreamingImageRequestStreamingImageDeletedWaitTypeDef = TypedDict(
    "_RequiredGetStreamingImageRequestStreamingImageDeletedWaitTypeDef",
    {
        "streamingImageId": str,
        "studioId": str,
    },
)
_OptionalGetStreamingImageRequestStreamingImageDeletedWaitTypeDef = TypedDict(
    "_OptionalGetStreamingImageRequestStreamingImageDeletedWaitTypeDef",
    {
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)


class GetStreamingImageRequestStreamingImageDeletedWaitTypeDef(
    _RequiredGetStreamingImageRequestStreamingImageDeletedWaitTypeDef,
    _OptionalGetStreamingImageRequestStreamingImageDeletedWaitTypeDef,
):
    pass


_RequiredGetStreamingImageRequestStreamingImageReadyWaitTypeDef = TypedDict(
    "_RequiredGetStreamingImageRequestStreamingImageReadyWaitTypeDef",
    {
        "streamingImageId": str,
        "studioId": str,
    },
)
_OptionalGetStreamingImageRequestStreamingImageReadyWaitTypeDef = TypedDict(
    "_OptionalGetStreamingImageRequestStreamingImageReadyWaitTypeDef",
    {
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)


class GetStreamingImageRequestStreamingImageReadyWaitTypeDef(
    _RequiredGetStreamingImageRequestStreamingImageReadyWaitTypeDef,
    _OptionalGetStreamingImageRequestStreamingImageReadyWaitTypeDef,
):
    pass


GetStreamingImageResponseTypeDef = TypedDict(
    "GetStreamingImageResponseTypeDef",
    {
        "streamingImage": "StreamingImageTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetStreamingSessionRequestRequestTypeDef = TypedDict(
    "GetStreamingSessionRequestRequestTypeDef",
    {
        "sessionId": str,
        "studioId": str,
    },
)

_RequiredGetStreamingSessionRequestStreamingSessionDeletedWaitTypeDef = TypedDict(
    "_RequiredGetStreamingSessionRequestStreamingSessionDeletedWaitTypeDef",
    {
        "sessionId": str,
        "studioId": str,
    },
)
_OptionalGetStreamingSessionRequestStreamingSessionDeletedWaitTypeDef = TypedDict(
    "_OptionalGetStreamingSessionRequestStreamingSessionDeletedWaitTypeDef",
    {
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)


class GetStreamingSessionRequestStreamingSessionDeletedWaitTypeDef(
    _RequiredGetStreamingSessionRequestStreamingSessionDeletedWaitTypeDef,
    _OptionalGetStreamingSessionRequestStreamingSessionDeletedWaitTypeDef,
):
    pass


_RequiredGetStreamingSessionRequestStreamingSessionReadyWaitTypeDef = TypedDict(
    "_RequiredGetStreamingSessionRequestStreamingSessionReadyWaitTypeDef",
    {
        "sessionId": str,
        "studioId": str,
    },
)
_OptionalGetStreamingSessionRequestStreamingSessionReadyWaitTypeDef = TypedDict(
    "_OptionalGetStreamingSessionRequestStreamingSessionReadyWaitTypeDef",
    {
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)


class GetStreamingSessionRequestStreamingSessionReadyWaitTypeDef(
    _RequiredGetStreamingSessionRequestStreamingSessionReadyWaitTypeDef,
    _OptionalGetStreamingSessionRequestStreamingSessionReadyWaitTypeDef,
):
    pass


_RequiredGetStreamingSessionRequestStreamingSessionStoppedWaitTypeDef = TypedDict(
    "_RequiredGetStreamingSessionRequestStreamingSessionStoppedWaitTypeDef",
    {
        "sessionId": str,
        "studioId": str,
    },
)
_OptionalGetStreamingSessionRequestStreamingSessionStoppedWaitTypeDef = TypedDict(
    "_OptionalGetStreamingSessionRequestStreamingSessionStoppedWaitTypeDef",
    {
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)


class GetStreamingSessionRequestStreamingSessionStoppedWaitTypeDef(
    _RequiredGetStreamingSessionRequestStreamingSessionStoppedWaitTypeDef,
    _OptionalGetStreamingSessionRequestStreamingSessionStoppedWaitTypeDef,
):
    pass


GetStreamingSessionResponseTypeDef = TypedDict(
    "GetStreamingSessionResponseTypeDef",
    {
        "session": "StreamingSessionTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetStreamingSessionStreamRequestRequestTypeDef = TypedDict(
    "GetStreamingSessionStreamRequestRequestTypeDef",
    {
        "sessionId": str,
        "streamId": str,
        "studioId": str,
    },
)

_RequiredGetStreamingSessionStreamRequestStreamingSessionStreamReadyWaitTypeDef = TypedDict(
    "_RequiredGetStreamingSessionStreamRequestStreamingSessionStreamReadyWaitTypeDef",
    {
        "sessionId": str,
        "streamId": str,
        "studioId": str,
    },
)
_OptionalGetStreamingSessionStreamRequestStreamingSessionStreamReadyWaitTypeDef = TypedDict(
    "_OptionalGetStreamingSessionStreamRequestStreamingSessionStreamReadyWaitTypeDef",
    {
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)


class GetStreamingSessionStreamRequestStreamingSessionStreamReadyWaitTypeDef(
    _RequiredGetStreamingSessionStreamRequestStreamingSessionStreamReadyWaitTypeDef,
    _OptionalGetStreamingSessionStreamRequestStreamingSessionStreamReadyWaitTypeDef,
):
    pass


GetStreamingSessionStreamResponseTypeDef = TypedDict(
    "GetStreamingSessionStreamResponseTypeDef",
    {
        "stream": "StreamingSessionStreamTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetStudioComponentRequestRequestTypeDef = TypedDict(
    "GetStudioComponentRequestRequestTypeDef",
    {
        "studioComponentId": str,
        "studioId": str,
    },
)

_RequiredGetStudioComponentRequestStudioComponentDeletedWaitTypeDef = TypedDict(
    "_RequiredGetStudioComponentRequestStudioComponentDeletedWaitTypeDef",
    {
        "studioComponentId": str,
        "studioId": str,
    },
)
_OptionalGetStudioComponentRequestStudioComponentDeletedWaitTypeDef = TypedDict(
    "_OptionalGetStudioComponentRequestStudioComponentDeletedWaitTypeDef",
    {
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)


class GetStudioComponentRequestStudioComponentDeletedWaitTypeDef(
    _RequiredGetStudioComponentRequestStudioComponentDeletedWaitTypeDef,
    _OptionalGetStudioComponentRequestStudioComponentDeletedWaitTypeDef,
):
    pass


_RequiredGetStudioComponentRequestStudioComponentReadyWaitTypeDef = TypedDict(
    "_RequiredGetStudioComponentRequestStudioComponentReadyWaitTypeDef",
    {
        "studioComponentId": str,
        "studioId": str,
    },
)
_OptionalGetStudioComponentRequestStudioComponentReadyWaitTypeDef = TypedDict(
    "_OptionalGetStudioComponentRequestStudioComponentReadyWaitTypeDef",
    {
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)


class GetStudioComponentRequestStudioComponentReadyWaitTypeDef(
    _RequiredGetStudioComponentRequestStudioComponentReadyWaitTypeDef,
    _OptionalGetStudioComponentRequestStudioComponentReadyWaitTypeDef,
):
    pass


GetStudioComponentResponseTypeDef = TypedDict(
    "GetStudioComponentResponseTypeDef",
    {
        "studioComponent": "StudioComponentTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetStudioMemberRequestRequestTypeDef = TypedDict(
    "GetStudioMemberRequestRequestTypeDef",
    {
        "principalId": str,
        "studioId": str,
    },
)

GetStudioMemberResponseTypeDef = TypedDict(
    "GetStudioMemberResponseTypeDef",
    {
        "member": "StudioMembershipTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetStudioRequestRequestTypeDef = TypedDict(
    "GetStudioRequestRequestTypeDef",
    {
        "studioId": str,
    },
)

_RequiredGetStudioRequestStudioDeletedWaitTypeDef = TypedDict(
    "_RequiredGetStudioRequestStudioDeletedWaitTypeDef",
    {
        "studioId": str,
    },
)
_OptionalGetStudioRequestStudioDeletedWaitTypeDef = TypedDict(
    "_OptionalGetStudioRequestStudioDeletedWaitTypeDef",
    {
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)


class GetStudioRequestStudioDeletedWaitTypeDef(
    _RequiredGetStudioRequestStudioDeletedWaitTypeDef,
    _OptionalGetStudioRequestStudioDeletedWaitTypeDef,
):
    pass


_RequiredGetStudioRequestStudioReadyWaitTypeDef = TypedDict(
    "_RequiredGetStudioRequestStudioReadyWaitTypeDef",
    {
        "studioId": str,
    },
)
_OptionalGetStudioRequestStudioReadyWaitTypeDef = TypedDict(
    "_OptionalGetStudioRequestStudioReadyWaitTypeDef",
    {
        "WaiterConfig": "WaiterConfigTypeDef",
    },
    total=False,
)


class GetStudioRequestStudioReadyWaitTypeDef(
    _RequiredGetStudioRequestStudioReadyWaitTypeDef, _OptionalGetStudioRequestStudioReadyWaitTypeDef
):
    pass


GetStudioResponseTypeDef = TypedDict(
    "GetStudioResponseTypeDef",
    {
        "studio": "StudioTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

LaunchProfileInitializationActiveDirectoryTypeDef = TypedDict(
    "LaunchProfileInitializationActiveDirectoryTypeDef",
    {
        "computerAttributes": List["ActiveDirectoryComputerAttributeTypeDef"],
        "directoryId": str,
        "directoryName": str,
        "dnsIpAddresses": List[str],
        "organizationalUnitDistinguishedName": str,
        "studioComponentId": str,
        "studioComponentName": str,
    },
    total=False,
)

LaunchProfileInitializationScriptTypeDef = TypedDict(
    "LaunchProfileInitializationScriptTypeDef",
    {
        "script": str,
        "studioComponentId": str,
        "studioComponentName": str,
    },
    total=False,
)

LaunchProfileInitializationTypeDef = TypedDict(
    "LaunchProfileInitializationTypeDef",
    {
        "activeDirectory": "LaunchProfileInitializationActiveDirectoryTypeDef",
        "ec2SecurityGroupIds": List[str],
        "launchProfileId": str,
        "launchProfileProtocolVersion": str,
        "launchPurpose": str,
        "name": str,
        "platform": LaunchProfilePlatformType,
        "systemInitializationScripts": List["LaunchProfileInitializationScriptTypeDef"],
        "userInitializationScripts": List["LaunchProfileInitializationScriptTypeDef"],
    },
    total=False,
)

LaunchProfileMembershipTypeDef = TypedDict(
    "LaunchProfileMembershipTypeDef",
    {
        "identityStoreId": str,
        "persona": Literal["USER"],
        "principalId": str,
        "sid": str,
    },
    total=False,
)

LaunchProfileTypeDef = TypedDict(
    "LaunchProfileTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "ec2SubnetIds": List[str],
        "launchProfileId": str,
        "launchProfileProtocolVersions": List[str],
        "name": str,
        "state": LaunchProfileStateType,
        "statusCode": LaunchProfileStatusCodeType,
        "statusMessage": str,
        "streamConfiguration": "StreamConfigurationTypeDef",
        "studioComponentIds": List[str],
        "tags": Dict[str, str],
        "updatedAt": datetime,
        "updatedBy": str,
        "validationResults": List["ValidationResultTypeDef"],
    },
    total=False,
)

LicenseServiceConfigurationTypeDef = TypedDict(
    "LicenseServiceConfigurationTypeDef",
    {
        "endpoint": str,
    },
    total=False,
)

_RequiredListEulaAcceptancesRequestListEulaAcceptancesPaginateTypeDef = TypedDict(
    "_RequiredListEulaAcceptancesRequestListEulaAcceptancesPaginateTypeDef",
    {
        "studioId": str,
    },
)
_OptionalListEulaAcceptancesRequestListEulaAcceptancesPaginateTypeDef = TypedDict(
    "_OptionalListEulaAcceptancesRequestListEulaAcceptancesPaginateTypeDef",
    {
        "eulaIds": Sequence[str],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListEulaAcceptancesRequestListEulaAcceptancesPaginateTypeDef(
    _RequiredListEulaAcceptancesRequestListEulaAcceptancesPaginateTypeDef,
    _OptionalListEulaAcceptancesRequestListEulaAcceptancesPaginateTypeDef,
):
    pass


_RequiredListEulaAcceptancesRequestRequestTypeDef = TypedDict(
    "_RequiredListEulaAcceptancesRequestRequestTypeDef",
    {
        "studioId": str,
    },
)
_OptionalListEulaAcceptancesRequestRequestTypeDef = TypedDict(
    "_OptionalListEulaAcceptancesRequestRequestTypeDef",
    {
        "eulaIds": Sequence[str],
        "nextToken": str,
    },
    total=False,
)


class ListEulaAcceptancesRequestRequestTypeDef(
    _RequiredListEulaAcceptancesRequestRequestTypeDef,
    _OptionalListEulaAcceptancesRequestRequestTypeDef,
):
    pass


ListEulaAcceptancesResponseTypeDef = TypedDict(
    "ListEulaAcceptancesResponseTypeDef",
    {
        "eulaAcceptances": List["EulaAcceptanceTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListEulasRequestListEulasPaginateTypeDef = TypedDict(
    "ListEulasRequestListEulasPaginateTypeDef",
    {
        "eulaIds": Sequence[str],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListEulasRequestRequestTypeDef = TypedDict(
    "ListEulasRequestRequestTypeDef",
    {
        "eulaIds": Sequence[str],
        "nextToken": str,
    },
    total=False,
)

ListEulasResponseTypeDef = TypedDict(
    "ListEulasResponseTypeDef",
    {
        "eulas": List["EulaTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListLaunchProfileMembersRequestListLaunchProfileMembersPaginateTypeDef = TypedDict(
    "_RequiredListLaunchProfileMembersRequestListLaunchProfileMembersPaginateTypeDef",
    {
        "launchProfileId": str,
        "studioId": str,
    },
)
_OptionalListLaunchProfileMembersRequestListLaunchProfileMembersPaginateTypeDef = TypedDict(
    "_OptionalListLaunchProfileMembersRequestListLaunchProfileMembersPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListLaunchProfileMembersRequestListLaunchProfileMembersPaginateTypeDef(
    _RequiredListLaunchProfileMembersRequestListLaunchProfileMembersPaginateTypeDef,
    _OptionalListLaunchProfileMembersRequestListLaunchProfileMembersPaginateTypeDef,
):
    pass


_RequiredListLaunchProfileMembersRequestRequestTypeDef = TypedDict(
    "_RequiredListLaunchProfileMembersRequestRequestTypeDef",
    {
        "launchProfileId": str,
        "studioId": str,
    },
)
_OptionalListLaunchProfileMembersRequestRequestTypeDef = TypedDict(
    "_OptionalListLaunchProfileMembersRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListLaunchProfileMembersRequestRequestTypeDef(
    _RequiredListLaunchProfileMembersRequestRequestTypeDef,
    _OptionalListLaunchProfileMembersRequestRequestTypeDef,
):
    pass


ListLaunchProfileMembersResponseTypeDef = TypedDict(
    "ListLaunchProfileMembersResponseTypeDef",
    {
        "members": List["LaunchProfileMembershipTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListLaunchProfilesRequestListLaunchProfilesPaginateTypeDef = TypedDict(
    "_RequiredListLaunchProfilesRequestListLaunchProfilesPaginateTypeDef",
    {
        "studioId": str,
    },
)
_OptionalListLaunchProfilesRequestListLaunchProfilesPaginateTypeDef = TypedDict(
    "_OptionalListLaunchProfilesRequestListLaunchProfilesPaginateTypeDef",
    {
        "principalId": str,
        "states": Sequence[LaunchProfileStateType],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListLaunchProfilesRequestListLaunchProfilesPaginateTypeDef(
    _RequiredListLaunchProfilesRequestListLaunchProfilesPaginateTypeDef,
    _OptionalListLaunchProfilesRequestListLaunchProfilesPaginateTypeDef,
):
    pass


_RequiredListLaunchProfilesRequestRequestTypeDef = TypedDict(
    "_RequiredListLaunchProfilesRequestRequestTypeDef",
    {
        "studioId": str,
    },
)
_OptionalListLaunchProfilesRequestRequestTypeDef = TypedDict(
    "_OptionalListLaunchProfilesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "principalId": str,
        "states": Sequence[LaunchProfileStateType],
    },
    total=False,
)


class ListLaunchProfilesRequestRequestTypeDef(
    _RequiredListLaunchProfilesRequestRequestTypeDef,
    _OptionalListLaunchProfilesRequestRequestTypeDef,
):
    pass


ListLaunchProfilesResponseTypeDef = TypedDict(
    "ListLaunchProfilesResponseTypeDef",
    {
        "launchProfiles": List["LaunchProfileTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListStreamingImagesRequestListStreamingImagesPaginateTypeDef = TypedDict(
    "_RequiredListStreamingImagesRequestListStreamingImagesPaginateTypeDef",
    {
        "studioId": str,
    },
)
_OptionalListStreamingImagesRequestListStreamingImagesPaginateTypeDef = TypedDict(
    "_OptionalListStreamingImagesRequestListStreamingImagesPaginateTypeDef",
    {
        "owner": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListStreamingImagesRequestListStreamingImagesPaginateTypeDef(
    _RequiredListStreamingImagesRequestListStreamingImagesPaginateTypeDef,
    _OptionalListStreamingImagesRequestListStreamingImagesPaginateTypeDef,
):
    pass


_RequiredListStreamingImagesRequestRequestTypeDef = TypedDict(
    "_RequiredListStreamingImagesRequestRequestTypeDef",
    {
        "studioId": str,
    },
)
_OptionalListStreamingImagesRequestRequestTypeDef = TypedDict(
    "_OptionalListStreamingImagesRequestRequestTypeDef",
    {
        "nextToken": str,
        "owner": str,
    },
    total=False,
)


class ListStreamingImagesRequestRequestTypeDef(
    _RequiredListStreamingImagesRequestRequestTypeDef,
    _OptionalListStreamingImagesRequestRequestTypeDef,
):
    pass


ListStreamingImagesResponseTypeDef = TypedDict(
    "ListStreamingImagesResponseTypeDef",
    {
        "nextToken": str,
        "streamingImages": List["StreamingImageTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListStreamingSessionsRequestListStreamingSessionsPaginateTypeDef = TypedDict(
    "_RequiredListStreamingSessionsRequestListStreamingSessionsPaginateTypeDef",
    {
        "studioId": str,
    },
)
_OptionalListStreamingSessionsRequestListStreamingSessionsPaginateTypeDef = TypedDict(
    "_OptionalListStreamingSessionsRequestListStreamingSessionsPaginateTypeDef",
    {
        "createdBy": str,
        "ownedBy": str,
        "sessionIds": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListStreamingSessionsRequestListStreamingSessionsPaginateTypeDef(
    _RequiredListStreamingSessionsRequestListStreamingSessionsPaginateTypeDef,
    _OptionalListStreamingSessionsRequestListStreamingSessionsPaginateTypeDef,
):
    pass


_RequiredListStreamingSessionsRequestRequestTypeDef = TypedDict(
    "_RequiredListStreamingSessionsRequestRequestTypeDef",
    {
        "studioId": str,
    },
)
_OptionalListStreamingSessionsRequestRequestTypeDef = TypedDict(
    "_OptionalListStreamingSessionsRequestRequestTypeDef",
    {
        "createdBy": str,
        "nextToken": str,
        "ownedBy": str,
        "sessionIds": str,
    },
    total=False,
)


class ListStreamingSessionsRequestRequestTypeDef(
    _RequiredListStreamingSessionsRequestRequestTypeDef,
    _OptionalListStreamingSessionsRequestRequestTypeDef,
):
    pass


ListStreamingSessionsResponseTypeDef = TypedDict(
    "ListStreamingSessionsResponseTypeDef",
    {
        "nextToken": str,
        "sessions": List["StreamingSessionTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListStudioComponentsRequestListStudioComponentsPaginateTypeDef = TypedDict(
    "_RequiredListStudioComponentsRequestListStudioComponentsPaginateTypeDef",
    {
        "studioId": str,
    },
)
_OptionalListStudioComponentsRequestListStudioComponentsPaginateTypeDef = TypedDict(
    "_OptionalListStudioComponentsRequestListStudioComponentsPaginateTypeDef",
    {
        "states": Sequence[StudioComponentStateType],
        "types": Sequence[StudioComponentTypeType],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListStudioComponentsRequestListStudioComponentsPaginateTypeDef(
    _RequiredListStudioComponentsRequestListStudioComponentsPaginateTypeDef,
    _OptionalListStudioComponentsRequestListStudioComponentsPaginateTypeDef,
):
    pass


_RequiredListStudioComponentsRequestRequestTypeDef = TypedDict(
    "_RequiredListStudioComponentsRequestRequestTypeDef",
    {
        "studioId": str,
    },
)
_OptionalListStudioComponentsRequestRequestTypeDef = TypedDict(
    "_OptionalListStudioComponentsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "states": Sequence[StudioComponentStateType],
        "types": Sequence[StudioComponentTypeType],
    },
    total=False,
)


class ListStudioComponentsRequestRequestTypeDef(
    _RequiredListStudioComponentsRequestRequestTypeDef,
    _OptionalListStudioComponentsRequestRequestTypeDef,
):
    pass


ListStudioComponentsResponseTypeDef = TypedDict(
    "ListStudioComponentsResponseTypeDef",
    {
        "nextToken": str,
        "studioComponents": List["StudioComponentTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListStudioMembersRequestListStudioMembersPaginateTypeDef = TypedDict(
    "_RequiredListStudioMembersRequestListStudioMembersPaginateTypeDef",
    {
        "studioId": str,
    },
)
_OptionalListStudioMembersRequestListStudioMembersPaginateTypeDef = TypedDict(
    "_OptionalListStudioMembersRequestListStudioMembersPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListStudioMembersRequestListStudioMembersPaginateTypeDef(
    _RequiredListStudioMembersRequestListStudioMembersPaginateTypeDef,
    _OptionalListStudioMembersRequestListStudioMembersPaginateTypeDef,
):
    pass


_RequiredListStudioMembersRequestRequestTypeDef = TypedDict(
    "_RequiredListStudioMembersRequestRequestTypeDef",
    {
        "studioId": str,
    },
)
_OptionalListStudioMembersRequestRequestTypeDef = TypedDict(
    "_OptionalListStudioMembersRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListStudioMembersRequestRequestTypeDef(
    _RequiredListStudioMembersRequestRequestTypeDef, _OptionalListStudioMembersRequestRequestTypeDef
):
    pass


ListStudioMembersResponseTypeDef = TypedDict(
    "ListStudioMembersResponseTypeDef",
    {
        "members": List["StudioMembershipTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListStudiosRequestListStudiosPaginateTypeDef = TypedDict(
    "ListStudiosRequestListStudiosPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListStudiosRequestRequestTypeDef = TypedDict(
    "ListStudiosRequestRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)

ListStudiosResponseTypeDef = TypedDict(
    "ListStudiosResponseTypeDef",
    {
        "nextToken": str,
        "studios": List["StudioTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

NewLaunchProfileMemberTypeDef = TypedDict(
    "NewLaunchProfileMemberTypeDef",
    {
        "persona": Literal["USER"],
        "principalId": str,
    },
)

NewStudioMemberTypeDef = TypedDict(
    "NewStudioMemberTypeDef",
    {
        "persona": Literal["ADMINISTRATOR"],
        "principalId": str,
    },
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

_RequiredPutLaunchProfileMembersRequestRequestTypeDef = TypedDict(
    "_RequiredPutLaunchProfileMembersRequestRequestTypeDef",
    {
        "identityStoreId": str,
        "launchProfileId": str,
        "members": Sequence["NewLaunchProfileMemberTypeDef"],
        "studioId": str,
    },
)
_OptionalPutLaunchProfileMembersRequestRequestTypeDef = TypedDict(
    "_OptionalPutLaunchProfileMembersRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class PutLaunchProfileMembersRequestRequestTypeDef(
    _RequiredPutLaunchProfileMembersRequestRequestTypeDef,
    _OptionalPutLaunchProfileMembersRequestRequestTypeDef,
):
    pass


_RequiredPutStudioMembersRequestRequestTypeDef = TypedDict(
    "_RequiredPutStudioMembersRequestRequestTypeDef",
    {
        "identityStoreId": str,
        "members": Sequence["NewStudioMemberTypeDef"],
        "studioId": str,
    },
)
_OptionalPutStudioMembersRequestRequestTypeDef = TypedDict(
    "_OptionalPutStudioMembersRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class PutStudioMembersRequestRequestTypeDef(
    _RequiredPutStudioMembersRequestRequestTypeDef, _OptionalPutStudioMembersRequestRequestTypeDef
):
    pass


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

ScriptParameterKeyValueTypeDef = TypedDict(
    "ScriptParameterKeyValueTypeDef",
    {
        "key": str,
        "value": str,
    },
    total=False,
)

SharedFileSystemConfigurationTypeDef = TypedDict(
    "SharedFileSystemConfigurationTypeDef",
    {
        "endpoint": str,
        "fileSystemId": str,
        "linuxMountPoint": str,
        "shareName": str,
        "windowsMountDrive": str,
    },
    total=False,
)

_RequiredStartStreamingSessionRequestRequestTypeDef = TypedDict(
    "_RequiredStartStreamingSessionRequestRequestTypeDef",
    {
        "sessionId": str,
        "studioId": str,
    },
)
_OptionalStartStreamingSessionRequestRequestTypeDef = TypedDict(
    "_OptionalStartStreamingSessionRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class StartStreamingSessionRequestRequestTypeDef(
    _RequiredStartStreamingSessionRequestRequestTypeDef,
    _OptionalStartStreamingSessionRequestRequestTypeDef,
):
    pass


StartStreamingSessionResponseTypeDef = TypedDict(
    "StartStreamingSessionResponseTypeDef",
    {
        "session": "StreamingSessionTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredStartStudioSSOConfigurationRepairRequestRequestTypeDef = TypedDict(
    "_RequiredStartStudioSSOConfigurationRepairRequestRequestTypeDef",
    {
        "studioId": str,
    },
)
_OptionalStartStudioSSOConfigurationRepairRequestRequestTypeDef = TypedDict(
    "_OptionalStartStudioSSOConfigurationRepairRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class StartStudioSSOConfigurationRepairRequestRequestTypeDef(
    _RequiredStartStudioSSOConfigurationRepairRequestRequestTypeDef,
    _OptionalStartStudioSSOConfigurationRepairRequestRequestTypeDef,
):
    pass


StartStudioSSOConfigurationRepairResponseTypeDef = TypedDict(
    "StartStudioSSOConfigurationRepairResponseTypeDef",
    {
        "studio": "StudioTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredStopStreamingSessionRequestRequestTypeDef = TypedDict(
    "_RequiredStopStreamingSessionRequestRequestTypeDef",
    {
        "sessionId": str,
        "studioId": str,
    },
)
_OptionalStopStreamingSessionRequestRequestTypeDef = TypedDict(
    "_OptionalStopStreamingSessionRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class StopStreamingSessionRequestRequestTypeDef(
    _RequiredStopStreamingSessionRequestRequestTypeDef,
    _OptionalStopStreamingSessionRequestRequestTypeDef,
):
    pass


StopStreamingSessionResponseTypeDef = TypedDict(
    "StopStreamingSessionResponseTypeDef",
    {
        "session": "StreamingSessionTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredStreamConfigurationCreateTypeDef = TypedDict(
    "_RequiredStreamConfigurationCreateTypeDef",
    {
        "clipboardMode": StreamingClipboardModeType,
        "ec2InstanceTypes": Sequence[StreamingInstanceTypeType],
        "streamingImageIds": Sequence[str],
    },
)
_OptionalStreamConfigurationCreateTypeDef = TypedDict(
    "_OptionalStreamConfigurationCreateTypeDef",
    {
        "maxSessionLengthInMinutes": int,
        "maxStoppedSessionLengthInMinutes": int,
        "sessionStorage": "StreamConfigurationSessionStorageTypeDef",
    },
    total=False,
)


class StreamConfigurationCreateTypeDef(
    _RequiredStreamConfigurationCreateTypeDef, _OptionalStreamConfigurationCreateTypeDef
):
    pass


_RequiredStreamConfigurationSessionStorageTypeDef = TypedDict(
    "_RequiredStreamConfigurationSessionStorageTypeDef",
    {
        "mode": Sequence[Literal["UPLOAD"]],
    },
)
_OptionalStreamConfigurationSessionStorageTypeDef = TypedDict(
    "_OptionalStreamConfigurationSessionStorageTypeDef",
    {
        "root": "StreamingSessionStorageRootTypeDef",
    },
    total=False,
)


class StreamConfigurationSessionStorageTypeDef(
    _RequiredStreamConfigurationSessionStorageTypeDef,
    _OptionalStreamConfigurationSessionStorageTypeDef,
):
    pass


_RequiredStreamConfigurationTypeDef = TypedDict(
    "_RequiredStreamConfigurationTypeDef",
    {
        "clipboardMode": StreamingClipboardModeType,
        "ec2InstanceTypes": List[StreamingInstanceTypeType],
        "streamingImageIds": List[str],
    },
)
_OptionalStreamConfigurationTypeDef = TypedDict(
    "_OptionalStreamConfigurationTypeDef",
    {
        "maxSessionLengthInMinutes": int,
        "maxStoppedSessionLengthInMinutes": int,
        "sessionStorage": "StreamConfigurationSessionStorageTypeDef",
    },
    total=False,
)


class StreamConfigurationTypeDef(
    _RequiredStreamConfigurationTypeDef, _OptionalStreamConfigurationTypeDef
):
    pass


_RequiredStreamingImageEncryptionConfigurationTypeDef = TypedDict(
    "_RequiredStreamingImageEncryptionConfigurationTypeDef",
    {
        "keyType": Literal["CUSTOMER_MANAGED_KEY"],
    },
)
_OptionalStreamingImageEncryptionConfigurationTypeDef = TypedDict(
    "_OptionalStreamingImageEncryptionConfigurationTypeDef",
    {
        "keyArn": str,
    },
    total=False,
)


class StreamingImageEncryptionConfigurationTypeDef(
    _RequiredStreamingImageEncryptionConfigurationTypeDef,
    _OptionalStreamingImageEncryptionConfigurationTypeDef,
):
    pass


StreamingImageTypeDef = TypedDict(
    "StreamingImageTypeDef",
    {
        "arn": str,
        "description": str,
        "ec2ImageId": str,
        "encryptionConfiguration": "StreamingImageEncryptionConfigurationTypeDef",
        "eulaIds": List[str],
        "name": str,
        "owner": str,
        "platform": str,
        "state": StreamingImageStateType,
        "statusCode": StreamingImageStatusCodeType,
        "statusMessage": str,
        "streamingImageId": str,
        "tags": Dict[str, str],
    },
    total=False,
)

StreamingSessionStorageRootTypeDef = TypedDict(
    "StreamingSessionStorageRootTypeDef",
    {
        "linux": str,
        "windows": str,
    },
    total=False,
)

StreamingSessionStreamTypeDef = TypedDict(
    "StreamingSessionStreamTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "expiresAt": datetime,
        "ownedBy": str,
        "state": StreamingSessionStreamStateType,
        "statusCode": StreamingSessionStreamStatusCodeType,
        "streamId": str,
        "url": str,
    },
    total=False,
)

StreamingSessionTypeDef = TypedDict(
    "StreamingSessionTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "createdBy": str,
        "ec2InstanceType": str,
        "launchProfileId": str,
        "ownedBy": str,
        "sessionId": str,
        "startedAt": datetime,
        "startedBy": str,
        "state": StreamingSessionStateType,
        "statusCode": StreamingSessionStatusCodeType,
        "statusMessage": str,
        "stopAt": datetime,
        "stoppedAt": datetime,
        "stoppedBy": str,
        "streamingImageId": str,
        "tags": Dict[str, str],
        "terminateAt": datetime,
        "updatedAt": datetime,
        "updatedBy": str,
    },
    total=False,
)

StudioComponentConfigurationTypeDef = TypedDict(
    "StudioComponentConfigurationTypeDef",
    {
        "activeDirectoryConfiguration": "ActiveDirectoryConfigurationTypeDef",
        "computeFarmConfiguration": "ComputeFarmConfigurationTypeDef",
        "licenseServiceConfiguration": "LicenseServiceConfigurationTypeDef",
        "sharedFileSystemConfiguration": "SharedFileSystemConfigurationTypeDef",
    },
    total=False,
)

StudioComponentInitializationScriptTypeDef = TypedDict(
    "StudioComponentInitializationScriptTypeDef",
    {
        "launchProfileProtocolVersion": str,
        "platform": LaunchProfilePlatformType,
        "runContext": StudioComponentInitializationScriptRunContextType,
        "script": str,
    },
    total=False,
)

StudioComponentSummaryTypeDef = TypedDict(
    "StudioComponentSummaryTypeDef",
    {
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "name": str,
        "studioComponentId": str,
        "subtype": StudioComponentSubtypeType,
        "type": StudioComponentTypeType,
        "updatedAt": datetime,
        "updatedBy": str,
    },
    total=False,
)

StudioComponentTypeDef = TypedDict(
    "StudioComponentTypeDef",
    {
        "arn": str,
        "configuration": "StudioComponentConfigurationTypeDef",
        "createdAt": datetime,
        "createdBy": str,
        "description": str,
        "ec2SecurityGroupIds": List[str],
        "initializationScripts": List["StudioComponentInitializationScriptTypeDef"],
        "name": str,
        "scriptParameters": List["ScriptParameterKeyValueTypeDef"],
        "state": StudioComponentStateType,
        "statusCode": StudioComponentStatusCodeType,
        "statusMessage": str,
        "studioComponentId": str,
        "subtype": StudioComponentSubtypeType,
        "tags": Dict[str, str],
        "type": StudioComponentTypeType,
        "updatedAt": datetime,
        "updatedBy": str,
    },
    total=False,
)

_RequiredStudioEncryptionConfigurationTypeDef = TypedDict(
    "_RequiredStudioEncryptionConfigurationTypeDef",
    {
        "keyType": StudioEncryptionConfigurationKeyTypeType,
    },
)
_OptionalStudioEncryptionConfigurationTypeDef = TypedDict(
    "_OptionalStudioEncryptionConfigurationTypeDef",
    {
        "keyArn": str,
    },
    total=False,
)


class StudioEncryptionConfigurationTypeDef(
    _RequiredStudioEncryptionConfigurationTypeDef, _OptionalStudioEncryptionConfigurationTypeDef
):
    pass


StudioMembershipTypeDef = TypedDict(
    "StudioMembershipTypeDef",
    {
        "identityStoreId": str,
        "persona": Literal["ADMINISTRATOR"],
        "principalId": str,
        "sid": str,
    },
    total=False,
)

StudioTypeDef = TypedDict(
    "StudioTypeDef",
    {
        "adminRoleArn": str,
        "arn": str,
        "createdAt": datetime,
        "displayName": str,
        "homeRegion": str,
        "ssoClientId": str,
        "state": StudioStateType,
        "statusCode": StudioStatusCodeType,
        "statusMessage": str,
        "studioEncryptionConfiguration": "StudioEncryptionConfigurationTypeDef",
        "studioId": str,
        "studioName": str,
        "studioUrl": str,
        "tags": Dict[str, str],
        "updatedAt": datetime,
        "userRoleArn": str,
    },
    total=False,
)

_RequiredTagResourceRequestRequestTypeDef = TypedDict(
    "_RequiredTagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)
_OptionalTagResourceRequestRequestTypeDef = TypedDict(
    "_OptionalTagResourceRequestRequestTypeDef",
    {
        "tags": Mapping[str, str],
    },
    total=False,
)


class TagResourceRequestRequestTypeDef(
    _RequiredTagResourceRequestRequestTypeDef, _OptionalTagResourceRequestRequestTypeDef
):
    pass


UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateLaunchProfileMemberRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateLaunchProfileMemberRequestRequestTypeDef",
    {
        "launchProfileId": str,
        "persona": Literal["USER"],
        "principalId": str,
        "studioId": str,
    },
)
_OptionalUpdateLaunchProfileMemberRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateLaunchProfileMemberRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class UpdateLaunchProfileMemberRequestRequestTypeDef(
    _RequiredUpdateLaunchProfileMemberRequestRequestTypeDef,
    _OptionalUpdateLaunchProfileMemberRequestRequestTypeDef,
):
    pass


UpdateLaunchProfileMemberResponseTypeDef = TypedDict(
    "UpdateLaunchProfileMemberResponseTypeDef",
    {
        "member": "LaunchProfileMembershipTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateLaunchProfileRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateLaunchProfileRequestRequestTypeDef",
    {
        "launchProfileId": str,
        "studioId": str,
    },
)
_OptionalUpdateLaunchProfileRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateLaunchProfileRequestRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
        "launchProfileProtocolVersions": Sequence[str],
        "name": str,
        "streamConfiguration": "StreamConfigurationCreateTypeDef",
        "studioComponentIds": Sequence[str],
    },
    total=False,
)


class UpdateLaunchProfileRequestRequestTypeDef(
    _RequiredUpdateLaunchProfileRequestRequestTypeDef,
    _OptionalUpdateLaunchProfileRequestRequestTypeDef,
):
    pass


UpdateLaunchProfileResponseTypeDef = TypedDict(
    "UpdateLaunchProfileResponseTypeDef",
    {
        "launchProfile": "LaunchProfileTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateStreamingImageRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateStreamingImageRequestRequestTypeDef",
    {
        "streamingImageId": str,
        "studioId": str,
    },
)
_OptionalUpdateStreamingImageRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateStreamingImageRequestRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
        "name": str,
    },
    total=False,
)


class UpdateStreamingImageRequestRequestTypeDef(
    _RequiredUpdateStreamingImageRequestRequestTypeDef,
    _OptionalUpdateStreamingImageRequestRequestTypeDef,
):
    pass


UpdateStreamingImageResponseTypeDef = TypedDict(
    "UpdateStreamingImageResponseTypeDef",
    {
        "streamingImage": "StreamingImageTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateStudioComponentRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateStudioComponentRequestRequestTypeDef",
    {
        "studioComponentId": str,
        "studioId": str,
    },
)
_OptionalUpdateStudioComponentRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateStudioComponentRequestRequestTypeDef",
    {
        "clientToken": str,
        "configuration": "StudioComponentConfigurationTypeDef",
        "description": str,
        "ec2SecurityGroupIds": Sequence[str],
        "initializationScripts": Sequence["StudioComponentInitializationScriptTypeDef"],
        "name": str,
        "scriptParameters": Sequence["ScriptParameterKeyValueTypeDef"],
        "subtype": StudioComponentSubtypeType,
        "type": StudioComponentTypeType,
    },
    total=False,
)


class UpdateStudioComponentRequestRequestTypeDef(
    _RequiredUpdateStudioComponentRequestRequestTypeDef,
    _OptionalUpdateStudioComponentRequestRequestTypeDef,
):
    pass


UpdateStudioComponentResponseTypeDef = TypedDict(
    "UpdateStudioComponentResponseTypeDef",
    {
        "studioComponent": "StudioComponentTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateStudioRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateStudioRequestRequestTypeDef",
    {
        "studioId": str,
    },
)
_OptionalUpdateStudioRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateStudioRequestRequestTypeDef",
    {
        "adminRoleArn": str,
        "clientToken": str,
        "displayName": str,
        "userRoleArn": str,
    },
    total=False,
)


class UpdateStudioRequestRequestTypeDef(
    _RequiredUpdateStudioRequestRequestTypeDef, _OptionalUpdateStudioRequestRequestTypeDef
):
    pass


UpdateStudioResponseTypeDef = TypedDict(
    "UpdateStudioResponseTypeDef",
    {
        "studio": "StudioTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ValidationResultTypeDef = TypedDict(
    "ValidationResultTypeDef",
    {
        "state": LaunchProfileValidationStateType,
        "statusCode": LaunchProfileValidationStatusCodeType,
        "statusMessage": str,
        "type": LaunchProfileValidationTypeType,
    },
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)
