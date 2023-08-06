"""
Type annotations for codebuild service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_codebuild.client import CodeBuildClient

    session = get_session()
    async with session.create_client("codebuild") as client:
        client: CodeBuildClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    AuthTypeType,
    ComputeTypeType,
    EnvironmentTypeType,
    ImagePullCredentialsTypeType,
    ProjectSortByTypeType,
    ProjectVisibilityTypeType,
    ReportCodeCoverageSortByTypeType,
    ReportGroupSortByTypeType,
    ReportGroupTrendFieldTypeType,
    ReportTypeType,
    RetryBuildBatchTypeType,
    ServerTypeType,
    SharedResourceSortByTypeType,
    SortOrderTypeType,
    SourceTypeType,
    WebhookBuildTypeType,
)
from .paginator import (
    DescribeCodeCoveragesPaginator,
    DescribeTestCasesPaginator,
    ListBuildBatchesForProjectPaginator,
    ListBuildBatchesPaginator,
    ListBuildsForProjectPaginator,
    ListBuildsPaginator,
    ListProjectsPaginator,
    ListReportGroupsPaginator,
    ListReportsForReportGroupPaginator,
    ListReportsPaginator,
    ListSharedProjectsPaginator,
    ListSharedReportGroupsPaginator,
)
from .type_defs import (
    BatchDeleteBuildsOutputTypeDef,
    BatchGetBuildBatchesOutputTypeDef,
    BatchGetBuildsOutputTypeDef,
    BatchGetProjectsOutputTypeDef,
    BatchGetReportGroupsOutputTypeDef,
    BatchGetReportsOutputTypeDef,
    BuildBatchFilterTypeDef,
    BuildStatusConfigTypeDef,
    CreateProjectOutputTypeDef,
    CreateReportGroupOutputTypeDef,
    CreateWebhookOutputTypeDef,
    DeleteBuildBatchOutputTypeDef,
    DeleteSourceCredentialsOutputTypeDef,
    DescribeCodeCoveragesOutputTypeDef,
    DescribeTestCasesOutputTypeDef,
    EnvironmentVariableTypeDef,
    GetReportGroupTrendOutputTypeDef,
    GetResourcePolicyOutputTypeDef,
    GitSubmodulesConfigTypeDef,
    ImportSourceCredentialsOutputTypeDef,
    ListBuildBatchesForProjectOutputTypeDef,
    ListBuildBatchesOutputTypeDef,
    ListBuildsForProjectOutputTypeDef,
    ListBuildsOutputTypeDef,
    ListCuratedEnvironmentImagesOutputTypeDef,
    ListProjectsOutputTypeDef,
    ListReportGroupsOutputTypeDef,
    ListReportsForReportGroupOutputTypeDef,
    ListReportsOutputTypeDef,
    ListSharedProjectsOutputTypeDef,
    ListSharedReportGroupsOutputTypeDef,
    ListSourceCredentialsOutputTypeDef,
    LogsConfigTypeDef,
    ProjectArtifactsTypeDef,
    ProjectBuildBatchConfigTypeDef,
    ProjectCacheTypeDef,
    ProjectEnvironmentTypeDef,
    ProjectFileSystemLocationTypeDef,
    ProjectSourceTypeDef,
    ProjectSourceVersionTypeDef,
    PutResourcePolicyOutputTypeDef,
    RegistryCredentialTypeDef,
    ReportExportConfigTypeDef,
    ReportFilterTypeDef,
    RetryBuildBatchOutputTypeDef,
    RetryBuildOutputTypeDef,
    SourceAuthTypeDef,
    StartBuildBatchOutputTypeDef,
    StartBuildOutputTypeDef,
    StopBuildBatchOutputTypeDef,
    StopBuildOutputTypeDef,
    TagTypeDef,
    TestCaseFilterTypeDef,
    UpdateProjectOutputTypeDef,
    UpdateProjectVisibilityOutputTypeDef,
    UpdateReportGroupOutputTypeDef,
    UpdateWebhookOutputTypeDef,
    VpcConfigTypeDef,
    WebhookFilterTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("CodeBuildClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccountLimitExceededException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InvalidInputException: Type[BotocoreClientError]
    OAuthProviderException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]


class CodeBuildClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CodeBuildClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#exceptions)
        """

    async def batch_delete_builds(self, *, ids: Sequence[str]) -> BatchDeleteBuildsOutputTypeDef:
        """
        Deletes one or more builds.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.batch_delete_builds)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#batch_delete_builds)
        """

    async def batch_get_build_batches(
        self, *, ids: Sequence[str]
    ) -> BatchGetBuildBatchesOutputTypeDef:
        """
        Retrieves information about one or more batch builds.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.batch_get_build_batches)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#batch_get_build_batches)
        """

    async def batch_get_builds(self, *, ids: Sequence[str]) -> BatchGetBuildsOutputTypeDef:
        """
        Gets information about one or more builds.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.batch_get_builds)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#batch_get_builds)
        """

    async def batch_get_projects(self, *, names: Sequence[str]) -> BatchGetProjectsOutputTypeDef:
        """
        Gets information about one or more build projects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.batch_get_projects)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#batch_get_projects)
        """

    async def batch_get_report_groups(
        self, *, reportGroupArns: Sequence[str]
    ) -> BatchGetReportGroupsOutputTypeDef:
        """
        Returns an array of report groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.batch_get_report_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#batch_get_report_groups)
        """

    async def batch_get_reports(self, *, reportArns: Sequence[str]) -> BatchGetReportsOutputTypeDef:
        """
        Returns an array of reports.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.batch_get_reports)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#batch_get_reports)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#can_paginate)
        """

    async def create_project(
        self,
        *,
        name: str,
        source: "ProjectSourceTypeDef",
        artifacts: "ProjectArtifactsTypeDef",
        environment: "ProjectEnvironmentTypeDef",
        serviceRole: str,
        description: str = ...,
        secondarySources: Sequence["ProjectSourceTypeDef"] = ...,
        sourceVersion: str = ...,
        secondarySourceVersions: Sequence["ProjectSourceVersionTypeDef"] = ...,
        secondaryArtifacts: Sequence["ProjectArtifactsTypeDef"] = ...,
        cache: "ProjectCacheTypeDef" = ...,
        timeoutInMinutes: int = ...,
        queuedTimeoutInMinutes: int = ...,
        encryptionKey: str = ...,
        tags: Sequence["TagTypeDef"] = ...,
        vpcConfig: "VpcConfigTypeDef" = ...,
        badgeEnabled: bool = ...,
        logsConfig: "LogsConfigTypeDef" = ...,
        fileSystemLocations: Sequence["ProjectFileSystemLocationTypeDef"] = ...,
        buildBatchConfig: "ProjectBuildBatchConfigTypeDef" = ...,
        concurrentBuildLimit: int = ...
    ) -> CreateProjectOutputTypeDef:
        """
        Creates a build project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.create_project)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#create_project)
        """

    async def create_report_group(
        self,
        *,
        name: str,
        type: ReportTypeType,
        exportConfig: "ReportExportConfigTypeDef",
        tags: Sequence["TagTypeDef"] = ...
    ) -> CreateReportGroupOutputTypeDef:
        """
        Creates a report group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.create_report_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#create_report_group)
        """

    async def create_webhook(
        self,
        *,
        projectName: str,
        branchFilter: str = ...,
        filterGroups: Sequence[Sequence["WebhookFilterTypeDef"]] = ...,
        buildType: WebhookBuildTypeType = ...
    ) -> CreateWebhookOutputTypeDef:
        """
        For an existing CodeBuild build project that has its source code stored in a
        GitHub or Bitbucket repository, enables CodeBuild to start rebuilding the source
        code every time a code change is pushed to the repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.create_webhook)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#create_webhook)
        """

    async def delete_build_batch(self, *, id: str) -> DeleteBuildBatchOutputTypeDef:
        """
        Deletes a batch build.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.delete_build_batch)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#delete_build_batch)
        """

    async def delete_project(self, *, name: str) -> Dict[str, Any]:
        """
        Deletes a build project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.delete_project)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#delete_project)
        """

    async def delete_report(self, *, arn: str) -> Dict[str, Any]:
        """
        Deletes a report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.delete_report)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#delete_report)
        """

    async def delete_report_group(self, *, arn: str, deleteReports: bool = ...) -> Dict[str, Any]:
        """
        Deletes a report group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.delete_report_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#delete_report_group)
        """

    async def delete_resource_policy(self, *, resourceArn: str) -> Dict[str, Any]:
        """
        Deletes a resource policy that is identified by its resource ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.delete_resource_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#delete_resource_policy)
        """

    async def delete_source_credentials(self, *, arn: str) -> DeleteSourceCredentialsOutputTypeDef:
        """
        Deletes a set of GitHub, GitHub Enterprise, or Bitbucket source credentials.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.delete_source_credentials)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#delete_source_credentials)
        """

    async def delete_webhook(self, *, projectName: str) -> Dict[str, Any]:
        """
        For an existing CodeBuild build project that has its source code stored in a
        GitHub or Bitbucket repository, stops CodeBuild from rebuilding the source code
        every time a code change is pushed to the repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.delete_webhook)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#delete_webhook)
        """

    async def describe_code_coverages(
        self,
        *,
        reportArn: str,
        nextToken: str = ...,
        maxResults: int = ...,
        sortOrder: SortOrderTypeType = ...,
        sortBy: ReportCodeCoverageSortByTypeType = ...,
        minLineCoveragePercentage: float = ...,
        maxLineCoveragePercentage: float = ...
    ) -> DescribeCodeCoveragesOutputTypeDef:
        """
        Retrieves one or more code coverage reports.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.describe_code_coverages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#describe_code_coverages)
        """

    async def describe_test_cases(
        self,
        *,
        reportArn: str,
        nextToken: str = ...,
        maxResults: int = ...,
        filter: "TestCaseFilterTypeDef" = ...
    ) -> DescribeTestCasesOutputTypeDef:
        """
        Returns a list of details about test cases for a report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.describe_test_cases)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#describe_test_cases)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#generate_presigned_url)
        """

    async def get_report_group_trend(
        self,
        *,
        reportGroupArn: str,
        trendField: ReportGroupTrendFieldTypeType,
        numOfReports: int = ...
    ) -> GetReportGroupTrendOutputTypeDef:
        """
        Analyzes and accumulates test report values for the specified test reports.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.get_report_group_trend)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#get_report_group_trend)
        """

    async def get_resource_policy(self, *, resourceArn: str) -> GetResourcePolicyOutputTypeDef:
        """
        Gets a resource policy that is identified by its resource ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.get_resource_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#get_resource_policy)
        """

    async def import_source_credentials(
        self,
        *,
        token: str,
        serverType: ServerTypeType,
        authType: AuthTypeType,
        username: str = ...,
        shouldOverwrite: bool = ...
    ) -> ImportSourceCredentialsOutputTypeDef:
        """
        Imports the source repository credentials for an CodeBuild project that has its
        source code stored in a GitHub, GitHub Enterprise, or Bitbucket repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.import_source_credentials)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#import_source_credentials)
        """

    async def invalidate_project_cache(self, *, projectName: str) -> Dict[str, Any]:
        """
        Resets the cache for a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.invalidate_project_cache)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#invalidate_project_cache)
        """

    async def list_build_batches(
        self,
        *,
        filter: "BuildBatchFilterTypeDef" = ...,
        maxResults: int = ...,
        sortOrder: SortOrderTypeType = ...,
        nextToken: str = ...
    ) -> ListBuildBatchesOutputTypeDef:
        """
        Retrieves the identifiers of your build batches in the current region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.list_build_batches)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#list_build_batches)
        """

    async def list_build_batches_for_project(
        self,
        *,
        projectName: str = ...,
        filter: "BuildBatchFilterTypeDef" = ...,
        maxResults: int = ...,
        sortOrder: SortOrderTypeType = ...,
        nextToken: str = ...
    ) -> ListBuildBatchesForProjectOutputTypeDef:
        """
        Retrieves the identifiers of the build batches for a specific project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.list_build_batches_for_project)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#list_build_batches_for_project)
        """

    async def list_builds(
        self, *, sortOrder: SortOrderTypeType = ..., nextToken: str = ...
    ) -> ListBuildsOutputTypeDef:
        """
        Gets a list of build IDs, with each build ID representing a single build.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.list_builds)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#list_builds)
        """

    async def list_builds_for_project(
        self, *, projectName: str, sortOrder: SortOrderTypeType = ..., nextToken: str = ...
    ) -> ListBuildsForProjectOutputTypeDef:
        """
        Gets a list of build identifiers for the specified build project, with each
        build identifier representing a single build.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.list_builds_for_project)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#list_builds_for_project)
        """

    async def list_curated_environment_images(self) -> ListCuratedEnvironmentImagesOutputTypeDef:
        """
        Gets information about Docker images that are managed by CodeBuild.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.list_curated_environment_images)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#list_curated_environment_images)
        """

    async def list_projects(
        self,
        *,
        sortBy: ProjectSortByTypeType = ...,
        sortOrder: SortOrderTypeType = ...,
        nextToken: str = ...
    ) -> ListProjectsOutputTypeDef:
        """
        Gets a list of build project names, with each build project name representing a
        single build project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.list_projects)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#list_projects)
        """

    async def list_report_groups(
        self,
        *,
        sortOrder: SortOrderTypeType = ...,
        sortBy: ReportGroupSortByTypeType = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListReportGroupsOutputTypeDef:
        """
        Gets a list ARNs for the report groups in the current Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.list_report_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#list_report_groups)
        """

    async def list_reports(
        self,
        *,
        sortOrder: SortOrderTypeType = ...,
        nextToken: str = ...,
        maxResults: int = ...,
        filter: "ReportFilterTypeDef" = ...
    ) -> ListReportsOutputTypeDef:
        """
        Returns a list of ARNs for the reports in the current Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.list_reports)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#list_reports)
        """

    async def list_reports_for_report_group(
        self,
        *,
        reportGroupArn: str,
        nextToken: str = ...,
        sortOrder: SortOrderTypeType = ...,
        maxResults: int = ...,
        filter: "ReportFilterTypeDef" = ...
    ) -> ListReportsForReportGroupOutputTypeDef:
        """
        Returns a list of ARNs for the reports that belong to a `ReportGroup` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.list_reports_for_report_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#list_reports_for_report_group)
        """

    async def list_shared_projects(
        self,
        *,
        sortBy: SharedResourceSortByTypeType = ...,
        sortOrder: SortOrderTypeType = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListSharedProjectsOutputTypeDef:
        """
        Gets a list of projects that are shared with other Amazon Web Services accounts
        or users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.list_shared_projects)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#list_shared_projects)
        """

    async def list_shared_report_groups(
        self,
        *,
        sortOrder: SortOrderTypeType = ...,
        sortBy: SharedResourceSortByTypeType = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListSharedReportGroupsOutputTypeDef:
        """
        Gets a list of report groups that are shared with other Amazon Web Services
        accounts or users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.list_shared_report_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#list_shared_report_groups)
        """

    async def list_source_credentials(self) -> ListSourceCredentialsOutputTypeDef:
        """
        Returns a list of `SourceCredentialsInfo` objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.list_source_credentials)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#list_source_credentials)
        """

    async def put_resource_policy(
        self, *, policy: str, resourceArn: str
    ) -> PutResourcePolicyOutputTypeDef:
        """
        Stores a resource policy for the ARN of a `Project` or `ReportGroup` object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.put_resource_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#put_resource_policy)
        """

    async def retry_build(
        self, *, id: str = ..., idempotencyToken: str = ...
    ) -> RetryBuildOutputTypeDef:
        """
        Restarts a build.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.retry_build)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#retry_build)
        """

    async def retry_build_batch(
        self,
        *,
        id: str = ...,
        idempotencyToken: str = ...,
        retryType: RetryBuildBatchTypeType = ...
    ) -> RetryBuildBatchOutputTypeDef:
        """
        Restarts a failed batch build.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.retry_build_batch)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#retry_build_batch)
        """

    async def start_build(
        self,
        *,
        projectName: str,
        secondarySourcesOverride: Sequence["ProjectSourceTypeDef"] = ...,
        secondarySourcesVersionOverride: Sequence["ProjectSourceVersionTypeDef"] = ...,
        sourceVersion: str = ...,
        artifactsOverride: "ProjectArtifactsTypeDef" = ...,
        secondaryArtifactsOverride: Sequence["ProjectArtifactsTypeDef"] = ...,
        environmentVariablesOverride: Sequence["EnvironmentVariableTypeDef"] = ...,
        sourceTypeOverride: SourceTypeType = ...,
        sourceLocationOverride: str = ...,
        sourceAuthOverride: "SourceAuthTypeDef" = ...,
        gitCloneDepthOverride: int = ...,
        gitSubmodulesConfigOverride: "GitSubmodulesConfigTypeDef" = ...,
        buildspecOverride: str = ...,
        insecureSslOverride: bool = ...,
        reportBuildStatusOverride: bool = ...,
        buildStatusConfigOverride: "BuildStatusConfigTypeDef" = ...,
        environmentTypeOverride: EnvironmentTypeType = ...,
        imageOverride: str = ...,
        computeTypeOverride: ComputeTypeType = ...,
        certificateOverride: str = ...,
        cacheOverride: "ProjectCacheTypeDef" = ...,
        serviceRoleOverride: str = ...,
        privilegedModeOverride: bool = ...,
        timeoutInMinutesOverride: int = ...,
        queuedTimeoutInMinutesOverride: int = ...,
        encryptionKeyOverride: str = ...,
        idempotencyToken: str = ...,
        logsConfigOverride: "LogsConfigTypeDef" = ...,
        registryCredentialOverride: "RegistryCredentialTypeDef" = ...,
        imagePullCredentialsTypeOverride: ImagePullCredentialsTypeType = ...,
        debugSessionEnabled: bool = ...
    ) -> StartBuildOutputTypeDef:
        """
        Starts running a build.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.start_build)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#start_build)
        """

    async def start_build_batch(
        self,
        *,
        projectName: str,
        secondarySourcesOverride: Sequence["ProjectSourceTypeDef"] = ...,
        secondarySourcesVersionOverride: Sequence["ProjectSourceVersionTypeDef"] = ...,
        sourceVersion: str = ...,
        artifactsOverride: "ProjectArtifactsTypeDef" = ...,
        secondaryArtifactsOverride: Sequence["ProjectArtifactsTypeDef"] = ...,
        environmentVariablesOverride: Sequence["EnvironmentVariableTypeDef"] = ...,
        sourceTypeOverride: SourceTypeType = ...,
        sourceLocationOverride: str = ...,
        sourceAuthOverride: "SourceAuthTypeDef" = ...,
        gitCloneDepthOverride: int = ...,
        gitSubmodulesConfigOverride: "GitSubmodulesConfigTypeDef" = ...,
        buildspecOverride: str = ...,
        insecureSslOverride: bool = ...,
        reportBuildBatchStatusOverride: bool = ...,
        environmentTypeOverride: EnvironmentTypeType = ...,
        imageOverride: str = ...,
        computeTypeOverride: ComputeTypeType = ...,
        certificateOverride: str = ...,
        cacheOverride: "ProjectCacheTypeDef" = ...,
        serviceRoleOverride: str = ...,
        privilegedModeOverride: bool = ...,
        buildTimeoutInMinutesOverride: int = ...,
        queuedTimeoutInMinutesOverride: int = ...,
        encryptionKeyOverride: str = ...,
        idempotencyToken: str = ...,
        logsConfigOverride: "LogsConfigTypeDef" = ...,
        registryCredentialOverride: "RegistryCredentialTypeDef" = ...,
        imagePullCredentialsTypeOverride: ImagePullCredentialsTypeType = ...,
        buildBatchConfigOverride: "ProjectBuildBatchConfigTypeDef" = ...,
        debugSessionEnabled: bool = ...
    ) -> StartBuildBatchOutputTypeDef:
        """
        Starts a batch build for a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.start_build_batch)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#start_build_batch)
        """

    async def stop_build(self, *, id: str) -> StopBuildOutputTypeDef:
        """
        Attempts to stop running a build.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.stop_build)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#stop_build)
        """

    async def stop_build_batch(self, *, id: str) -> StopBuildBatchOutputTypeDef:
        """
        Stops a running batch build.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.stop_build_batch)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#stop_build_batch)
        """

    async def update_project(
        self,
        *,
        name: str,
        description: str = ...,
        source: "ProjectSourceTypeDef" = ...,
        secondarySources: Sequence["ProjectSourceTypeDef"] = ...,
        sourceVersion: str = ...,
        secondarySourceVersions: Sequence["ProjectSourceVersionTypeDef"] = ...,
        artifacts: "ProjectArtifactsTypeDef" = ...,
        secondaryArtifacts: Sequence["ProjectArtifactsTypeDef"] = ...,
        cache: "ProjectCacheTypeDef" = ...,
        environment: "ProjectEnvironmentTypeDef" = ...,
        serviceRole: str = ...,
        timeoutInMinutes: int = ...,
        queuedTimeoutInMinutes: int = ...,
        encryptionKey: str = ...,
        tags: Sequence["TagTypeDef"] = ...,
        vpcConfig: "VpcConfigTypeDef" = ...,
        badgeEnabled: bool = ...,
        logsConfig: "LogsConfigTypeDef" = ...,
        fileSystemLocations: Sequence["ProjectFileSystemLocationTypeDef"] = ...,
        buildBatchConfig: "ProjectBuildBatchConfigTypeDef" = ...,
        concurrentBuildLimit: int = ...
    ) -> UpdateProjectOutputTypeDef:
        """
        Changes the settings of a build project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.update_project)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#update_project)
        """

    async def update_project_visibility(
        self,
        *,
        projectArn: str,
        projectVisibility: ProjectVisibilityTypeType,
        resourceAccessRole: str = ...
    ) -> UpdateProjectVisibilityOutputTypeDef:
        """
        Changes the public visibility for a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.update_project_visibility)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#update_project_visibility)
        """

    async def update_report_group(
        self,
        *,
        arn: str,
        exportConfig: "ReportExportConfigTypeDef" = ...,
        tags: Sequence["TagTypeDef"] = ...
    ) -> UpdateReportGroupOutputTypeDef:
        """
        Updates a report group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.update_report_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#update_report_group)
        """

    async def update_webhook(
        self,
        *,
        projectName: str,
        branchFilter: str = ...,
        rotateSecret: bool = ...,
        filterGroups: Sequence[Sequence["WebhookFilterTypeDef"]] = ...,
        buildType: WebhookBuildTypeType = ...
    ) -> UpdateWebhookOutputTypeDef:
        """
        Updates the webhook associated with an CodeBuild build project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.update_webhook)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#update_webhook)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_code_coverages"]
    ) -> DescribeCodeCoveragesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_test_cases"]
    ) -> DescribeTestCasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_build_batches"]
    ) -> ListBuildBatchesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_build_batches_for_project"]
    ) -> ListBuildBatchesForProjectPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_builds"]) -> ListBuildsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_builds_for_project"]
    ) -> ListBuildsForProjectPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_projects"]) -> ListProjectsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_report_groups"]
    ) -> ListReportGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_reports"]) -> ListReportsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_reports_for_report_group"]
    ) -> ListReportsForReportGroupPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_shared_projects"]
    ) -> ListSharedProjectsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_shared_report_groups"]
    ) -> ListSharedReportGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#get_paginator)
        """

    async def __aenter__(self) -> "CodeBuildClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/)
        """
