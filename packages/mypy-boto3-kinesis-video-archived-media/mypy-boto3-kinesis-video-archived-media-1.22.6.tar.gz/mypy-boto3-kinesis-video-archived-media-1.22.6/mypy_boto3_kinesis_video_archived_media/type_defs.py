"""
Type annotations for kinesis-video-archived-media service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_kinesis_video_archived_media/type_defs/)

Usage::

    ```python
    from mypy_boto3_kinesis_video_archived_media.type_defs import ClipFragmentSelectorTypeDef

    data: ClipFragmentSelectorTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    ClipFragmentSelectorTypeType,
    ContainerFormatType,
    DASHDisplayFragmentNumberType,
    DASHDisplayFragmentTimestampType,
    DASHFragmentSelectorTypeType,
    DASHPlaybackModeType,
    FormatType,
    FragmentSelectorTypeType,
    HLSDiscontinuityModeType,
    HLSDisplayFragmentTimestampType,
    HLSFragmentSelectorTypeType,
    HLSPlaybackModeType,
    ImageErrorType,
    ImageSelectorTypeType,
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
    "ClipFragmentSelectorTypeDef",
    "ClipTimestampRangeTypeDef",
    "DASHFragmentSelectorTypeDef",
    "DASHTimestampRangeTypeDef",
    "FragmentSelectorTypeDef",
    "FragmentTypeDef",
    "GetClipInputRequestTypeDef",
    "GetClipOutputTypeDef",
    "GetDASHStreamingSessionURLInputRequestTypeDef",
    "GetDASHStreamingSessionURLOutputTypeDef",
    "GetHLSStreamingSessionURLInputRequestTypeDef",
    "GetHLSStreamingSessionURLOutputTypeDef",
    "GetImagesInputGetImagesPaginateTypeDef",
    "GetImagesInputRequestTypeDef",
    "GetImagesOutputTypeDef",
    "GetMediaForFragmentListInputRequestTypeDef",
    "GetMediaForFragmentListOutputTypeDef",
    "HLSFragmentSelectorTypeDef",
    "HLSTimestampRangeTypeDef",
    "ImageTypeDef",
    "ListFragmentsInputListFragmentsPaginateTypeDef",
    "ListFragmentsInputRequestTypeDef",
    "ListFragmentsOutputTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "TimestampRangeTypeDef",
)

ClipFragmentSelectorTypeDef = TypedDict(
    "ClipFragmentSelectorTypeDef",
    {
        "FragmentSelectorType": ClipFragmentSelectorTypeType,
        "TimestampRange": "ClipTimestampRangeTypeDef",
    },
)

ClipTimestampRangeTypeDef = TypedDict(
    "ClipTimestampRangeTypeDef",
    {
        "StartTimestamp": Union[datetime, str],
        "EndTimestamp": Union[datetime, str],
    },
)

DASHFragmentSelectorTypeDef = TypedDict(
    "DASHFragmentSelectorTypeDef",
    {
        "FragmentSelectorType": DASHFragmentSelectorTypeType,
        "TimestampRange": "DASHTimestampRangeTypeDef",
    },
    total=False,
)

DASHTimestampRangeTypeDef = TypedDict(
    "DASHTimestampRangeTypeDef",
    {
        "StartTimestamp": Union[datetime, str],
        "EndTimestamp": Union[datetime, str],
    },
    total=False,
)

FragmentSelectorTypeDef = TypedDict(
    "FragmentSelectorTypeDef",
    {
        "FragmentSelectorType": FragmentSelectorTypeType,
        "TimestampRange": "TimestampRangeTypeDef",
    },
)

FragmentTypeDef = TypedDict(
    "FragmentTypeDef",
    {
        "FragmentNumber": str,
        "FragmentSizeInBytes": int,
        "ProducerTimestamp": datetime,
        "ServerTimestamp": datetime,
        "FragmentLengthInMilliseconds": int,
    },
    total=False,
)

_RequiredGetClipInputRequestTypeDef = TypedDict(
    "_RequiredGetClipInputRequestTypeDef",
    {
        "ClipFragmentSelector": "ClipFragmentSelectorTypeDef",
    },
)
_OptionalGetClipInputRequestTypeDef = TypedDict(
    "_OptionalGetClipInputRequestTypeDef",
    {
        "StreamName": str,
        "StreamARN": str,
    },
    total=False,
)


class GetClipInputRequestTypeDef(
    _RequiredGetClipInputRequestTypeDef, _OptionalGetClipInputRequestTypeDef
):
    pass


GetClipOutputTypeDef = TypedDict(
    "GetClipOutputTypeDef",
    {
        "ContentType": str,
        "Payload": StreamingBody,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetDASHStreamingSessionURLInputRequestTypeDef = TypedDict(
    "GetDASHStreamingSessionURLInputRequestTypeDef",
    {
        "StreamName": str,
        "StreamARN": str,
        "PlaybackMode": DASHPlaybackModeType,
        "DisplayFragmentTimestamp": DASHDisplayFragmentTimestampType,
        "DisplayFragmentNumber": DASHDisplayFragmentNumberType,
        "DASHFragmentSelector": "DASHFragmentSelectorTypeDef",
        "Expires": int,
        "MaxManifestFragmentResults": int,
    },
    total=False,
)

GetDASHStreamingSessionURLOutputTypeDef = TypedDict(
    "GetDASHStreamingSessionURLOutputTypeDef",
    {
        "DASHStreamingSessionURL": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetHLSStreamingSessionURLInputRequestTypeDef = TypedDict(
    "GetHLSStreamingSessionURLInputRequestTypeDef",
    {
        "StreamName": str,
        "StreamARN": str,
        "PlaybackMode": HLSPlaybackModeType,
        "HLSFragmentSelector": "HLSFragmentSelectorTypeDef",
        "ContainerFormat": ContainerFormatType,
        "DiscontinuityMode": HLSDiscontinuityModeType,
        "DisplayFragmentTimestamp": HLSDisplayFragmentTimestampType,
        "Expires": int,
        "MaxMediaPlaylistFragmentResults": int,
    },
    total=False,
)

GetHLSStreamingSessionURLOutputTypeDef = TypedDict(
    "GetHLSStreamingSessionURLOutputTypeDef",
    {
        "HLSStreamingSessionURL": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGetImagesInputGetImagesPaginateTypeDef = TypedDict(
    "_RequiredGetImagesInputGetImagesPaginateTypeDef",
    {
        "ImageSelectorType": ImageSelectorTypeType,
        "StartTimestamp": Union[datetime, str],
        "EndTimestamp": Union[datetime, str],
        "SamplingInterval": int,
        "Format": FormatType,
    },
)
_OptionalGetImagesInputGetImagesPaginateTypeDef = TypedDict(
    "_OptionalGetImagesInputGetImagesPaginateTypeDef",
    {
        "StreamName": str,
        "StreamARN": str,
        "FormatConfig": Mapping[Literal["JPEGQuality"], str],
        "WidthPixels": int,
        "HeightPixels": int,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class GetImagesInputGetImagesPaginateTypeDef(
    _RequiredGetImagesInputGetImagesPaginateTypeDef, _OptionalGetImagesInputGetImagesPaginateTypeDef
):
    pass


_RequiredGetImagesInputRequestTypeDef = TypedDict(
    "_RequiredGetImagesInputRequestTypeDef",
    {
        "ImageSelectorType": ImageSelectorTypeType,
        "StartTimestamp": Union[datetime, str],
        "EndTimestamp": Union[datetime, str],
        "SamplingInterval": int,
        "Format": FormatType,
    },
)
_OptionalGetImagesInputRequestTypeDef = TypedDict(
    "_OptionalGetImagesInputRequestTypeDef",
    {
        "StreamName": str,
        "StreamARN": str,
        "FormatConfig": Mapping[Literal["JPEGQuality"], str],
        "WidthPixels": int,
        "HeightPixels": int,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class GetImagesInputRequestTypeDef(
    _RequiredGetImagesInputRequestTypeDef, _OptionalGetImagesInputRequestTypeDef
):
    pass


GetImagesOutputTypeDef = TypedDict(
    "GetImagesOutputTypeDef",
    {
        "Images": List["ImageTypeDef"],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredGetMediaForFragmentListInputRequestTypeDef = TypedDict(
    "_RequiredGetMediaForFragmentListInputRequestTypeDef",
    {
        "Fragments": Sequence[str],
    },
)
_OptionalGetMediaForFragmentListInputRequestTypeDef = TypedDict(
    "_OptionalGetMediaForFragmentListInputRequestTypeDef",
    {
        "StreamName": str,
        "StreamARN": str,
    },
    total=False,
)


class GetMediaForFragmentListInputRequestTypeDef(
    _RequiredGetMediaForFragmentListInputRequestTypeDef,
    _OptionalGetMediaForFragmentListInputRequestTypeDef,
):
    pass


GetMediaForFragmentListOutputTypeDef = TypedDict(
    "GetMediaForFragmentListOutputTypeDef",
    {
        "ContentType": str,
        "Payload": StreamingBody,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

HLSFragmentSelectorTypeDef = TypedDict(
    "HLSFragmentSelectorTypeDef",
    {
        "FragmentSelectorType": HLSFragmentSelectorTypeType,
        "TimestampRange": "HLSTimestampRangeTypeDef",
    },
    total=False,
)

HLSTimestampRangeTypeDef = TypedDict(
    "HLSTimestampRangeTypeDef",
    {
        "StartTimestamp": Union[datetime, str],
        "EndTimestamp": Union[datetime, str],
    },
    total=False,
)

ImageTypeDef = TypedDict(
    "ImageTypeDef",
    {
        "TimeStamp": datetime,
        "Error": ImageErrorType,
        "ImageContent": str,
    },
    total=False,
)

ListFragmentsInputListFragmentsPaginateTypeDef = TypedDict(
    "ListFragmentsInputListFragmentsPaginateTypeDef",
    {
        "StreamName": str,
        "StreamARN": str,
        "FragmentSelector": "FragmentSelectorTypeDef",
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListFragmentsInputRequestTypeDef = TypedDict(
    "ListFragmentsInputRequestTypeDef",
    {
        "StreamName": str,
        "StreamARN": str,
        "MaxResults": int,
        "NextToken": str,
        "FragmentSelector": "FragmentSelectorTypeDef",
    },
    total=False,
)

ListFragmentsOutputTypeDef = TypedDict(
    "ListFragmentsOutputTypeDef",
    {
        "Fragments": List["FragmentTypeDef"],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
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

TimestampRangeTypeDef = TypedDict(
    "TimestampRangeTypeDef",
    {
        "StartTimestamp": Union[datetime, str],
        "EndTimestamp": Union[datetime, str],
    },
)
