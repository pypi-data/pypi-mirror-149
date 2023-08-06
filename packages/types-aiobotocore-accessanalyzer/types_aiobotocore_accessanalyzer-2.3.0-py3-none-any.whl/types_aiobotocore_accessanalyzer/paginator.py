"""
Type annotations for accessanalyzer service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_accessanalyzer.client import AccessAnalyzerClient
    from types_aiobotocore_accessanalyzer.paginator import (
        ListAccessPreviewFindingsPaginator,
        ListAccessPreviewsPaginator,
        ListAnalyzedResourcesPaginator,
        ListAnalyzersPaginator,
        ListArchiveRulesPaginator,
        ListFindingsPaginator,
        ListPolicyGenerationsPaginator,
        ValidatePolicyPaginator,
    )

    session = get_session()
    with session.create_client("accessanalyzer") as client:
        client: AccessAnalyzerClient

        list_access_preview_findings_paginator: ListAccessPreviewFindingsPaginator = client.get_paginator("list_access_preview_findings")
        list_access_previews_paginator: ListAccessPreviewsPaginator = client.get_paginator("list_access_previews")
        list_analyzed_resources_paginator: ListAnalyzedResourcesPaginator = client.get_paginator("list_analyzed_resources")
        list_analyzers_paginator: ListAnalyzersPaginator = client.get_paginator("list_analyzers")
        list_archive_rules_paginator: ListArchiveRulesPaginator = client.get_paginator("list_archive_rules")
        list_findings_paginator: ListFindingsPaginator = client.get_paginator("list_findings")
        list_policy_generations_paginator: ListPolicyGenerationsPaginator = client.get_paginator("list_policy_generations")
        validate_policy_paginator: ValidatePolicyPaginator = client.get_paginator("validate_policy")
    ```
"""
import sys
from typing import Generic, Iterator, Mapping, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import (
    LocaleType,
    PolicyTypeType,
    ResourceTypeType,
    TypeType,
    ValidatePolicyResourceTypeType,
)
from .type_defs import (
    CriterionTypeDef,
    ListAccessPreviewFindingsResponseTypeDef,
    ListAccessPreviewsResponseTypeDef,
    ListAnalyzedResourcesResponseTypeDef,
    ListAnalyzersResponseTypeDef,
    ListArchiveRulesResponseTypeDef,
    ListFindingsResponseTypeDef,
    ListPolicyGenerationsResponseTypeDef,
    PaginatorConfigTypeDef,
    SortCriteriaTypeDef,
    ValidatePolicyResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator


__all__ = (
    "ListAccessPreviewFindingsPaginator",
    "ListAccessPreviewsPaginator",
    "ListAnalyzedResourcesPaginator",
    "ListAnalyzersPaginator",
    "ListArchiveRulesPaginator",
    "ListFindingsPaginator",
    "ListPolicyGenerationsPaginator",
    "ValidatePolicyPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAccessPreviewFindingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAccessPreviewFindings)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#listaccesspreviewfindingspaginator)
    """

    def paginate(
        self,
        *,
        accessPreviewId: str,
        analyzerArn: str,
        filter: Mapping[str, "CriterionTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListAccessPreviewFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAccessPreviewFindings.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#listaccesspreviewfindingspaginator)
        """


class ListAccessPreviewsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAccessPreviews)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#listaccesspreviewspaginator)
    """

    def paginate(
        self, *, analyzerArn: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListAccessPreviewsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAccessPreviews.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#listaccesspreviewspaginator)
        """


class ListAnalyzedResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAnalyzedResources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#listanalyzedresourcespaginator)
    """

    def paginate(
        self,
        *,
        analyzerArn: str,
        resourceType: ResourceTypeType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListAnalyzedResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAnalyzedResources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#listanalyzedresourcespaginator)
        """


class ListAnalyzersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAnalyzers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#listanalyzerspaginator)
    """

    def paginate(
        self, *, type: TypeType = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListAnalyzersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAnalyzers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#listanalyzerspaginator)
        """


class ListArchiveRulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListArchiveRules)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#listarchiverulespaginator)
    """

    def paginate(
        self, *, analyzerName: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListArchiveRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListArchiveRules.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#listarchiverulespaginator)
        """


class ListFindingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListFindings)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#listfindingspaginator)
    """

    def paginate(
        self,
        *,
        analyzerArn: str,
        filter: Mapping[str, "CriterionTypeDef"] = ...,
        sort: "SortCriteriaTypeDef" = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListFindings.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#listfindingspaginator)
        """


class ListPolicyGenerationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListPolicyGenerations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#listpolicygenerationspaginator)
    """

    def paginate(
        self, *, principalArn: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListPolicyGenerationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListPolicyGenerations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#listpolicygenerationspaginator)
        """


class ValidatePolicyPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ValidatePolicy)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#validatepolicypaginator)
    """

    def paginate(
        self,
        *,
        policyDocument: str,
        policyType: PolicyTypeType,
        locale: LocaleType = ...,
        validatePolicyResourceType: ValidatePolicyResourceTypeType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ValidatePolicyResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ValidatePolicy.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/paginators/#validatepolicypaginator)
        """
