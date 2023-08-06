"""
Type annotations for mobile service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mobile/type_defs/)

Usage::

    ```python
    from mypy_boto3_mobile.type_defs import BundleDetailsTypeDef

    data: BundleDetailsTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Union

from botocore.response import StreamingBody

from .literals import PlatformType, ProjectStateType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "BundleDetailsTypeDef",
    "CreateProjectRequestRequestTypeDef",
    "CreateProjectResultTypeDef",
    "DeleteProjectRequestRequestTypeDef",
    "DeleteProjectResultTypeDef",
    "DescribeBundleRequestRequestTypeDef",
    "DescribeBundleResultTypeDef",
    "DescribeProjectRequestRequestTypeDef",
    "DescribeProjectResultTypeDef",
    "ExportBundleRequestRequestTypeDef",
    "ExportBundleResultTypeDef",
    "ExportProjectRequestRequestTypeDef",
    "ExportProjectResultTypeDef",
    "ListBundlesRequestListBundlesPaginateTypeDef",
    "ListBundlesRequestRequestTypeDef",
    "ListBundlesResultTypeDef",
    "ListProjectsRequestListProjectsPaginateTypeDef",
    "ListProjectsRequestRequestTypeDef",
    "ListProjectsResultTypeDef",
    "PaginatorConfigTypeDef",
    "ProjectDetailsTypeDef",
    "ProjectSummaryTypeDef",
    "ResourceTypeDef",
    "ResponseMetadataTypeDef",
    "UpdateProjectRequestRequestTypeDef",
    "UpdateProjectResultTypeDef",
)

BundleDetailsTypeDef = TypedDict(
    "BundleDetailsTypeDef",
    {
        "bundleId": str,
        "title": str,
        "version": str,
        "description": str,
        "iconUrl": str,
        "availablePlatforms": List[PlatformType],
    },
    total=False,
)

CreateProjectRequestRequestTypeDef = TypedDict(
    "CreateProjectRequestRequestTypeDef",
    {
        "name": str,
        "region": str,
        "contents": Union[str, bytes, IO[Any], StreamingBody],
        "snapshotId": str,
    },
    total=False,
)

CreateProjectResultTypeDef = TypedDict(
    "CreateProjectResultTypeDef",
    {
        "details": "ProjectDetailsTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteProjectRequestRequestTypeDef = TypedDict(
    "DeleteProjectRequestRequestTypeDef",
    {
        "projectId": str,
    },
)

DeleteProjectResultTypeDef = TypedDict(
    "DeleteProjectResultTypeDef",
    {
        "deletedResources": List["ResourceTypeDef"],
        "orphanedResources": List["ResourceTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeBundleRequestRequestTypeDef = TypedDict(
    "DescribeBundleRequestRequestTypeDef",
    {
        "bundleId": str,
    },
)

DescribeBundleResultTypeDef = TypedDict(
    "DescribeBundleResultTypeDef",
    {
        "details": "BundleDetailsTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDescribeProjectRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeProjectRequestRequestTypeDef",
    {
        "projectId": str,
    },
)
_OptionalDescribeProjectRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeProjectRequestRequestTypeDef",
    {
        "syncFromResources": bool,
    },
    total=False,
)


class DescribeProjectRequestRequestTypeDef(
    _RequiredDescribeProjectRequestRequestTypeDef, _OptionalDescribeProjectRequestRequestTypeDef
):
    pass


DescribeProjectResultTypeDef = TypedDict(
    "DescribeProjectResultTypeDef",
    {
        "details": "ProjectDetailsTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredExportBundleRequestRequestTypeDef = TypedDict(
    "_RequiredExportBundleRequestRequestTypeDef",
    {
        "bundleId": str,
    },
)
_OptionalExportBundleRequestRequestTypeDef = TypedDict(
    "_OptionalExportBundleRequestRequestTypeDef",
    {
        "projectId": str,
        "platform": PlatformType,
    },
    total=False,
)


class ExportBundleRequestRequestTypeDef(
    _RequiredExportBundleRequestRequestTypeDef, _OptionalExportBundleRequestRequestTypeDef
):
    pass


ExportBundleResultTypeDef = TypedDict(
    "ExportBundleResultTypeDef",
    {
        "downloadUrl": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ExportProjectRequestRequestTypeDef = TypedDict(
    "ExportProjectRequestRequestTypeDef",
    {
        "projectId": str,
    },
)

ExportProjectResultTypeDef = TypedDict(
    "ExportProjectResultTypeDef",
    {
        "downloadUrl": str,
        "shareUrl": str,
        "snapshotId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListBundlesRequestListBundlesPaginateTypeDef = TypedDict(
    "ListBundlesRequestListBundlesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListBundlesRequestRequestTypeDef = TypedDict(
    "ListBundlesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListBundlesResultTypeDef = TypedDict(
    "ListBundlesResultTypeDef",
    {
        "bundleList": List["BundleDetailsTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListProjectsRequestListProjectsPaginateTypeDef = TypedDict(
    "ListProjectsRequestListProjectsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListProjectsRequestRequestTypeDef = TypedDict(
    "ListProjectsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListProjectsResultTypeDef = TypedDict(
    "ListProjectsResultTypeDef",
    {
        "projects": List["ProjectSummaryTypeDef"],
        "nextToken": str,
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

ProjectDetailsTypeDef = TypedDict(
    "ProjectDetailsTypeDef",
    {
        "name": str,
        "projectId": str,
        "region": str,
        "state": ProjectStateType,
        "createdDate": datetime,
        "lastUpdatedDate": datetime,
        "consoleUrl": str,
        "resources": List["ResourceTypeDef"],
    },
    total=False,
)

ProjectSummaryTypeDef = TypedDict(
    "ProjectSummaryTypeDef",
    {
        "name": str,
        "projectId": str,
    },
    total=False,
)

ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "type": str,
        "name": str,
        "arn": str,
        "feature": str,
        "attributes": Dict[str, str],
    },
    total=False,
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

_RequiredUpdateProjectRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateProjectRequestRequestTypeDef",
    {
        "projectId": str,
    },
)
_OptionalUpdateProjectRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateProjectRequestRequestTypeDef",
    {
        "contents": Union[str, bytes, IO[Any], StreamingBody],
    },
    total=False,
)


class UpdateProjectRequestRequestTypeDef(
    _RequiredUpdateProjectRequestRequestTypeDef, _OptionalUpdateProjectRequestRequestTypeDef
):
    pass


UpdateProjectResultTypeDef = TypedDict(
    "UpdateProjectResultTypeDef",
    {
        "details": "ProjectDetailsTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
