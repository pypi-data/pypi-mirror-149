"""
Type annotations for translate service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_translate/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_translate.client import TranslateClient

    session = get_session()
    async with session.create_client("translate") as client:
        client: TranslateClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import TerminologyDataFormatType
from .paginator import ListTerminologiesPaginator
from .type_defs import (
    CreateParallelDataResponseTypeDef,
    DeleteParallelDataResponseTypeDef,
    DescribeTextTranslationJobResponseTypeDef,
    EncryptionKeyTypeDef,
    GetParallelDataResponseTypeDef,
    GetTerminologyResponseTypeDef,
    ImportTerminologyResponseTypeDef,
    InputDataConfigTypeDef,
    ListParallelDataResponseTypeDef,
    ListTerminologiesResponseTypeDef,
    ListTextTranslationJobsResponseTypeDef,
    OutputDataConfigTypeDef,
    ParallelDataConfigTypeDef,
    StartTextTranslationJobResponseTypeDef,
    StopTextTranslationJobResponseTypeDef,
    TerminologyDataTypeDef,
    TextTranslationJobFilterTypeDef,
    TranslateTextResponseTypeDef,
    TranslationSettingsTypeDef,
    UpdateParallelDataResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("TranslateClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    DetectedLanguageLowConfidenceException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidFilterException: Type[BotocoreClientError]
    InvalidParameterValueException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    TextSizeLimitExceededException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    UnsupportedLanguagePairException: Type[BotocoreClientError]


class TranslateClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate.html#Translate.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_translate/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        TranslateClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate.html#Translate.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_translate/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate.html#Translate.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_translate/client/#can_paginate)
        """

    async def create_parallel_data(
        self,
        *,
        Name: str,
        ParallelDataConfig: "ParallelDataConfigTypeDef",
        ClientToken: str,
        Description: str = ...,
        EncryptionKey: "EncryptionKeyTypeDef" = ...
    ) -> CreateParallelDataResponseTypeDef:
        """
        Creates a parallel data resource in Amazon Translate by importing an input file
        from Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate.html#Translate.Client.create_parallel_data)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_translate/client/#create_parallel_data)
        """

    async def delete_parallel_data(self, *, Name: str) -> DeleteParallelDataResponseTypeDef:
        """
        Deletes a parallel data resource in Amazon Translate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate.html#Translate.Client.delete_parallel_data)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_translate/client/#delete_parallel_data)
        """

    async def delete_terminology(self, *, Name: str) -> None:
        """
        A synchronous action that deletes a custom terminology.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate.html#Translate.Client.delete_terminology)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_translate/client/#delete_terminology)
        """

    async def describe_text_translation_job(
        self, *, JobId: str
    ) -> DescribeTextTranslationJobResponseTypeDef:
        """
        Gets the properties associated with an asynchronous batch translation job
        including name, ID, status, source and target languages, input/output S3
        buckets, and so on.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate.html#Translate.Client.describe_text_translation_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_translate/client/#describe_text_translation_job)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate.html#Translate.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_translate/client/#generate_presigned_url)
        """

    async def get_parallel_data(self, *, Name: str) -> GetParallelDataResponseTypeDef:
        """
        Provides information about a parallel data resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate.html#Translate.Client.get_parallel_data)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_translate/client/#get_parallel_data)
        """

    async def get_terminology(
        self, *, Name: str, TerminologyDataFormat: TerminologyDataFormatType = ...
    ) -> GetTerminologyResponseTypeDef:
        """
        Retrieves a custom terminology.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate.html#Translate.Client.get_terminology)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_translate/client/#get_terminology)
        """

    async def import_terminology(
        self,
        *,
        Name: str,
        MergeStrategy: Literal["OVERWRITE"],
        TerminologyData: "TerminologyDataTypeDef",
        Description: str = ...,
        EncryptionKey: "EncryptionKeyTypeDef" = ...
    ) -> ImportTerminologyResponseTypeDef:
        """
        Creates or updates a custom terminology, depending on whether or not one already
        exists for the given terminology name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate.html#Translate.Client.import_terminology)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_translate/client/#import_terminology)
        """

    async def list_parallel_data(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListParallelDataResponseTypeDef:
        """
        Provides a list of your parallel data resources in Amazon Translate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate.html#Translate.Client.list_parallel_data)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_translate/client/#list_parallel_data)
        """

    async def list_terminologies(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListTerminologiesResponseTypeDef:
        """
        Provides a list of custom terminologies associated with your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate.html#Translate.Client.list_terminologies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_translate/client/#list_terminologies)
        """

    async def list_text_translation_jobs(
        self,
        *,
        Filter: "TextTranslationJobFilterTypeDef" = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListTextTranslationJobsResponseTypeDef:
        """
        Gets a list of the batch translation jobs that you have submitted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate.html#Translate.Client.list_text_translation_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_translate/client/#list_text_translation_jobs)
        """

    async def start_text_translation_job(
        self,
        *,
        InputDataConfig: "InputDataConfigTypeDef",
        OutputDataConfig: "OutputDataConfigTypeDef",
        DataAccessRoleArn: str,
        SourceLanguageCode: str,
        TargetLanguageCodes: Sequence[str],
        ClientToken: str,
        JobName: str = ...,
        TerminologyNames: Sequence[str] = ...,
        ParallelDataNames: Sequence[str] = ...,
        Settings: "TranslationSettingsTypeDef" = ...
    ) -> StartTextTranslationJobResponseTypeDef:
        """
        Starts an asynchronous batch translation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate.html#Translate.Client.start_text_translation_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_translate/client/#start_text_translation_job)
        """

    async def stop_text_translation_job(
        self, *, JobId: str
    ) -> StopTextTranslationJobResponseTypeDef:
        """
        Stops an asynchronous batch translation job that is in progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate.html#Translate.Client.stop_text_translation_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_translate/client/#stop_text_translation_job)
        """

    async def translate_text(
        self,
        *,
        Text: str,
        SourceLanguageCode: str,
        TargetLanguageCode: str,
        TerminologyNames: Sequence[str] = ...,
        Settings: "TranslationSettingsTypeDef" = ...
    ) -> TranslateTextResponseTypeDef:
        """
        Translates input text from the source language to the target language.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate.html#Translate.Client.translate_text)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_translate/client/#translate_text)
        """

    async def update_parallel_data(
        self,
        *,
        Name: str,
        ParallelDataConfig: "ParallelDataConfigTypeDef",
        ClientToken: str,
        Description: str = ...
    ) -> UpdateParallelDataResponseTypeDef:
        """
        Updates a previously created parallel data resource by importing a new input
        file from Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate.html#Translate.Client.update_parallel_data)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_translate/client/#update_parallel_data)
        """

    def get_paginator(
        self, operation_name: Literal["list_terminologies"]
    ) -> ListTerminologiesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate.html#Translate.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_translate/client/#get_paginator)
        """

    async def __aenter__(self) -> "TranslateClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate.html#Translate.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_translate/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate.html#Translate.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_translate/client/)
        """
