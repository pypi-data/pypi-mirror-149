"""
Type annotations for inspector service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_inspector.client import InspectorClient

    session = get_session()
    async with session.create_client("inspector") as client:
        client: InspectorClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import InspectorEventType, ReportFileFormatType, ReportTypeType, StopActionType
from .paginator import (
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
from .type_defs import (
    AddAttributesToFindingsResponseTypeDef,
    AgentFilterTypeDef,
    AssessmentRunFilterTypeDef,
    AssessmentTargetFilterTypeDef,
    AssessmentTemplateFilterTypeDef,
    AttributeTypeDef,
    CreateAssessmentTargetResponseTypeDef,
    CreateAssessmentTemplateResponseTypeDef,
    CreateExclusionsPreviewResponseTypeDef,
    CreateResourceGroupResponseTypeDef,
    DescribeAssessmentRunsResponseTypeDef,
    DescribeAssessmentTargetsResponseTypeDef,
    DescribeAssessmentTemplatesResponseTypeDef,
    DescribeCrossAccountAccessRoleResponseTypeDef,
    DescribeExclusionsResponseTypeDef,
    DescribeFindingsResponseTypeDef,
    DescribeResourceGroupsResponseTypeDef,
    DescribeRulesPackagesResponseTypeDef,
    FindingFilterTypeDef,
    GetAssessmentReportResponseTypeDef,
    GetExclusionsPreviewResponseTypeDef,
    GetTelemetryMetadataResponseTypeDef,
    ListAssessmentRunAgentsResponseTypeDef,
    ListAssessmentRunsResponseTypeDef,
    ListAssessmentTargetsResponseTypeDef,
    ListAssessmentTemplatesResponseTypeDef,
    ListEventSubscriptionsResponseTypeDef,
    ListExclusionsResponseTypeDef,
    ListFindingsResponseTypeDef,
    ListRulesPackagesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    PreviewAgentsResponseTypeDef,
    RemoveAttributesFromFindingsResponseTypeDef,
    ResourceGroupTagTypeDef,
    StartAssessmentRunResponseTypeDef,
    TagTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("InspectorClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    AgentsAlreadyRunningAssessmentException: Type[BotocoreClientError]
    AssessmentRunInProgressException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalException: Type[BotocoreClientError]
    InvalidCrossAccountRoleException: Type[BotocoreClientError]
    InvalidInputException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NoSuchEntityException: Type[BotocoreClientError]
    PreviewGenerationInProgressException: Type[BotocoreClientError]
    ServiceTemporarilyUnavailableException: Type[BotocoreClientError]
    UnsupportedFeatureException: Type[BotocoreClientError]

class InspectorClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        InspectorClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#exceptions)
        """
    async def add_attributes_to_findings(
        self, *, findingArns: Sequence[str], attributes: Sequence["AttributeTypeDef"]
    ) -> AddAttributesToFindingsResponseTypeDef:
        """
        Assigns attributes (key and value pairs) to the findings that are specified by
        the ARNs of the findings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.add_attributes_to_findings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#add_attributes_to_findings)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#can_paginate)
        """
    async def create_assessment_target(
        self, *, assessmentTargetName: str, resourceGroupArn: str = ...
    ) -> CreateAssessmentTargetResponseTypeDef:
        """
        Creates a new assessment target using the ARN of the resource group that is
        generated by  CreateResourceGroup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.create_assessment_target)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#create_assessment_target)
        """
    async def create_assessment_template(
        self,
        *,
        assessmentTargetArn: str,
        assessmentTemplateName: str,
        durationInSeconds: int,
        rulesPackageArns: Sequence[str],
        userAttributesForFindings: Sequence["AttributeTypeDef"] = ...
    ) -> CreateAssessmentTemplateResponseTypeDef:
        """
        Creates an assessment template for the assessment target that is specified by
        the ARN of the assessment target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.create_assessment_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#create_assessment_template)
        """
    async def create_exclusions_preview(
        self, *, assessmentTemplateArn: str
    ) -> CreateExclusionsPreviewResponseTypeDef:
        """
        Starts the generation of an exclusions preview for the specified assessment
        template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.create_exclusions_preview)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#create_exclusions_preview)
        """
    async def create_resource_group(
        self, *, resourceGroupTags: Sequence["ResourceGroupTagTypeDef"]
    ) -> CreateResourceGroupResponseTypeDef:
        """
        Creates a resource group using the specified set of tags (key and value pairs)
        that are used to select the EC2 instances to be included in an Amazon Inspector
        assessment target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.create_resource_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#create_resource_group)
        """
    async def delete_assessment_run(self, *, assessmentRunArn: str) -> None:
        """
        Deletes the assessment run that is specified by the ARN of the assessment run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.delete_assessment_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#delete_assessment_run)
        """
    async def delete_assessment_target(self, *, assessmentTargetArn: str) -> None:
        """
        Deletes the assessment target that is specified by the ARN of the assessment
        target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.delete_assessment_target)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#delete_assessment_target)
        """
    async def delete_assessment_template(self, *, assessmentTemplateArn: str) -> None:
        """
        Deletes the assessment template that is specified by the ARN of the assessment
        template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.delete_assessment_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#delete_assessment_template)
        """
    async def describe_assessment_runs(
        self, *, assessmentRunArns: Sequence[str]
    ) -> DescribeAssessmentRunsResponseTypeDef:
        """
        Describes the assessment runs that are specified by the ARNs of the assessment
        runs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.describe_assessment_runs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#describe_assessment_runs)
        """
    async def describe_assessment_targets(
        self, *, assessmentTargetArns: Sequence[str]
    ) -> DescribeAssessmentTargetsResponseTypeDef:
        """
        Describes the assessment targets that are specified by the ARNs of the
        assessment targets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.describe_assessment_targets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#describe_assessment_targets)
        """
    async def describe_assessment_templates(
        self, *, assessmentTemplateArns: Sequence[str]
    ) -> DescribeAssessmentTemplatesResponseTypeDef:
        """
        Describes the assessment templates that are specified by the ARNs of the
        assessment templates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.describe_assessment_templates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#describe_assessment_templates)
        """
    async def describe_cross_account_access_role(
        self,
    ) -> DescribeCrossAccountAccessRoleResponseTypeDef:
        """
        Describes the IAM role that enables Amazon Inspector to access your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.describe_cross_account_access_role)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#describe_cross_account_access_role)
        """
    async def describe_exclusions(
        self, *, exclusionArns: Sequence[str], locale: Literal["EN_US"] = ...
    ) -> DescribeExclusionsResponseTypeDef:
        """
        Describes the exclusions that are specified by the exclusions' ARNs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.describe_exclusions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#describe_exclusions)
        """
    async def describe_findings(
        self, *, findingArns: Sequence[str], locale: Literal["EN_US"] = ...
    ) -> DescribeFindingsResponseTypeDef:
        """
        Describes the findings that are specified by the ARNs of the findings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.describe_findings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#describe_findings)
        """
    async def describe_resource_groups(
        self, *, resourceGroupArns: Sequence[str]
    ) -> DescribeResourceGroupsResponseTypeDef:
        """
        Describes the resource groups that are specified by the ARNs of the resource
        groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.describe_resource_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#describe_resource_groups)
        """
    async def describe_rules_packages(
        self, *, rulesPackageArns: Sequence[str], locale: Literal["EN_US"] = ...
    ) -> DescribeRulesPackagesResponseTypeDef:
        """
        Describes the rules packages that are specified by the ARNs of the rules
        packages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.describe_rules_packages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#describe_rules_packages)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#generate_presigned_url)
        """
    async def get_assessment_report(
        self,
        *,
        assessmentRunArn: str,
        reportFileFormat: ReportFileFormatType,
        reportType: ReportTypeType
    ) -> GetAssessmentReportResponseTypeDef:
        """
        Produces an assessment report that includes detailed and comprehensive results
        of a specified assessment run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.get_assessment_report)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#get_assessment_report)
        """
    async def get_exclusions_preview(
        self,
        *,
        assessmentTemplateArn: str,
        previewToken: str,
        nextToken: str = ...,
        maxResults: int = ...,
        locale: Literal["EN_US"] = ...
    ) -> GetExclusionsPreviewResponseTypeDef:
        """
        Retrieves the exclusions preview (a list of ExclusionPreview objects) specified
        by the preview token.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.get_exclusions_preview)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#get_exclusions_preview)
        """
    async def get_telemetry_metadata(
        self, *, assessmentRunArn: str
    ) -> GetTelemetryMetadataResponseTypeDef:
        """
        Information about the data that is collected for the specified assessment run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.get_telemetry_metadata)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#get_telemetry_metadata)
        """
    async def list_assessment_run_agents(
        self,
        *,
        assessmentRunArn: str,
        filter: "AgentFilterTypeDef" = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListAssessmentRunAgentsResponseTypeDef:
        """
        Lists the agents of the assessment runs that are specified by the ARNs of the
        assessment runs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.list_assessment_run_agents)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#list_assessment_run_agents)
        """
    async def list_assessment_runs(
        self,
        *,
        assessmentTemplateArns: Sequence[str] = ...,
        filter: "AssessmentRunFilterTypeDef" = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListAssessmentRunsResponseTypeDef:
        """
        Lists the assessment runs that correspond to the assessment templates that are
        specified by the ARNs of the assessment templates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.list_assessment_runs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#list_assessment_runs)
        """
    async def list_assessment_targets(
        self,
        *,
        filter: "AssessmentTargetFilterTypeDef" = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListAssessmentTargetsResponseTypeDef:
        """
        Lists the ARNs of the assessment targets within this AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.list_assessment_targets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#list_assessment_targets)
        """
    async def list_assessment_templates(
        self,
        *,
        assessmentTargetArns: Sequence[str] = ...,
        filter: "AssessmentTemplateFilterTypeDef" = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListAssessmentTemplatesResponseTypeDef:
        """
        Lists the assessment templates that correspond to the assessment targets that
        are specified by the ARNs of the assessment targets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.list_assessment_templates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#list_assessment_templates)
        """
    async def list_event_subscriptions(
        self, *, resourceArn: str = ..., nextToken: str = ..., maxResults: int = ...
    ) -> ListEventSubscriptionsResponseTypeDef:
        """
        Lists all the event subscriptions for the assessment template that is specified
        by the ARN of the assessment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.list_event_subscriptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#list_event_subscriptions)
        """
    async def list_exclusions(
        self, *, assessmentRunArn: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListExclusionsResponseTypeDef:
        """
        List exclusions that are generated by the assessment run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.list_exclusions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#list_exclusions)
        """
    async def list_findings(
        self,
        *,
        assessmentRunArns: Sequence[str] = ...,
        filter: "FindingFilterTypeDef" = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListFindingsResponseTypeDef:
        """
        Lists findings that are generated by the assessment runs that are specified by
        the ARNs of the assessment runs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.list_findings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#list_findings)
        """
    async def list_rules_packages(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListRulesPackagesResponseTypeDef:
        """
        Lists all available Amazon Inspector rules packages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.list_rules_packages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#list_rules_packages)
        """
    async def list_tags_for_resource(
        self, *, resourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all tags associated with an assessment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#list_tags_for_resource)
        """
    async def preview_agents(
        self, *, previewAgentsArn: str, nextToken: str = ..., maxResults: int = ...
    ) -> PreviewAgentsResponseTypeDef:
        """
        Previews the agents installed on the EC2 instances that are part of the
        specified assessment target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.preview_agents)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#preview_agents)
        """
    async def register_cross_account_access_role(self, *, roleArn: str) -> None:
        """
        Registers the IAM role that grants Amazon Inspector access to AWS Services
        needed to perform security assessments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.register_cross_account_access_role)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#register_cross_account_access_role)
        """
    async def remove_attributes_from_findings(
        self, *, findingArns: Sequence[str], attributeKeys: Sequence[str]
    ) -> RemoveAttributesFromFindingsResponseTypeDef:
        """
        Removes entire attributes (key and value pairs) from the findings that are
        specified by the ARNs of the findings where an attribute with the specified key
        exists.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.remove_attributes_from_findings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#remove_attributes_from_findings)
        """
    async def set_tags_for_resource(
        self, *, resourceArn: str, tags: Sequence["TagTypeDef"] = ...
    ) -> None:
        """
        Sets tags (key and value pairs) to the assessment template that is specified by
        the ARN of the assessment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.set_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#set_tags_for_resource)
        """
    async def start_assessment_run(
        self, *, assessmentTemplateArn: str, assessmentRunName: str = ...
    ) -> StartAssessmentRunResponseTypeDef:
        """
        Starts the assessment run specified by the ARN of the assessment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.start_assessment_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#start_assessment_run)
        """
    async def stop_assessment_run(
        self, *, assessmentRunArn: str, stopAction: StopActionType = ...
    ) -> None:
        """
        Stops the assessment run that is specified by the ARN of the assessment run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.stop_assessment_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#stop_assessment_run)
        """
    async def subscribe_to_event(
        self, *, resourceArn: str, event: InspectorEventType, topicArn: str
    ) -> None:
        """
        Enables the process of sending Amazon Simple Notification Service (SNS)
        notifications about a specified event to a specified SNS topic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.subscribe_to_event)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#subscribe_to_event)
        """
    async def unsubscribe_from_event(
        self, *, resourceArn: str, event: InspectorEventType, topicArn: str
    ) -> None:
        """
        Disables the process of sending Amazon Simple Notification Service (SNS)
        notifications about a specified event to a specified SNS topic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.unsubscribe_from_event)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#unsubscribe_from_event)
        """
    async def update_assessment_target(
        self, *, assessmentTargetArn: str, assessmentTargetName: str, resourceGroupArn: str = ...
    ) -> None:
        """
        Updates the assessment target that is specified by the ARN of the assessment
        target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.update_assessment_target)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#update_assessment_target)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_assessment_run_agents"]
    ) -> ListAssessmentRunAgentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_assessment_runs"]
    ) -> ListAssessmentRunsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_assessment_targets"]
    ) -> ListAssessmentTargetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_assessment_templates"]
    ) -> ListAssessmentTemplatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_event_subscriptions"]
    ) -> ListEventSubscriptionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_exclusions"]) -> ListExclusionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_findings"]) -> ListFindingsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_rules_packages"]
    ) -> ListRulesPackagesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["preview_agents"]) -> PreviewAgentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/#get_paginator)
        """
    async def __aenter__(self) -> "InspectorClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector.html#Inspector.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/client/)
        """
