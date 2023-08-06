"""
Type annotations for codebuild service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_codebuild.client import CodeBuildClient
    from types_aiobotocore_codebuild.paginator import (
        DescribeCodeCoveragesPaginator,
        DescribeTestCasesPaginator,
        ListBuildBatchesPaginator,
        ListBuildBatchesForProjectPaginator,
        ListBuildsPaginator,
        ListBuildsForProjectPaginator,
        ListProjectsPaginator,
        ListReportGroupsPaginator,
        ListReportsPaginator,
        ListReportsForReportGroupPaginator,
        ListSharedProjectsPaginator,
        ListSharedReportGroupsPaginator,
    )

    session = get_session()
    with session.create_client("codebuild") as client:
        client: CodeBuildClient

        describe_code_coverages_paginator: DescribeCodeCoveragesPaginator = client.get_paginator("describe_code_coverages")
        describe_test_cases_paginator: DescribeTestCasesPaginator = client.get_paginator("describe_test_cases")
        list_build_batches_paginator: ListBuildBatchesPaginator = client.get_paginator("list_build_batches")
        list_build_batches_for_project_paginator: ListBuildBatchesForProjectPaginator = client.get_paginator("list_build_batches_for_project")
        list_builds_paginator: ListBuildsPaginator = client.get_paginator("list_builds")
        list_builds_for_project_paginator: ListBuildsForProjectPaginator = client.get_paginator("list_builds_for_project")
        list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
        list_report_groups_paginator: ListReportGroupsPaginator = client.get_paginator("list_report_groups")
        list_reports_paginator: ListReportsPaginator = client.get_paginator("list_reports")
        list_reports_for_report_group_paginator: ListReportsForReportGroupPaginator = client.get_paginator("list_reports_for_report_group")
        list_shared_projects_paginator: ListSharedProjectsPaginator = client.get_paginator("list_shared_projects")
        list_shared_report_groups_paginator: ListSharedReportGroupsPaginator = client.get_paginator("list_shared_report_groups")
    ```
"""
import sys
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import (
    ProjectSortByTypeType,
    ReportCodeCoverageSortByTypeType,
    ReportGroupSortByTypeType,
    SharedResourceSortByTypeType,
    SortOrderTypeType,
)
from .type_defs import (
    BuildBatchFilterTypeDef,
    DescribeCodeCoveragesOutputTypeDef,
    DescribeTestCasesOutputTypeDef,
    ListBuildBatchesForProjectOutputTypeDef,
    ListBuildBatchesOutputTypeDef,
    ListBuildsForProjectOutputTypeDef,
    ListBuildsOutputTypeDef,
    ListProjectsOutputTypeDef,
    ListReportGroupsOutputTypeDef,
    ListReportsForReportGroupOutputTypeDef,
    ListReportsOutputTypeDef,
    ListSharedProjectsOutputTypeDef,
    ListSharedReportGroupsOutputTypeDef,
    PaginatorConfigTypeDef,
    ReportFilterTypeDef,
    TestCaseFilterTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator

__all__ = (
    "DescribeCodeCoveragesPaginator",
    "DescribeTestCasesPaginator",
    "ListBuildBatchesPaginator",
    "ListBuildBatchesForProjectPaginator",
    "ListBuildsPaginator",
    "ListBuildsForProjectPaginator",
    "ListProjectsPaginator",
    "ListReportGroupsPaginator",
    "ListReportsPaginator",
    "ListReportsForReportGroupPaginator",
    "ListSharedProjectsPaginator",
    "ListSharedReportGroupsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeCodeCoveragesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Paginator.DescribeCodeCoverages)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#describecodecoveragespaginator)
    """

    def paginate(
        self,
        *,
        reportArn: str,
        sortOrder: SortOrderTypeType = ...,
        sortBy: ReportCodeCoverageSortByTypeType = ...,
        minLineCoveragePercentage: float = ...,
        maxLineCoveragePercentage: float = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeCodeCoveragesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Paginator.DescribeCodeCoverages.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#describecodecoveragespaginator)
        """

class DescribeTestCasesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Paginator.DescribeTestCases)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#describetestcasespaginator)
    """

    def paginate(
        self,
        *,
        reportArn: str,
        filter: "TestCaseFilterTypeDef" = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeTestCasesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Paginator.DescribeTestCases.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#describetestcasespaginator)
        """

class ListBuildBatchesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Paginator.ListBuildBatches)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listbuildbatchespaginator)
    """

    def paginate(
        self,
        *,
        filter: "BuildBatchFilterTypeDef" = ...,
        sortOrder: SortOrderTypeType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListBuildBatchesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Paginator.ListBuildBatches.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listbuildbatchespaginator)
        """

class ListBuildBatchesForProjectPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Paginator.ListBuildBatchesForProject)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listbuildbatchesforprojectpaginator)
    """

    def paginate(
        self,
        *,
        projectName: str = ...,
        filter: "BuildBatchFilterTypeDef" = ...,
        sortOrder: SortOrderTypeType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListBuildBatchesForProjectOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Paginator.ListBuildBatchesForProject.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listbuildbatchesforprojectpaginator)
        """

class ListBuildsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Paginator.ListBuilds)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listbuildspaginator)
    """

    def paginate(
        self,
        *,
        sortOrder: SortOrderTypeType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListBuildsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Paginator.ListBuilds.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listbuildspaginator)
        """

class ListBuildsForProjectPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Paginator.ListBuildsForProject)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listbuildsforprojectpaginator)
    """

    def paginate(
        self,
        *,
        projectName: str,
        sortOrder: SortOrderTypeType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListBuildsForProjectOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Paginator.ListBuildsForProject.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listbuildsforprojectpaginator)
        """

class ListProjectsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Paginator.ListProjects)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listprojectspaginator)
    """

    def paginate(
        self,
        *,
        sortBy: ProjectSortByTypeType = ...,
        sortOrder: SortOrderTypeType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListProjectsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Paginator.ListProjects.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listprojectspaginator)
        """

class ListReportGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Paginator.ListReportGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listreportgroupspaginator)
    """

    def paginate(
        self,
        *,
        sortOrder: SortOrderTypeType = ...,
        sortBy: ReportGroupSortByTypeType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListReportGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Paginator.ListReportGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listreportgroupspaginator)
        """

class ListReportsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Paginator.ListReports)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listreportspaginator)
    """

    def paginate(
        self,
        *,
        sortOrder: SortOrderTypeType = ...,
        filter: "ReportFilterTypeDef" = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListReportsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Paginator.ListReports.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listreportspaginator)
        """

class ListReportsForReportGroupPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Paginator.ListReportsForReportGroup)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listreportsforreportgrouppaginator)
    """

    def paginate(
        self,
        *,
        reportGroupArn: str,
        sortOrder: SortOrderTypeType = ...,
        filter: "ReportFilterTypeDef" = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListReportsForReportGroupOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Paginator.ListReportsForReportGroup.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listreportsforreportgrouppaginator)
        """

class ListSharedProjectsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Paginator.ListSharedProjects)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listsharedprojectspaginator)
    """

    def paginate(
        self,
        *,
        sortBy: SharedResourceSortByTypeType = ...,
        sortOrder: SortOrderTypeType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListSharedProjectsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Paginator.ListSharedProjects.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listsharedprojectspaginator)
        """

class ListSharedReportGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Paginator.ListSharedReportGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listsharedreportgroupspaginator)
    """

    def paginate(
        self,
        *,
        sortOrder: SortOrderTypeType = ...,
        sortBy: SharedResourceSortByTypeType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListSharedReportGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Paginator.ListSharedReportGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listsharedreportgroupspaginator)
        """
