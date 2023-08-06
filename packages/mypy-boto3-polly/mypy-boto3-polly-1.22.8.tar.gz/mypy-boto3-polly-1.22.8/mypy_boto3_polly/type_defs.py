"""
Type annotations for polly service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_polly/type_defs/)

Usage::

    ```python
    from mypy_boto3_polly.type_defs import DeleteLexiconInputRequestTypeDef

    data: DeleteLexiconInputRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from botocore.response import StreamingBody

from .literals import (
    EngineType,
    GenderType,
    LanguageCodeType,
    OutputFormatType,
    SpeechMarkTypeType,
    TaskStatusType,
    TextTypeType,
    VoiceIdType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "DeleteLexiconInputRequestTypeDef",
    "DescribeVoicesInputDescribeVoicesPaginateTypeDef",
    "DescribeVoicesInputRequestTypeDef",
    "DescribeVoicesOutputTypeDef",
    "GetLexiconInputRequestTypeDef",
    "GetLexiconOutputTypeDef",
    "GetSpeechSynthesisTaskInputRequestTypeDef",
    "GetSpeechSynthesisTaskOutputTypeDef",
    "LexiconAttributesTypeDef",
    "LexiconDescriptionTypeDef",
    "LexiconTypeDef",
    "ListLexiconsInputListLexiconsPaginateTypeDef",
    "ListLexiconsInputRequestTypeDef",
    "ListLexiconsOutputTypeDef",
    "ListSpeechSynthesisTasksInputListSpeechSynthesisTasksPaginateTypeDef",
    "ListSpeechSynthesisTasksInputRequestTypeDef",
    "ListSpeechSynthesisTasksOutputTypeDef",
    "PaginatorConfigTypeDef",
    "PutLexiconInputRequestTypeDef",
    "ResponseMetadataTypeDef",
    "StartSpeechSynthesisTaskInputRequestTypeDef",
    "StartSpeechSynthesisTaskOutputTypeDef",
    "SynthesisTaskTypeDef",
    "SynthesizeSpeechInputRequestTypeDef",
    "SynthesizeSpeechOutputTypeDef",
    "VoiceTypeDef",
)

DeleteLexiconInputRequestTypeDef = TypedDict(
    "DeleteLexiconInputRequestTypeDef",
    {
        "Name": str,
    },
)

DescribeVoicesInputDescribeVoicesPaginateTypeDef = TypedDict(
    "DescribeVoicesInputDescribeVoicesPaginateTypeDef",
    {
        "Engine": EngineType,
        "LanguageCode": LanguageCodeType,
        "IncludeAdditionalLanguageCodes": bool,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeVoicesInputRequestTypeDef = TypedDict(
    "DescribeVoicesInputRequestTypeDef",
    {
        "Engine": EngineType,
        "LanguageCode": LanguageCodeType,
        "IncludeAdditionalLanguageCodes": bool,
        "NextToken": str,
    },
    total=False,
)

DescribeVoicesOutputTypeDef = TypedDict(
    "DescribeVoicesOutputTypeDef",
    {
        "Voices": List["VoiceTypeDef"],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetLexiconInputRequestTypeDef = TypedDict(
    "GetLexiconInputRequestTypeDef",
    {
        "Name": str,
    },
)

GetLexiconOutputTypeDef = TypedDict(
    "GetLexiconOutputTypeDef",
    {
        "Lexicon": "LexiconTypeDef",
        "LexiconAttributes": "LexiconAttributesTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetSpeechSynthesisTaskInputRequestTypeDef = TypedDict(
    "GetSpeechSynthesisTaskInputRequestTypeDef",
    {
        "TaskId": str,
    },
)

GetSpeechSynthesisTaskOutputTypeDef = TypedDict(
    "GetSpeechSynthesisTaskOutputTypeDef",
    {
        "SynthesisTask": "SynthesisTaskTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

LexiconAttributesTypeDef = TypedDict(
    "LexiconAttributesTypeDef",
    {
        "Alphabet": str,
        "LanguageCode": LanguageCodeType,
        "LastModified": datetime,
        "LexiconArn": str,
        "LexemesCount": int,
        "Size": int,
    },
    total=False,
)

LexiconDescriptionTypeDef = TypedDict(
    "LexiconDescriptionTypeDef",
    {
        "Name": str,
        "Attributes": "LexiconAttributesTypeDef",
    },
    total=False,
)

LexiconTypeDef = TypedDict(
    "LexiconTypeDef",
    {
        "Content": str,
        "Name": str,
    },
    total=False,
)

ListLexiconsInputListLexiconsPaginateTypeDef = TypedDict(
    "ListLexiconsInputListLexiconsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListLexiconsInputRequestTypeDef = TypedDict(
    "ListLexiconsInputRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)

ListLexiconsOutputTypeDef = TypedDict(
    "ListLexiconsOutputTypeDef",
    {
        "Lexicons": List["LexiconDescriptionTypeDef"],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListSpeechSynthesisTasksInputListSpeechSynthesisTasksPaginateTypeDef = TypedDict(
    "ListSpeechSynthesisTasksInputListSpeechSynthesisTasksPaginateTypeDef",
    {
        "Status": TaskStatusType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListSpeechSynthesisTasksInputRequestTypeDef = TypedDict(
    "ListSpeechSynthesisTasksInputRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "Status": TaskStatusType,
    },
    total=False,
)

ListSpeechSynthesisTasksOutputTypeDef = TypedDict(
    "ListSpeechSynthesisTasksOutputTypeDef",
    {
        "NextToken": str,
        "SynthesisTasks": List["SynthesisTaskTypeDef"],
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

PutLexiconInputRequestTypeDef = TypedDict(
    "PutLexiconInputRequestTypeDef",
    {
        "Name": str,
        "Content": str,
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

_RequiredStartSpeechSynthesisTaskInputRequestTypeDef = TypedDict(
    "_RequiredStartSpeechSynthesisTaskInputRequestTypeDef",
    {
        "OutputFormat": OutputFormatType,
        "OutputS3BucketName": str,
        "Text": str,
        "VoiceId": VoiceIdType,
    },
)
_OptionalStartSpeechSynthesisTaskInputRequestTypeDef = TypedDict(
    "_OptionalStartSpeechSynthesisTaskInputRequestTypeDef",
    {
        "Engine": EngineType,
        "LanguageCode": LanguageCodeType,
        "LexiconNames": Sequence[str],
        "OutputS3KeyPrefix": str,
        "SampleRate": str,
        "SnsTopicArn": str,
        "SpeechMarkTypes": Sequence[SpeechMarkTypeType],
        "TextType": TextTypeType,
    },
    total=False,
)


class StartSpeechSynthesisTaskInputRequestTypeDef(
    _RequiredStartSpeechSynthesisTaskInputRequestTypeDef,
    _OptionalStartSpeechSynthesisTaskInputRequestTypeDef,
):
    pass


StartSpeechSynthesisTaskOutputTypeDef = TypedDict(
    "StartSpeechSynthesisTaskOutputTypeDef",
    {
        "SynthesisTask": "SynthesisTaskTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

SynthesisTaskTypeDef = TypedDict(
    "SynthesisTaskTypeDef",
    {
        "Engine": EngineType,
        "TaskId": str,
        "TaskStatus": TaskStatusType,
        "TaskStatusReason": str,
        "OutputUri": str,
        "CreationTime": datetime,
        "RequestCharacters": int,
        "SnsTopicArn": str,
        "LexiconNames": List[str],
        "OutputFormat": OutputFormatType,
        "SampleRate": str,
        "SpeechMarkTypes": List[SpeechMarkTypeType],
        "TextType": TextTypeType,
        "VoiceId": VoiceIdType,
        "LanguageCode": LanguageCodeType,
    },
    total=False,
)

_RequiredSynthesizeSpeechInputRequestTypeDef = TypedDict(
    "_RequiredSynthesizeSpeechInputRequestTypeDef",
    {
        "OutputFormat": OutputFormatType,
        "Text": str,
        "VoiceId": VoiceIdType,
    },
)
_OptionalSynthesizeSpeechInputRequestTypeDef = TypedDict(
    "_OptionalSynthesizeSpeechInputRequestTypeDef",
    {
        "Engine": EngineType,
        "LanguageCode": LanguageCodeType,
        "LexiconNames": Sequence[str],
        "SampleRate": str,
        "SpeechMarkTypes": Sequence[SpeechMarkTypeType],
        "TextType": TextTypeType,
    },
    total=False,
)


class SynthesizeSpeechInputRequestTypeDef(
    _RequiredSynthesizeSpeechInputRequestTypeDef, _OptionalSynthesizeSpeechInputRequestTypeDef
):
    pass


SynthesizeSpeechOutputTypeDef = TypedDict(
    "SynthesizeSpeechOutputTypeDef",
    {
        "AudioStream": StreamingBody,
        "ContentType": str,
        "RequestCharacters": int,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

VoiceTypeDef = TypedDict(
    "VoiceTypeDef",
    {
        "Gender": GenderType,
        "Id": VoiceIdType,
        "LanguageCode": LanguageCodeType,
        "LanguageName": str,
        "Name": str,
        "AdditionalLanguageCodes": List[LanguageCodeType],
        "SupportedEngines": List[EngineType],
    },
    total=False,
)
