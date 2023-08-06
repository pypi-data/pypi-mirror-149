"""
Type annotations for kendra service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kendra.client import kendraClient

    session = get_session()
    async with session.create_client("kendra") as client:
        client: kendraClient
    ```
"""
from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    DataSourceSyncJobStatusType,
    DataSourceTypeType,
    FaqFileFormatType,
    IndexEditionType,
    IntervalType,
    MetricTypeType,
    ModeType,
    QueryResultTypeType,
    UserContextPolicyType,
)
from .type_defs import (
    AssociateEntitiesToExperienceResponseTypeDef,
    AssociatePersonasToEntitiesResponseTypeDef,
    AttributeFilterTypeDef,
    BatchDeleteDocumentResponseTypeDef,
    BatchGetDocumentStatusResponseTypeDef,
    BatchPutDocumentResponseTypeDef,
    CapacityUnitsConfigurationTypeDef,
    ClickFeedbackTypeDef,
    CreateDataSourceResponseTypeDef,
    CreateExperienceResponseTypeDef,
    CreateFaqResponseTypeDef,
    CreateIndexResponseTypeDef,
    CreateQuerySuggestionsBlockListResponseTypeDef,
    CreateThesaurusResponseTypeDef,
    CustomDocumentEnrichmentConfigurationTypeDef,
    DataSourceConfigurationTypeDef,
    DataSourceSyncJobMetricTargetTypeDef,
    DescribeDataSourceResponseTypeDef,
    DescribeExperienceResponseTypeDef,
    DescribeFaqResponseTypeDef,
    DescribeIndexResponseTypeDef,
    DescribePrincipalMappingResponseTypeDef,
    DescribeQuerySuggestionsBlockListResponseTypeDef,
    DescribeQuerySuggestionsConfigResponseTypeDef,
    DescribeThesaurusResponseTypeDef,
    DisassociateEntitiesFromExperienceResponseTypeDef,
    DisassociatePersonasFromEntitiesResponseTypeDef,
    DocumentInfoTypeDef,
    DocumentMetadataConfigurationTypeDef,
    DocumentRelevanceConfigurationTypeDef,
    DocumentTypeDef,
    EntityConfigurationTypeDef,
    EntityPersonaConfigurationTypeDef,
    ExperienceConfigurationTypeDef,
    FacetTypeDef,
    GetQuerySuggestionsResponseTypeDef,
    GetSnapshotsResponseTypeDef,
    GroupMembersTypeDef,
    ListDataSourcesResponseTypeDef,
    ListDataSourceSyncJobsResponseTypeDef,
    ListEntityPersonasResponseTypeDef,
    ListExperienceEntitiesResponseTypeDef,
    ListExperiencesResponseTypeDef,
    ListFaqsResponseTypeDef,
    ListGroupsOlderThanOrderingIdResponseTypeDef,
    ListIndicesResponseTypeDef,
    ListQuerySuggestionsBlockListsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListThesauriResponseTypeDef,
    QueryResultTypeDef,
    RelevanceFeedbackTypeDef,
    S3PathTypeDef,
    ServerSideEncryptionConfigurationTypeDef,
    SortingConfigurationTypeDef,
    SpellCorrectionConfigurationTypeDef,
    StartDataSourceSyncJobResponseTypeDef,
    TagTypeDef,
    TimeRangeTypeDef,
    UserContextTypeDef,
    UserGroupResolutionConfigurationTypeDef,
    UserTokenConfigurationTypeDef,
)

