"""
Type annotations for inspector service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_inspector.client import InspectorClient
    from types_aiobotocore_inspector.paginator import (
        ListAssessmentRunAgentsPaginator,
        ListAssessmentRunsPaginator,
        ListAssessmentTargetsPaginator,
        ListAssessmentTemplatesPaginator,
        ListEventSubscriptionsPaginator,
        ListExclusionsPaginator,
        ListFindingsPaginator,
        ListRulesPackagesPaginator,
        PreviewAgentsPaginator,
    )

    session = get_session()
    with session.create_client("inspector") as client:
        client: InspectorClient

        list_assessment_run_agents_paginator: ListAssessmentRunAgentsPaginator = client.get_paginator("list_assessment_run_agents")
        list_assessment_runs_paginator: ListAssessmentRunsPaginator = client.get_paginator("list_assessment_runs")
        list_assessment_targets_paginator: ListAssessmentTargetsPaginator = client.get_paginator("list_assessment_targets")
        list_assessment_templates_paginator: ListAssessmentTemplatesPaginator = client.get_paginator("list_assessment_templates")
        list_event_subscriptions_paginator: ListEventSubscriptionsPaginator = client.get_paginator("list_event_subscriptions")
        list_exclusions_paginator: ListExclusionsPaginator = client.get_paginator("list_exclusions")
        list_findings_paginator: ListFindingsPaginator = client.get_paginator("list_findings")
        list_rules_packages_paginator: ListRulesPackagesPaginator = client.get_paginator("list_rules_packages")
        preview_agents_paginator: PreviewAgentsPaginator = client.get_paginator("preview_agents")
    ```
"""
import sys
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    AgentFilterTypeDef,
    AssessmentRunFilterTypeDef,
    AssessmentTargetFilterTypeDef,
    AssessmentTemplateFilterTypeDef,
    FindingFilterTypeDef,
    ListAssessmentRunAgentsResponseTypeDef,
    ListAssessmentRunsResponseTypeDef,
    ListAssessmentTargetsResponseTypeDef,
    ListAssessmentTemplatesResponseTypeDef,
    ListEventSubscriptionsResponseTypeDef,
    ListExclusionsResponseTypeDef,
    ListFindingsResponseTypeDef,
    ListRulesPackagesResponseTypeDef,
    PaginatorConfigTypeDef,
    PreviewAgentsResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator


__all__ = (
    "ListAssessmentRunAgentsPaginator",
    "ListAssessmentRunsPaginator",
    "ListAssessmentTargetsPaginator",
    "ListAssessmentTemplatesPaginator",
    "ListEventSubscriptionsPaginator",
    "ListExclusionsPaginator",
    "ListFindingsPaginator",
    "ListRulesPackagesPaginator",
    "PreviewAgentsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListAssessmentRunAgentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Paginator.ListAssessmentRunAgents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#listassessmentrunagentspaginator)
    """

    def paginate(
        self,
        *,
        assessmentRunArn: str,
        filter: "AgentFilterTypeDef" = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListAssessmentRunAgentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Paginator.ListAssessmentRunAgents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#listassessmentrunagentspaginator)
        """


class ListAssessmentRunsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Paginator.ListAssessmentRuns)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#listassessmentrunspaginator)
    """

    def paginate(
        self,
        *,
        assessmentTemplateArns: Sequence[str] = ...,
        filter: "AssessmentRunFilterTypeDef" = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListAssessmentRunsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Paginator.ListAssessmentRuns.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#listassessmentrunspaginator)
        """


class ListAssessmentTargetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Paginator.ListAssessmentTargets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#listassessmenttargetspaginator)
    """

    def paginate(
        self,
        *,
        filter: "AssessmentTargetFilterTypeDef" = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListAssessmentTargetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Paginator.ListAssessmentTargets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#listassessmenttargetspaginator)
        """


class ListAssessmentTemplatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Paginator.ListAssessmentTemplates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#listassessmenttemplatespaginator)
    """

    def paginate(
        self,
        *,
        assessmentTargetArns: Sequence[str] = ...,
        filter: "AssessmentTemplateFilterTypeDef" = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListAssessmentTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Paginator.ListAssessmentTemplates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#listassessmenttemplatespaginator)
        """


class ListEventSubscriptionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Paginator.ListEventSubscriptions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#listeventsubscriptionspaginator)
    """

    def paginate(
        self, *, resourceArn: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListEventSubscriptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Paginator.ListEventSubscriptions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#listeventsubscriptionspaginator)
        """


class ListExclusionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Paginator.ListExclusions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#listexclusionspaginator)
    """

    def paginate(
        self, *, assessmentRunArn: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListExclusionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Paginator.ListExclusions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#listexclusionspaginator)
        """


class ListFindingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Paginator.ListFindings)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#listfindingspaginator)
    """

    def paginate(
        self,
        *,
        assessmentRunArns: Sequence[str] = ...,
        filter: "FindingFilterTypeDef" = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Paginator.ListFindings.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#listfindingspaginator)
        """


class ListRulesPackagesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Paginator.ListRulesPackages)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#listrulespackagespaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListRulesPackagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Paginator.ListRulesPackages.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#listrulespackagespaginator)
        """


class PreviewAgentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Paginator.PreviewAgents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#previewagentspaginator)
    """

    def paginate(
        self, *, previewAgentsArn: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[PreviewAgentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Paginator.PreviewAgents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#previewagentspaginator)
        """
