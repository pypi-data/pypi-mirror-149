"""
Type annotations for textract service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_textract/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_textract.client import TextractClient

    session = get_session()
    async with session.create_client("textract") as client:
        client: TextractClient
    ```
"""
from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import FeatureTypeType
from .type_defs import (
    AnalyzeDocumentResponseTypeDef,
    AnalyzeExpenseResponseTypeDef,
    AnalyzeIDResponseTypeDef,
    DetectDocumentTextResponseTypeDef,
    DocumentLocationTypeDef,
    DocumentTypeDef,
    GetDocumentAnalysisResponseTypeDef,
    GetDocumentTextDetectionResponseTypeDef,
    GetExpenseAnalysisResponseTypeDef,
    HumanLoopConfigTypeDef,
    NotificationChannelTypeDef,
    OutputConfigTypeDef,
    StartDocumentAnalysisResponseTypeDef,
    StartDocumentTextDetectionResponseTypeDef,
    StartExpenseAnalysisResponseTypeDef,
)

__all__ = ("TextractClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    BadDocumentException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DocumentTooLargeException: Type[BotocoreClientError]
    HumanLoopQuotaExceededException: Type[BotocoreClientError]
    IdempotentParameterMismatchException: Type[BotocoreClientError]
    InternalServerError: Type[BotocoreClientError]
    InvalidJobIdException: Type[BotocoreClientError]
    InvalidKMSKeyException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidS3ObjectException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ProvisionedThroughputExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    UnsupportedDocumentException: Type[BotocoreClientError]


class TextractClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_textract/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        TextractClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_textract/client/#exceptions)
        """

    async def analyze_document(
        self,
        *,
        Document: "DocumentTypeDef",
        FeatureTypes: Sequence[FeatureTypeType],
        HumanLoopConfig: "HumanLoopConfigTypeDef" = ...
    ) -> AnalyzeDocumentResponseTypeDef:
        """
        Analyzes an input document for relationships between detected items.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.analyze_document)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_textract/client/#analyze_document)
        """

    async def analyze_expense(
        self, *, Document: "DocumentTypeDef"
    ) -> AnalyzeExpenseResponseTypeDef:
        """
        `AnalyzeExpense` synchronously analyzes an input document for financially
        related relationships between text.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.analyze_expense)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_textract/client/#analyze_expense)
        """

    async def analyze_id(
        self, *, DocumentPages: Sequence["DocumentTypeDef"]
    ) -> AnalyzeIDResponseTypeDef:
        """
        Analyzes identity documents for relevant information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.analyze_id)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_textract/client/#analyze_id)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_textract/client/#can_paginate)
        """

    async def detect_document_text(
        self, *, Document: "DocumentTypeDef"
    ) -> DetectDocumentTextResponseTypeDef:
        """
        Detects text in the input document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.detect_document_text)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_textract/client/#detect_document_text)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_textract/client/#generate_presigned_url)
        """

    async def get_document_analysis(
        self, *, JobId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> GetDocumentAnalysisResponseTypeDef:
        """
        Gets the results for an Amazon Textract asynchronous operation that analyzes
        text in a document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.get_document_analysis)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_textract/client/#get_document_analysis)
        """

    async def get_document_text_detection(
        self, *, JobId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> GetDocumentTextDetectionResponseTypeDef:
        """
        Gets the results for an Amazon Textract asynchronous operation that detects text
        in a document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.get_document_text_detection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_textract/client/#get_document_text_detection)
        """

    async def get_expense_analysis(
        self, *, JobId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> GetExpenseAnalysisResponseTypeDef:
        """
        Gets the results for an Amazon Textract asynchronous operation that analyzes
        invoices and receipts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.get_expense_analysis)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_textract/client/#get_expense_analysis)
        """

    async def start_document_analysis(
        self,
        *,
        DocumentLocation: "DocumentLocationTypeDef",
        FeatureTypes: Sequence[FeatureTypeType],
        ClientRequestToken: str = ...,
        JobTag: str = ...,
        NotificationChannel: "NotificationChannelTypeDef" = ...,
        OutputConfig: "OutputConfigTypeDef" = ...,
        KMSKeyId: str = ...
    ) -> StartDocumentAnalysisResponseTypeDef:
        """
        Starts the asynchronous analysis of an input document for relationships between
        detected items such as key-value pairs, tables, and selection elements.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.start_document_analysis)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_textract/client/#start_document_analysis)
        """

    async def start_document_text_detection(
        self,
        *,
        DocumentLocation: "DocumentLocationTypeDef",
        ClientRequestToken: str = ...,
        JobTag: str = ...,
        NotificationChannel: "NotificationChannelTypeDef" = ...,
        OutputConfig: "OutputConfigTypeDef" = ...,
        KMSKeyId: str = ...
    ) -> StartDocumentTextDetectionResponseTypeDef:
        """
        Starts the asynchronous detection of text in a document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.start_document_text_detection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_textract/client/#start_document_text_detection)
        """

    async def start_expense_analysis(
        self,
        *,
        DocumentLocation: "DocumentLocationTypeDef",
        ClientRequestToken: str = ...,
        JobTag: str = ...,
        NotificationChannel: "NotificationChannelTypeDef" = ...,
        OutputConfig: "OutputConfigTypeDef" = ...,
        KMSKeyId: str = ...
    ) -> StartExpenseAnalysisResponseTypeDef:
        """
        Starts the asynchronous analysis of invoices or receipts for data like contact
        information, items purchased, and vendor names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.start_expense_analysis)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_textract/client/#start_expense_analysis)
        """

    async def __aenter__(self) -> "TextractClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_textract/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_textract/client/)
        """