__all__ = ("kendraClient",)


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
    InvalidRequestException: Type[BotocoreClientError]
    ResourceAlreadyExistException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourceUnavailableException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class kendraClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        kendraClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#exceptions)
        """

    async def associate_entities_to_experience(
        self, *, Id: str, IndexId: str, EntityList: Sequence["EntityConfigurationTypeDef"]
    ) -> AssociateEntitiesToExperienceResponseTypeDef:
        """
        Grants users or groups in your Amazon Web Services SSO identity source access to
        your Amazon Kendra experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.associate_entities_to_experience)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#associate_entities_to_experience)
        """

    async def associate_personas_to_entities(
        self, *, Id: str, IndexId: str, Personas: Sequence["EntityPersonaConfigurationTypeDef"]
    ) -> AssociatePersonasToEntitiesResponseTypeDef:
        """
        Defines the specific permissions of users or groups in your Amazon Web Services
        SSO identity source with access to your Amazon Kendra experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.associate_personas_to_entities)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#associate_personas_to_entities)
        """

    async def batch_delete_document(
        self,
        *,
        IndexId: str,
        DocumentIdList: Sequence[str],
        DataSourceSyncJobMetricTarget: "DataSourceSyncJobMetricTargetTypeDef" = ...
    ) -> BatchDeleteDocumentResponseTypeDef:
        """
        Removes one or more documents from an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.batch_delete_document)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#batch_delete_document)
        """

    async def batch_get_document_status(
        self, *, IndexId: str, DocumentInfoList: Sequence["DocumentInfoTypeDef"]
    ) -> BatchGetDocumentStatusResponseTypeDef:
        """
        Returns the indexing status for one or more documents submitted with the
        [BatchPutDocument](https://docs.aws.amazon.com/kendra/latest/dg/API_BatchPutDocument.html)_
        API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.batch_get_document_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#batch_get_document_status)
        """

    async def batch_put_document(
        self,
        *,
        IndexId: str,
        Documents: Sequence["DocumentTypeDef"],
        RoleArn: str = ...,
        CustomDocumentEnrichmentConfiguration: "CustomDocumentEnrichmentConfigurationTypeDef" = ...
    ) -> BatchPutDocumentResponseTypeDef:
        """
        Adds one or more documents to an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.batch_put_document)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#batch_put_document)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#can_paginate)
        """

    async def clear_query_suggestions(self, *, IndexId: str) -> None:
        """
        Clears existing query suggestions from an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.clear_query_suggestions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#clear_query_suggestions)
        """

    async def create_data_source(
        self,
        *,
        Name: str,
        IndexId: str,
        Type: DataSourceTypeType,
        Configuration: "DataSourceConfigurationTypeDef" = ...,
        Description: str = ...,
        Schedule: str = ...,
        RoleArn: str = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        ClientToken: str = ...,
        LanguageCode: str = ...,
        CustomDocumentEnrichmentConfiguration: "CustomDocumentEnrichmentConfigurationTypeDef" = ...
    ) -> CreateDataSourceResponseTypeDef:
        """
        Creates a data source that you want to use with an Amazon Kendra index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.create_data_source)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#create_data_source)
        """

    async def create_experience(
        self,
        *,
        Name: str,
        IndexId: str,
        RoleArn: str = ...,
        Configuration: "ExperienceConfigurationTypeDef" = ...,
        Description: str = ...,
        ClientToken: str = ...
    ) -> CreateExperienceResponseTypeDef:
        """
        Creates an Amazon Kendra experience such as a search application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.create_experience)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#create_experience)
        """

    async def create_faq(
        self,
        *,
        IndexId: str,
        Name: str,
        S3Path: "S3PathTypeDef",
        RoleArn: str,
        Description: str = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        FileFormat: FaqFileFormatType = ...,
        ClientToken: str = ...,
        LanguageCode: str = ...
    ) -> CreateFaqResponseTypeDef:
        """
        Creates an new set of frequently asked question (FAQ) questions and answers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.create_faq)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#create_faq)
        """

    async def create_index(
        self,
        *,
        Name: str,
        RoleArn: str,
        Edition: IndexEditionType = ...,
        ServerSideEncryptionConfiguration: "ServerSideEncryptionConfigurationTypeDef" = ...,
        Description: str = ...,
        ClientToken: str = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        UserTokenConfigurations: Sequence["UserTokenConfigurationTypeDef"] = ...,
        UserContextPolicy: UserContextPolicyType = ...,
        UserGroupResolutionConfiguration: "UserGroupResolutionConfigurationTypeDef" = ...
    ) -> CreateIndexResponseTypeDef:
        """
        Creates a new Amazon Kendra index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.create_index)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#create_index)
        """

    async def create_query_suggestions_block_list(
        self,
        *,
        IndexId: str,
        Name: str,
        SourceS3Path: "S3PathTypeDef",
        RoleArn: str,
        Description: str = ...,
        ClientToken: str = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateQuerySuggestionsBlockListResponseTypeDef:
        """
        Creates a block list to exlcude certain queries from suggestions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.create_query_suggestions_block_list)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#create_query_suggestions_block_list)
        """

    async def create_thesaurus(
        self,
        *,
        IndexId: str,
        Name: str,
        RoleArn: str,
        SourceS3Path: "S3PathTypeDef",
        Description: str = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        ClientToken: str = ...
    ) -> CreateThesaurusResponseTypeDef:
        """
        Creates a thesaurus for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.create_thesaurus)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#create_thesaurus)
        """

    async def delete_data_source(self, *, Id: str, IndexId: str) -> None:
        """
        Deletes an Amazon Kendra data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.delete_data_source)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#delete_data_source)
        """

    async def delete_experience(self, *, Id: str, IndexId: str) -> Dict[str, Any]:
        """
        Deletes your Amazon Kendra experience such as a search application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.delete_experience)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#delete_experience)
        """

    async def delete_faq(self, *, Id: str, IndexId: str) -> None:
        """
        Removes an FAQ from an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.delete_faq)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#delete_faq)
        """

    async def delete_index(self, *, Id: str) -> None:
        """
        Deletes an existing Amazon Kendra index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.delete_index)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#delete_index)
        """

    async def delete_principal_mapping(
        self, *, IndexId: str, GroupId: str, DataSourceId: str = ..., OrderingId: int = ...
    ) -> None:
        """
        Deletes a group so that all users and sub groups that belong to the group can no
        longer access documents only available to that group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.delete_principal_mapping)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#delete_principal_mapping)
        """

    async def delete_query_suggestions_block_list(self, *, IndexId: str, Id: str) -> None:
        """
        Deletes a block list used for query suggestions for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.delete_query_suggestions_block_list)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#delete_query_suggestions_block_list)
        """

    async def delete_thesaurus(self, *, Id: str, IndexId: str) -> None:
        """
        Deletes an existing Amazon Kendra thesaurus.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.delete_thesaurus)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#delete_thesaurus)
        """

    async def describe_data_source(
        self, *, Id: str, IndexId: str
    ) -> DescribeDataSourceResponseTypeDef:
        """
        Gets information about an Amazon Kendra data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.describe_data_source)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#describe_data_source)
        """

    async def describe_experience(
        self, *, Id: str, IndexId: str
    ) -> DescribeExperienceResponseTypeDef:
        """
        Gets information about your Amazon Kendra experience such as a search
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.describe_experience)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#describe_experience)
        """

    async def describe_faq(self, *, Id: str, IndexId: str) -> DescribeFaqResponseTypeDef:
        """
        Gets information about an FAQ list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.describe_faq)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#describe_faq)
        """

    async def describe_index(self, *, Id: str) -> DescribeIndexResponseTypeDef:
        """
        Describes an existing Amazon Kendra index See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/kendra-2019-02-03/DescribeIndex).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.describe_index)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#describe_index)
        """

    async def describe_principal_mapping(
        self, *, IndexId: str, GroupId: str, DataSourceId: str = ...
    ) -> DescribePrincipalMappingResponseTypeDef:
        """
        Describes the processing of `PUT` and `DELETE` actions for mapping users to
        their groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.describe_principal_mapping)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#describe_principal_mapping)
        """

    async def describe_query_suggestions_block_list(
        self, *, IndexId: str, Id: str
    ) -> DescribeQuerySuggestionsBlockListResponseTypeDef:
        """
        Describes a block list used for query suggestions for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.describe_query_suggestions_block_list)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#describe_query_suggestions_block_list)
        """

    async def describe_query_suggestions_config(
        self, *, IndexId: str
    ) -> DescribeQuerySuggestionsConfigResponseTypeDef:
        """
        Describes the settings of query suggestions for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.describe_query_suggestions_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#describe_query_suggestions_config)
        """

    async def describe_thesaurus(
        self, *, Id: str, IndexId: str
    ) -> DescribeThesaurusResponseTypeDef:
        """
        Describes an existing Amazon Kendra thesaurus.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.describe_thesaurus)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#describe_thesaurus)
        """

    async def disassociate_entities_from_experience(
        self, *, Id: str, IndexId: str, EntityList: Sequence["EntityConfigurationTypeDef"]
    ) -> DisassociateEntitiesFromExperienceResponseTypeDef:
        """
        Prevents users or groups in your Amazon Web Services SSO identity source from
        accessing your Amazon Kendra experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.disassociate_entities_from_experience)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#disassociate_entities_from_experience)
        """

    async def disassociate_personas_from_entities(
        self, *, Id: str, IndexId: str, EntityIds: Sequence[str]
    ) -> DisassociatePersonasFromEntitiesResponseTypeDef:
        """
        Removes the specific permissions of users or groups in your Amazon Web Services
        SSO identity source with access to your Amazon Kendra experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.disassociate_personas_from_entities)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#disassociate_personas_from_entities)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#generate_presigned_url)
        """

    async def get_query_suggestions(
        self, *, IndexId: str, QueryText: str, MaxSuggestionsCount: int = ...
    ) -> GetQuerySuggestionsResponseTypeDef:
        """
        Fetches the queries that are suggested to your users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.get_query_suggestions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#get_query_suggestions)
        """

    async def get_snapshots(
        self,
        *,
        IndexId: str,
        Interval: IntervalType,
        MetricType: MetricTypeType,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> GetSnapshotsResponseTypeDef:
        """
        Retrieves search metrics data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.get_snapshots)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#get_snapshots)
        """

    async def list_data_source_sync_jobs(
        self,
        *,
        Id: str,
        IndexId: str,
        NextToken: str = ...,
        MaxResults: int = ...,
        StartTimeFilter: "TimeRangeTypeDef" = ...,
        StatusFilter: DataSourceSyncJobStatusType = ...
    ) -> ListDataSourceSyncJobsResponseTypeDef:
        """
        Gets statistics about synchronizing Amazon Kendra with a data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.list_data_source_sync_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_data_source_sync_jobs)
        """

    async def list_data_sources(
        self, *, IndexId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListDataSourcesResponseTypeDef:
        """
        Lists the data sources that you have created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.list_data_sources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_data_sources)
        """

    async def list_entity_personas(
        self, *, Id: str, IndexId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListEntityPersonasResponseTypeDef:
        """
        Lists specific permissions of users and groups with access to your Amazon Kendra
        experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.list_entity_personas)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_entity_personas)
        """

    async def list_experience_entities(
        self, *, Id: str, IndexId: str, NextToken: str = ...
    ) -> ListExperienceEntitiesResponseTypeDef:
        """
        Lists users or groups in your Amazon Web Services SSO identity source that are
        granted access to your Amazon Kendra experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.list_experience_entities)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_experience_entities)
        """

    async def list_experiences(
        self, *, IndexId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListExperiencesResponseTypeDef:
        """
        Lists one or more Amazon Kendra experiences.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.list_experiences)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_experiences)
        """

    async def list_faqs(
        self, *, IndexId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListFaqsResponseTypeDef:
        """
        Gets a list of FAQ lists associated with an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.list_faqs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_faqs)
        """

    async def list_groups_older_than_ordering_id(
        self,
        *,
        IndexId: str,
        OrderingId: int,
        DataSourceId: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListGroupsOlderThanOrderingIdResponseTypeDef:
        """
        Provides a list of groups that are mapped to users before a given ordering or
        timestamp identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.list_groups_older_than_ordering_id)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_groups_older_than_ordering_id)
        """

    async def list_indices(
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> ListIndicesResponseTypeDef:
        """
        Lists the Amazon Kendra indexes that you have created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.list_indices)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_indices)
        """

    async def list_query_suggestions_block_lists(
        self, *, IndexId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListQuerySuggestionsBlockListsResponseTypeDef:
        """
        Lists the block lists used for query suggestions for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.list_query_suggestions_block_lists)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_query_suggestions_block_lists)
        """

    async def list_tags_for_resource(
        self, *, ResourceARN: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Gets a list of tags associated with a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_tags_for_resource)
        """

    async def list_thesauri(
        self, *, IndexId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListThesauriResponseTypeDef:
        """
        Lists the Amazon Kendra thesauri associated with an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.list_thesauri)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_thesauri)
        """

    async def put_principal_mapping(
        self,
        *,
        IndexId: str,
        GroupId: str,
        GroupMembers: "GroupMembersTypeDef",
        DataSourceId: str = ...,
        OrderingId: int = ...,
        RoleArn: str = ...
    ) -> None:
        """
        Maps users to their groups so that you only need to provide the user ID when you
        issue the query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.put_principal_mapping)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#put_principal_mapping)
        """

    async def query(
        self,
        *,
        IndexId: str,
        QueryText: str = ...,
        AttributeFilter: "AttributeFilterTypeDef" = ...,
        Facets: Sequence["FacetTypeDef"] = ...,
        RequestedDocumentAttributes: Sequence[str] = ...,
        QueryResultTypeFilter: QueryResultTypeType = ...,
        DocumentRelevanceOverrideConfigurations: Sequence[
            "DocumentRelevanceConfigurationTypeDef"
        ] = ...,
        PageNumber: int = ...,
        PageSize: int = ...,
        SortingConfiguration: "SortingConfigurationTypeDef" = ...,
        UserContext: "UserContextTypeDef" = ...,
        VisitorId: str = ...,
        SpellCorrectionConfiguration: "SpellCorrectionConfigurationTypeDef" = ...
    ) -> QueryResultTypeDef:
        """
        Searches an active index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.query)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#query)
        """

    async def start_data_source_sync_job(
        self, *, Id: str, IndexId: str
    ) -> StartDataSourceSyncJobResponseTypeDef:
        """
        Starts a synchronization job for a data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.start_data_source_sync_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#start_data_source_sync_job)
        """

    async def stop_data_source_sync_job(self, *, Id: str, IndexId: str) -> None:
        """
        Stops a synchronization job that is currently running.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.stop_data_source_sync_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#stop_data_source_sync_job)
        """

    async def submit_feedback(
        self,
        *,
        IndexId: str,
        QueryId: str,
        ClickFeedbackItems: Sequence["ClickFeedbackTypeDef"] = ...,
        RelevanceFeedbackItems: Sequence["RelevanceFeedbackTypeDef"] = ...
    ) -> None:
        """
        Enables you to provide feedback to Amazon Kendra to improve the performance of
        your index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.submit_feedback)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#submit_feedback)
        """

    async def tag_resource(
        self, *, ResourceARN: str, Tags: Sequence["TagTypeDef"]
    ) -> Dict[str, Any]:
        """
        Adds the specified tag to the specified index, FAQ, or data source resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#tag_resource)
        """

    async def untag_resource(self, *, ResourceARN: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes a tag from an index, FAQ, or a data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#untag_resource)
        """

    async def update_data_source(
        self,
        *,
        Id: str,
        IndexId: str,
        Name: str = ...,
        Configuration: "DataSourceConfigurationTypeDef" = ...,
        Description: str = ...,
        Schedule: str = ...,
        RoleArn: str = ...,
        LanguageCode: str = ...,
        CustomDocumentEnrichmentConfiguration: "CustomDocumentEnrichmentConfigurationTypeDef" = ...
    ) -> None:
        """
        Updates an existing Amazon Kendra data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.update_data_source)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#update_data_source)
        """

    async def update_experience(
        self,
        *,
        Id: str,
        IndexId: str,
        Name: str = ...,
        RoleArn: str = ...,
        Configuration: "ExperienceConfigurationTypeDef" = ...,
        Description: str = ...
    ) -> None:
        """
        Updates your Amazon Kendra experience such as a search application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.update_experience)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#update_experience)
        """

    async def update_index(
        self,
        *,
        Id: str,
        Name: str = ...,
        RoleArn: str = ...,
        Description: str = ...,
        DocumentMetadataConfigurationUpdates: Sequence[
            "DocumentMetadataConfigurationTypeDef"
        ] = ...,
        CapacityUnits: "CapacityUnitsConfigurationTypeDef" = ...,
        UserTokenConfigurations: Sequence["UserTokenConfigurationTypeDef"] = ...,
        UserContextPolicy: UserContextPolicyType = ...,
        UserGroupResolutionConfiguration: "UserGroupResolutionConfigurationTypeDef" = ...
    ) -> None:
        """
        Updates an existing Amazon Kendra index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.update_index)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#update_index)
        """

    async def update_query_suggestions_block_list(
        self,
        *,
        IndexId: str,
        Id: str,
        Name: str = ...,
        Description: str = ...,
        SourceS3Path: "S3PathTypeDef" = ...,
        RoleArn: str = ...
    ) -> None:
        """
        Updates a block list used for query suggestions for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.update_query_suggestions_block_list)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#update_query_suggestions_block_list)
        """

    async def update_query_suggestions_config(
        self,
        *,
        IndexId: str,
        Mode: ModeType = ...,
        QueryLogLookBackWindowInDays: int = ...,
        IncludeQueriesWithoutUserInformation: bool = ...,
        MinimumNumberOfQueryingUsers: int = ...,
        MinimumQueryCount: int = ...
    ) -> None:
        """
        Updates the settings of query suggestions for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.update_query_suggestions_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#update_query_suggestions_config)
        """

    async def update_thesaurus(
        self,
        *,
        Id: str,
        IndexId: str,
        Name: str = ...,
        Description: str = ...,
        RoleArn: str = ...,
        SourceS3Path: "S3PathTypeDef" = ...
    ) -> None:
        """
        Updates a thesaurus file associated with an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client.update_thesaurus)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#update_thesaurus)
        """

    async def __aenter__(self) -> "kendraClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#kendra.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/)
        """
