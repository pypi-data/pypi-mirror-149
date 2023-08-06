"""
Type annotations for wisdom service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_wisdom.client import ConnectWisdomServiceClient

    session = get_session()
    async with session.create_client("wisdom") as client:
        client: ConnectWisdomServiceClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import KnowledgeBaseTypeType
from .paginator import (
    ListAssistantAssociationsPaginator,
    ListAssistantsPaginator,
    ListContentsPaginator,
    ListKnowledgeBasesPaginator,
    QueryAssistantPaginator,
    SearchContentPaginator,
    SearchSessionsPaginator,
)
from .type_defs import (
    AssistantAssociationInputDataTypeDef,
    CreateAssistantAssociationResponseTypeDef,
    CreateAssistantResponseTypeDef,
    CreateContentResponseTypeDef,
    CreateKnowledgeBaseResponseTypeDef,
    CreateSessionResponseTypeDef,
    GetAssistantAssociationResponseTypeDef,
    GetAssistantResponseTypeDef,
    GetContentResponseTypeDef,
    GetContentSummaryResponseTypeDef,
    GetKnowledgeBaseResponseTypeDef,
    GetRecommendationsResponseTypeDef,
    GetSessionResponseTypeDef,
    ListAssistantAssociationsResponseTypeDef,
    ListAssistantsResponseTypeDef,
    ListContentsResponseTypeDef,
    ListKnowledgeBasesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    NotifyRecommendationsReceivedResponseTypeDef,
    QueryAssistantResponseTypeDef,
    RenderingConfigurationTypeDef,
    SearchContentResponseTypeDef,
    SearchExpressionTypeDef,
    SearchSessionsResponseTypeDef,
    ServerSideEncryptionConfigurationTypeDef,
    SourceConfigurationTypeDef,
    StartContentUploadResponseTypeDef,
    UpdateContentResponseTypeDef,
    UpdateKnowledgeBaseTemplateUriResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ConnectWisdomServiceClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    PreconditionFailedException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class ConnectWisdomServiceClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ConnectWisdomServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#can_paginate)
        """

    async def create_assistant(
        self,
        *,
        name: str,
        type: Literal["AGENT"],
        clientToken: str = ...,
        description: str = ...,
        serverSideEncryptionConfiguration: "ServerSideEncryptionConfigurationTypeDef" = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateAssistantResponseTypeDef:
        """
        Creates an Amazon Connect Wisdom assistant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.create_assistant)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#create_assistant)
        """

    async def create_assistant_association(
        self,
        *,
        assistantId: str,
        association: "AssistantAssociationInputDataTypeDef",
        associationType: Literal["KNOWLEDGE_BASE"],
        clientToken: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateAssistantAssociationResponseTypeDef:
        """
        Creates an association between an Amazon Connect Wisdom assistant and another
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.create_assistant_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#create_assistant_association)
        """

    async def create_content(
        self,
        *,
        knowledgeBaseId: str,
        name: str,
        uploadId: str,
        clientToken: str = ...,
        metadata: Mapping[str, str] = ...,
        overrideLinkOutUri: str = ...,
        tags: Mapping[str, str] = ...,
        title: str = ...
    ) -> CreateContentResponseTypeDef:
        """
        Creates Wisdom content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.create_content)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#create_content)
        """

    async def create_knowledge_base(
        self,
        *,
        knowledgeBaseType: KnowledgeBaseTypeType,
        name: str,
        clientToken: str = ...,
        description: str = ...,
        renderingConfiguration: "RenderingConfigurationTypeDef" = ...,
        serverSideEncryptionConfiguration: "ServerSideEncryptionConfigurationTypeDef" = ...,
        sourceConfiguration: "SourceConfigurationTypeDef" = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateKnowledgeBaseResponseTypeDef:
        """
        Creates a knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.create_knowledge_base)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#create_knowledge_base)
        """

    async def create_session(
        self,
        *,
        assistantId: str,
        name: str,
        clientToken: str = ...,
        description: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateSessionResponseTypeDef:
        """
        Creates a session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.create_session)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#create_session)
        """

    async def delete_assistant(self, *, assistantId: str) -> Dict[str, Any]:
        """
        Deletes an assistant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.delete_assistant)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#delete_assistant)
        """

    async def delete_assistant_association(
        self, *, assistantAssociationId: str, assistantId: str
    ) -> Dict[str, Any]:
        """
        Deletes an assistant association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.delete_assistant_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#delete_assistant_association)
        """

    async def delete_content(self, *, contentId: str, knowledgeBaseId: str) -> Dict[str, Any]:
        """
        Deletes the content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.delete_content)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#delete_content)
        """

    async def delete_knowledge_base(self, *, knowledgeBaseId: str) -> Dict[str, Any]:
        """
        Deletes the knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.delete_knowledge_base)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#delete_knowledge_base)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#generate_presigned_url)
        """

    async def get_assistant(self, *, assistantId: str) -> GetAssistantResponseTypeDef:
        """
        Retrieves information about an assistant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.get_assistant)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#get_assistant)
        """

    async def get_assistant_association(
        self, *, assistantAssociationId: str, assistantId: str
    ) -> GetAssistantAssociationResponseTypeDef:
        """
        Retrieves information about an assistant association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.get_assistant_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#get_assistant_association)
        """

    async def get_content(
        self, *, contentId: str, knowledgeBaseId: str
    ) -> GetContentResponseTypeDef:
        """
        Retrieves content, including a pre-signed URL to download the content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.get_content)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#get_content)
        """

    async def get_content_summary(
        self, *, contentId: str, knowledgeBaseId: str
    ) -> GetContentSummaryResponseTypeDef:
        """
        Retrieves summary information about the content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.get_content_summary)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#get_content_summary)
        """

    async def get_knowledge_base(self, *, knowledgeBaseId: str) -> GetKnowledgeBaseResponseTypeDef:
        """
        Retrieves information about the knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.get_knowledge_base)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#get_knowledge_base)
        """

    async def get_recommendations(
        self, *, assistantId: str, sessionId: str, maxResults: int = ..., waitTimeSeconds: int = ...
    ) -> GetRecommendationsResponseTypeDef:
        """
        Retrieves recommendations for the specified session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.get_recommendations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#get_recommendations)
        """

    async def get_session(self, *, assistantId: str, sessionId: str) -> GetSessionResponseTypeDef:
        """
        Retrieves information for a specified session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.get_session)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#get_session)
        """

    async def list_assistant_associations(
        self, *, assistantId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListAssistantAssociationsResponseTypeDef:
        """
        Lists information about assistant associations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.list_assistant_associations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#list_assistant_associations)
        """

    async def list_assistants(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListAssistantsResponseTypeDef:
        """
        Lists information about assistants.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.list_assistants)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#list_assistants)
        """

    async def list_contents(
        self, *, knowledgeBaseId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListContentsResponseTypeDef:
        """
        Lists the content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.list_contents)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#list_contents)
        """

    async def list_knowledge_bases(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListKnowledgeBasesResponseTypeDef:
        """
        Lists the knowledge bases.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.list_knowledge_bases)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#list_knowledge_bases)
        """

    async def list_tags_for_resource(
        self, *, resourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#list_tags_for_resource)
        """

    async def notify_recommendations_received(
        self, *, assistantId: str, recommendationIds: Sequence[str], sessionId: str
    ) -> NotifyRecommendationsReceivedResponseTypeDef:
        """
        Removes the specified recommendations from the specified assistant's queue of
        newly available recommendations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.notify_recommendations_received)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#notify_recommendations_received)
        """

    async def query_assistant(
        self, *, assistantId: str, queryText: str, maxResults: int = ..., nextToken: str = ...
    ) -> QueryAssistantResponseTypeDef:
        """
        Performs a manual search against the specified assistant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.query_assistant)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#query_assistant)
        """

    async def remove_knowledge_base_template_uri(self, *, knowledgeBaseId: str) -> Dict[str, Any]:
        """
        Removes a URI template from a knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.remove_knowledge_base_template_uri)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#remove_knowledge_base_template_uri)
        """

    async def search_content(
        self,
        *,
        knowledgeBaseId: str,
        searchExpression: "SearchExpressionTypeDef",
        maxResults: int = ...,
        nextToken: str = ...
    ) -> SearchContentResponseTypeDef:
        """
        Searches for content in a specified knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.search_content)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#search_content)
        """

    async def search_sessions(
        self,
        *,
        assistantId: str,
        searchExpression: "SearchExpressionTypeDef",
        maxResults: int = ...,
        nextToken: str = ...
    ) -> SearchSessionsResponseTypeDef:
        """
        Searches for sessions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.search_sessions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#search_sessions)
        """

    async def start_content_upload(
        self, *, contentType: str, knowledgeBaseId: str
    ) -> StartContentUploadResponseTypeDef:
        """
        Get a URL to upload content to a knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.start_content_upload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#start_content_upload)
        """

    async def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds the specified tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#tag_resource)
        """

    async def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes the specified tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#untag_resource)
        """

    async def update_content(
        self,
        *,
        contentId: str,
        knowledgeBaseId: str,
        metadata: Mapping[str, str] = ...,
        overrideLinkOutUri: str = ...,
        removeOverrideLinkOutUri: bool = ...,
        revisionId: str = ...,
        title: str = ...,
        uploadId: str = ...
    ) -> UpdateContentResponseTypeDef:
        """
        Updates information about the content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.update_content)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#update_content)
        """

    async def update_knowledge_base_template_uri(
        self, *, knowledgeBaseId: str, templateUri: str
    ) -> UpdateKnowledgeBaseTemplateUriResponseTypeDef:
        """
        Updates the template URI of a knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.update_knowledge_base_template_uri)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#update_knowledge_base_template_uri)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_assistant_associations"]
    ) -> ListAssistantAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_assistants"]) -> ListAssistantsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_contents"]) -> ListContentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_knowledge_bases"]
    ) -> ListKnowledgeBasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["query_assistant"]) -> QueryAssistantPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["search_content"]) -> SearchContentPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["search_sessions"]) -> SearchSessionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/#get_paginator)
        """

    async def __aenter__(self) -> "ConnectWisdomServiceClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom.html#ConnectWisdomService.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/client/)
        """
