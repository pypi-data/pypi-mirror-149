"""
Type annotations for inspector2 service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/type_defs/)

Usage::

    ```python
    from mypy_boto3_inspector2.type_defs import AccountAggregationResponseTypeDef

    data: AccountAggregationResponseTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AccountSortByType,
    AggregationFindingTypeType,
    AggregationResourceTypeType,
    AggregationTypeType,
    AmiSortByType,
    AwsEcrContainerSortByType,
    CoverageResourceTypeType,
    CoverageStringComparisonType,
    DelegatedAdminStatusType,
    Ec2InstanceSortByType,
    Ec2PlatformType,
    EcrScanFrequencyType,
    ErrorCodeType,
    ExternalReportStatusType,
    FilterActionType,
    FindingStatusType,
    FindingTypeSortByType,
    FindingTypeType,
    FreeTrialInfoErrorCodeType,
    FreeTrialStatusType,
    FreeTrialTypeType,
    GroupKeyType,
    ImageLayerSortByType,
    NetworkProtocolType,
    OperationType,
    PackageManagerType,
    PackageSortByType,
    RelationshipStatusType,
    ReportFormatType,
    ReportingErrorCodeType,
    RepositorySortByType,
    ResourceScanTypeType,
    ResourceTypeType,
    ScanStatusCodeType,
    ScanStatusReasonType,
    ScanTypeType,
    ServiceType,
    SeverityType,
    SortFieldType,
    SortOrderType,
    StatusType,
    StringComparisonType,
    TitleSortByType,
    UsageTypeType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AccountAggregationResponseTypeDef",
    "AccountAggregationTypeDef",
    "AccountStateTypeDef",
    "AccountTypeDef",
    "AggregationRequestTypeDef",
    "AggregationResponseTypeDef",
    "AmiAggregationResponseTypeDef",
    "AmiAggregationTypeDef",
    "AssociateMemberRequestRequestTypeDef",
    "AssociateMemberResponseTypeDef",
    "AutoEnableTypeDef",
    "AwsEc2InstanceDetailsTypeDef",
    "AwsEcrContainerAggregationResponseTypeDef",
    "AwsEcrContainerAggregationTypeDef",
    "AwsEcrContainerImageDetailsTypeDef",
    "BatchGetAccountStatusRequestRequestTypeDef",
    "BatchGetAccountStatusResponseTypeDef",
    "BatchGetFreeTrialInfoRequestRequestTypeDef",
    "BatchGetFreeTrialInfoResponseTypeDef",
    "CancelFindingsReportRequestRequestTypeDef",
    "CancelFindingsReportResponseTypeDef",
    "CountsTypeDef",
    "CoverageFilterCriteriaTypeDef",
    "CoverageMapFilterTypeDef",
    "CoverageStringFilterTypeDef",
    "CoveredResourceTypeDef",
    "CreateFilterRequestRequestTypeDef",
    "CreateFilterResponseTypeDef",
    "CreateFindingsReportRequestRequestTypeDef",
    "CreateFindingsReportResponseTypeDef",
    "CvssScoreAdjustmentTypeDef",
    "CvssScoreDetailsTypeDef",
    "CvssScoreTypeDef",
    "DateFilterTypeDef",
    "DelegatedAdminAccountTypeDef",
    "DelegatedAdminTypeDef",
    "DeleteFilterRequestRequestTypeDef",
    "DeleteFilterResponseTypeDef",
    "DescribeOrganizationConfigurationResponseTypeDef",
    "DestinationTypeDef",
    "DisableDelegatedAdminAccountRequestRequestTypeDef",
    "DisableDelegatedAdminAccountResponseTypeDef",
    "DisableRequestRequestTypeDef",
    "DisableResponseTypeDef",
    "DisassociateMemberRequestRequestTypeDef",
    "DisassociateMemberResponseTypeDef",
    "Ec2InstanceAggregationResponseTypeDef",
    "Ec2InstanceAggregationTypeDef",
    "Ec2MetadataTypeDef",
    "EcrContainerImageMetadataTypeDef",
    "EcrRepositoryMetadataTypeDef",
    "EnableDelegatedAdminAccountRequestRequestTypeDef",
    "EnableDelegatedAdminAccountResponseTypeDef",
    "EnableRequestRequestTypeDef",
    "EnableResponseTypeDef",
    "FailedAccountTypeDef",
    "FilterCriteriaTypeDef",
    "FilterTypeDef",
    "FindingTypeAggregationResponseTypeDef",
    "FindingTypeAggregationTypeDef",
    "FindingTypeDef",
    "FreeTrialAccountInfoTypeDef",
    "FreeTrialInfoErrorTypeDef",
    "FreeTrialInfoTypeDef",
    "GetDelegatedAdminAccountResponseTypeDef",
    "GetFindingsReportStatusRequestRequestTypeDef",
    "GetFindingsReportStatusResponseTypeDef",
    "GetMemberRequestRequestTypeDef",
    "GetMemberResponseTypeDef",
    "ImageLayerAggregationResponseTypeDef",
    "ImageLayerAggregationTypeDef",
    "InspectorScoreDetailsTypeDef",
    "ListAccountPermissionsRequestListAccountPermissionsPaginateTypeDef",
    "ListAccountPermissionsRequestRequestTypeDef",
    "ListAccountPermissionsResponseTypeDef",
    "ListCoverageRequestListCoveragePaginateTypeDef",
    "ListCoverageRequestRequestTypeDef",
    "ListCoverageResponseTypeDef",
    "ListCoverageStatisticsRequestListCoverageStatisticsPaginateTypeDef",
    "ListCoverageStatisticsRequestRequestTypeDef",
    "ListCoverageStatisticsResponseTypeDef",
    "ListDelegatedAdminAccountsRequestListDelegatedAdminAccountsPaginateTypeDef",
    "ListDelegatedAdminAccountsRequestRequestTypeDef",
    "ListDelegatedAdminAccountsResponseTypeDef",
    "ListFiltersRequestListFiltersPaginateTypeDef",
    "ListFiltersRequestRequestTypeDef",
    "ListFiltersResponseTypeDef",
    "ListFindingAggregationsRequestListFindingAggregationsPaginateTypeDef",
    "ListFindingAggregationsRequestRequestTypeDef",
    "ListFindingAggregationsResponseTypeDef",
    "ListFindingsRequestListFindingsPaginateTypeDef",
    "ListFindingsRequestRequestTypeDef",
    "ListFindingsResponseTypeDef",
    "ListMembersRequestListMembersPaginateTypeDef",
    "ListMembersRequestRequestTypeDef",
    "ListMembersResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListUsageTotalsRequestListUsageTotalsPaginateTypeDef",
    "ListUsageTotalsRequestRequestTypeDef",
    "ListUsageTotalsResponseTypeDef",
    "MapFilterTypeDef",
    "MemberTypeDef",
    "NetworkPathTypeDef",
    "NetworkReachabilityDetailsTypeDef",
    "NumberFilterTypeDef",
    "PackageAggregationResponseTypeDef",
    "PackageAggregationTypeDef",
    "PackageFilterTypeDef",
    "PackageVulnerabilityDetailsTypeDef",
    "PaginatorConfigTypeDef",
    "PermissionTypeDef",
    "PortRangeFilterTypeDef",
    "PortRangeTypeDef",
    "RecommendationTypeDef",
    "RemediationTypeDef",
    "RepositoryAggregationResponseTypeDef",
    "RepositoryAggregationTypeDef",
    "ResourceDetailsTypeDef",
    "ResourceScanMetadataTypeDef",
    "ResourceStateTypeDef",
    "ResourceStatusTypeDef",
    "ResourceTypeDef",
    "ResponseMetadataTypeDef",
    "ScanStatusTypeDef",
    "SeverityCountsTypeDef",
    "SortCriteriaTypeDef",
    "StateTypeDef",
    "StepTypeDef",
    "StringFilterTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TitleAggregationResponseTypeDef",
    "TitleAggregationTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateFilterRequestRequestTypeDef",
    "UpdateFilterResponseTypeDef",
    "UpdateOrganizationConfigurationRequestRequestTypeDef",
    "UpdateOrganizationConfigurationResponseTypeDef",
    "UsageTotalTypeDef",
    "UsageTypeDef",
    "VulnerablePackageTypeDef",
)

AccountAggregationResponseTypeDef = TypedDict(
    "AccountAggregationResponseTypeDef",
    {
        "accountId": str,
        "severityCounts": "SeverityCountsTypeDef",
    },
    total=False,
)

AccountAggregationTypeDef = TypedDict(
    "AccountAggregationTypeDef",
    {
        "findingType": AggregationFindingTypeType,
        "resourceType": AggregationResourceTypeType,
        "sortBy": AccountSortByType,
        "sortOrder": SortOrderType,
    },
    total=False,
)

AccountStateTypeDef = TypedDict(
    "AccountStateTypeDef",
    {
        "accountId": str,
        "resourceState": "ResourceStateTypeDef",
        "state": "StateTypeDef",
    },
)

AccountTypeDef = TypedDict(
    "AccountTypeDef",
    {
        "accountId": str,
        "resourceStatus": "ResourceStatusTypeDef",
        "status": StatusType,
    },
)

AggregationRequestTypeDef = TypedDict(
    "AggregationRequestTypeDef",
    {
        "accountAggregation": "AccountAggregationTypeDef",
        "amiAggregation": "AmiAggregationTypeDef",
        "awsEcrContainerAggregation": "AwsEcrContainerAggregationTypeDef",
        "ec2InstanceAggregation": "Ec2InstanceAggregationTypeDef",
        "findingTypeAggregation": "FindingTypeAggregationTypeDef",
        "imageLayerAggregation": "ImageLayerAggregationTypeDef",
        "packageAggregation": "PackageAggregationTypeDef",
        "repositoryAggregation": "RepositoryAggregationTypeDef",
        "titleAggregation": "TitleAggregationTypeDef",
    },
    total=False,
)

AggregationResponseTypeDef = TypedDict(
    "AggregationResponseTypeDef",
    {
        "accountAggregation": "AccountAggregationResponseTypeDef",
        "amiAggregation": "AmiAggregationResponseTypeDef",
        "awsEcrContainerAggregation": "AwsEcrContainerAggregationResponseTypeDef",
        "ec2InstanceAggregation": "Ec2InstanceAggregationResponseTypeDef",
        "findingTypeAggregation": "FindingTypeAggregationResponseTypeDef",
        "imageLayerAggregation": "ImageLayerAggregationResponseTypeDef",
        "packageAggregation": "PackageAggregationResponseTypeDef",
        "repositoryAggregation": "RepositoryAggregationResponseTypeDef",
        "titleAggregation": "TitleAggregationResponseTypeDef",
    },
    total=False,
)

_RequiredAmiAggregationResponseTypeDef = TypedDict(
    "_RequiredAmiAggregationResponseTypeDef",
    {
        "ami": str,
    },
)
_OptionalAmiAggregationResponseTypeDef = TypedDict(
    "_OptionalAmiAggregationResponseTypeDef",
    {
        "accountId": str,
        "affectedInstances": int,
        "severityCounts": "SeverityCountsTypeDef",
    },
    total=False,
)


class AmiAggregationResponseTypeDef(
    _RequiredAmiAggregationResponseTypeDef, _OptionalAmiAggregationResponseTypeDef
):
    pass


AmiAggregationTypeDef = TypedDict(
    "AmiAggregationTypeDef",
    {
        "amis": Sequence["StringFilterTypeDef"],
        "sortBy": AmiSortByType,
        "sortOrder": SortOrderType,
    },
    total=False,
)

AssociateMemberRequestRequestTypeDef = TypedDict(
    "AssociateMemberRequestRequestTypeDef",
    {
        "accountId": str,
    },
)

AssociateMemberResponseTypeDef = TypedDict(
    "AssociateMemberResponseTypeDef",
    {
        "accountId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AutoEnableTypeDef = TypedDict(
    "AutoEnableTypeDef",
    {
        "ec2": bool,
        "ecr": bool,
    },
)

AwsEc2InstanceDetailsTypeDef = TypedDict(
    "AwsEc2InstanceDetailsTypeDef",
    {
        "iamInstanceProfileArn": str,
        "imageId": str,
        "ipV4Addresses": List[str],
        "ipV6Addresses": List[str],
        "keyName": str,
        "launchedAt": datetime,
        "platform": str,
        "subnetId": str,
        "type": str,
        "vpcId": str,
    },
    total=False,
)

_RequiredAwsEcrContainerAggregationResponseTypeDef = TypedDict(
    "_RequiredAwsEcrContainerAggregationResponseTypeDef",
    {
        "resourceId": str,
    },
)
_OptionalAwsEcrContainerAggregationResponseTypeDef = TypedDict(
    "_OptionalAwsEcrContainerAggregationResponseTypeDef",
    {
        "accountId": str,
        "architecture": str,
        "imageSha": str,
        "imageTags": List[str],
        "repository": str,
        "severityCounts": "SeverityCountsTypeDef",
    },
    total=False,
)


class AwsEcrContainerAggregationResponseTypeDef(
    _RequiredAwsEcrContainerAggregationResponseTypeDef,
    _OptionalAwsEcrContainerAggregationResponseTypeDef,
):
    pass


AwsEcrContainerAggregationTypeDef = TypedDict(
    "AwsEcrContainerAggregationTypeDef",
    {
        "architectures": Sequence["StringFilterTypeDef"],
        "imageShas": Sequence["StringFilterTypeDef"],
        "imageTags": Sequence["StringFilterTypeDef"],
        "repositories": Sequence["StringFilterTypeDef"],
        "resourceIds": Sequence["StringFilterTypeDef"],
        "sortBy": AwsEcrContainerSortByType,
        "sortOrder": SortOrderType,
    },
    total=False,
)

_RequiredAwsEcrContainerImageDetailsTypeDef = TypedDict(
    "_RequiredAwsEcrContainerImageDetailsTypeDef",
    {
        "imageHash": str,
        "registry": str,
        "repositoryName": str,
    },
)
_OptionalAwsEcrContainerImageDetailsTypeDef = TypedDict(
    "_OptionalAwsEcrContainerImageDetailsTypeDef",
    {
        "architecture": str,
        "author": str,
        "imageTags": List[str],
        "platform": str,
        "pushedAt": datetime,
    },
    total=False,
)


class AwsEcrContainerImageDetailsTypeDef(
    _RequiredAwsEcrContainerImageDetailsTypeDef, _OptionalAwsEcrContainerImageDetailsTypeDef
):
    pass


BatchGetAccountStatusRequestRequestTypeDef = TypedDict(
    "BatchGetAccountStatusRequestRequestTypeDef",
    {
        "accountIds": Sequence[str],
    },
    total=False,
)

BatchGetAccountStatusResponseTypeDef = TypedDict(
    "BatchGetAccountStatusResponseTypeDef",
    {
        "accounts": List["AccountStateTypeDef"],
        "failedAccounts": List["FailedAccountTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

BatchGetFreeTrialInfoRequestRequestTypeDef = TypedDict(
    "BatchGetFreeTrialInfoRequestRequestTypeDef",
    {
        "accountIds": Sequence[str],
    },
)

BatchGetFreeTrialInfoResponseTypeDef = TypedDict(
    "BatchGetFreeTrialInfoResponseTypeDef",
    {
        "accounts": List["FreeTrialAccountInfoTypeDef"],
        "failedAccounts": List["FreeTrialInfoErrorTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CancelFindingsReportRequestRequestTypeDef = TypedDict(
    "CancelFindingsReportRequestRequestTypeDef",
    {
        "reportId": str,
    },
)

CancelFindingsReportResponseTypeDef = TypedDict(
    "CancelFindingsReportResponseTypeDef",
    {
        "reportId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CountsTypeDef = TypedDict(
    "CountsTypeDef",
    {
        "count": int,
        "groupKey": GroupKeyType,
    },
    total=False,
)

CoverageFilterCriteriaTypeDef = TypedDict(
    "CoverageFilterCriteriaTypeDef",
    {
        "accountId": Sequence["CoverageStringFilterTypeDef"],
        "ec2InstanceTags": Sequence["CoverageMapFilterTypeDef"],
        "ecrImageTags": Sequence["CoverageStringFilterTypeDef"],
        "ecrRepositoryName": Sequence["CoverageStringFilterTypeDef"],
        "resourceId": Sequence["CoverageStringFilterTypeDef"],
        "resourceType": Sequence["CoverageStringFilterTypeDef"],
        "scanStatusCode": Sequence["CoverageStringFilterTypeDef"],
        "scanStatusReason": Sequence["CoverageStringFilterTypeDef"],
        "scanType": Sequence["CoverageStringFilterTypeDef"],
    },
    total=False,
)

_RequiredCoverageMapFilterTypeDef = TypedDict(
    "_RequiredCoverageMapFilterTypeDef",
    {
        "comparison": Literal["EQUALS"],
        "key": str,
    },
)
_OptionalCoverageMapFilterTypeDef = TypedDict(
    "_OptionalCoverageMapFilterTypeDef",
    {
        "value": str,
    },
    total=False,
)


class CoverageMapFilterTypeDef(
    _RequiredCoverageMapFilterTypeDef, _OptionalCoverageMapFilterTypeDef
):
    pass


CoverageStringFilterTypeDef = TypedDict(
    "CoverageStringFilterTypeDef",
    {
        "comparison": CoverageStringComparisonType,
        "value": str,
    },
)

_RequiredCoveredResourceTypeDef = TypedDict(
    "_RequiredCoveredResourceTypeDef",
    {
        "accountId": str,
        "resourceId": str,
        "resourceType": CoverageResourceTypeType,
        "scanType": ScanTypeType,
    },
)
_OptionalCoveredResourceTypeDef = TypedDict(
    "_OptionalCoveredResourceTypeDef",
    {
        "resourceMetadata": "ResourceScanMetadataTypeDef",
        "scanStatus": "ScanStatusTypeDef",
    },
    total=False,
)


class CoveredResourceTypeDef(_RequiredCoveredResourceTypeDef, _OptionalCoveredResourceTypeDef):
    pass


_RequiredCreateFilterRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFilterRequestRequestTypeDef",
    {
        "action": FilterActionType,
        "filterCriteria": "FilterCriteriaTypeDef",
        "name": str,
    },
)
_OptionalCreateFilterRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFilterRequestRequestTypeDef",
    {
        "description": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateFilterRequestRequestTypeDef(
    _RequiredCreateFilterRequestRequestTypeDef, _OptionalCreateFilterRequestRequestTypeDef
):
    pass


CreateFilterResponseTypeDef = TypedDict(
    "CreateFilterResponseTypeDef",
    {
        "arn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateFindingsReportRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFindingsReportRequestRequestTypeDef",
    {
        "reportFormat": ReportFormatType,
        "s3Destination": "DestinationTypeDef",
    },
)
_OptionalCreateFindingsReportRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFindingsReportRequestRequestTypeDef",
    {
        "filterCriteria": "FilterCriteriaTypeDef",
    },
    total=False,
)


class CreateFindingsReportRequestRequestTypeDef(
    _RequiredCreateFindingsReportRequestRequestTypeDef,
    _OptionalCreateFindingsReportRequestRequestTypeDef,
):
    pass


CreateFindingsReportResponseTypeDef = TypedDict(
    "CreateFindingsReportResponseTypeDef",
    {
        "reportId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CvssScoreAdjustmentTypeDef = TypedDict(
    "CvssScoreAdjustmentTypeDef",
    {
        "metric": str,
        "reason": str,
    },
)

_RequiredCvssScoreDetailsTypeDef = TypedDict(
    "_RequiredCvssScoreDetailsTypeDef",
    {
        "score": float,
        "scoreSource": str,
        "scoringVector": str,
        "version": str,
    },
)
_OptionalCvssScoreDetailsTypeDef = TypedDict(
    "_OptionalCvssScoreDetailsTypeDef",
    {
        "adjustments": List["CvssScoreAdjustmentTypeDef"],
        "cvssSource": str,
    },
    total=False,
)


class CvssScoreDetailsTypeDef(_RequiredCvssScoreDetailsTypeDef, _OptionalCvssScoreDetailsTypeDef):
    pass


CvssScoreTypeDef = TypedDict(
    "CvssScoreTypeDef",
    {
        "baseScore": float,
        "scoringVector": str,
        "source": str,
        "version": str,
    },
)

DateFilterTypeDef = TypedDict(
    "DateFilterTypeDef",
    {
        "endInclusive": Union[datetime, str],
        "startInclusive": Union[datetime, str],
    },
    total=False,
)

DelegatedAdminAccountTypeDef = TypedDict(
    "DelegatedAdminAccountTypeDef",
    {
        "accountId": str,
        "status": DelegatedAdminStatusType,
    },
    total=False,
)

DelegatedAdminTypeDef = TypedDict(
    "DelegatedAdminTypeDef",
    {
        "accountId": str,
        "relationshipStatus": RelationshipStatusType,
    },
    total=False,
)

DeleteFilterRequestRequestTypeDef = TypedDict(
    "DeleteFilterRequestRequestTypeDef",
    {
        "arn": str,
    },
)

DeleteFilterResponseTypeDef = TypedDict(
    "DeleteFilterResponseTypeDef",
    {
        "arn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeOrganizationConfigurationResponseTypeDef = TypedDict(
    "DescribeOrganizationConfigurationResponseTypeDef",
    {
        "autoEnable": "AutoEnableTypeDef",
        "maxAccountLimitReached": bool,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDestinationTypeDef = TypedDict(
    "_RequiredDestinationTypeDef",
    {
        "bucketName": str,
        "kmsKeyArn": str,
    },
)
_OptionalDestinationTypeDef = TypedDict(
    "_OptionalDestinationTypeDef",
    {
        "keyPrefix": str,
    },
    total=False,
)


class DestinationTypeDef(_RequiredDestinationTypeDef, _OptionalDestinationTypeDef):
    pass


DisableDelegatedAdminAccountRequestRequestTypeDef = TypedDict(
    "DisableDelegatedAdminAccountRequestRequestTypeDef",
    {
        "delegatedAdminAccountId": str,
    },
)

DisableDelegatedAdminAccountResponseTypeDef = TypedDict(
    "DisableDelegatedAdminAccountResponseTypeDef",
    {
        "delegatedAdminAccountId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DisableRequestRequestTypeDef = TypedDict(
    "DisableRequestRequestTypeDef",
    {
        "accountIds": Sequence[str],
        "resourceTypes": Sequence[ResourceScanTypeType],
    },
    total=False,
)

DisableResponseTypeDef = TypedDict(
    "DisableResponseTypeDef",
    {
        "accounts": List["AccountTypeDef"],
        "failedAccounts": List["FailedAccountTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DisassociateMemberRequestRequestTypeDef = TypedDict(
    "DisassociateMemberRequestRequestTypeDef",
    {
        "accountId": str,
    },
)

DisassociateMemberResponseTypeDef = TypedDict(
    "DisassociateMemberResponseTypeDef",
    {
        "accountId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredEc2InstanceAggregationResponseTypeDef = TypedDict(
    "_RequiredEc2InstanceAggregationResponseTypeDef",
    {
        "instanceId": str,
    },
)
_OptionalEc2InstanceAggregationResponseTypeDef = TypedDict(
    "_OptionalEc2InstanceAggregationResponseTypeDef",
    {
        "accountId": str,
        "ami": str,
        "instanceTags": Dict[str, str],
        "networkFindings": int,
        "operatingSystem": str,
        "severityCounts": "SeverityCountsTypeDef",
    },
    total=False,
)


class Ec2InstanceAggregationResponseTypeDef(
    _RequiredEc2InstanceAggregationResponseTypeDef, _OptionalEc2InstanceAggregationResponseTypeDef
):
    pass


Ec2InstanceAggregationTypeDef = TypedDict(
    "Ec2InstanceAggregationTypeDef",
    {
        "amis": Sequence["StringFilterTypeDef"],
        "instanceIds": Sequence["StringFilterTypeDef"],
        "instanceTags": Sequence["MapFilterTypeDef"],
        "operatingSystems": Sequence["StringFilterTypeDef"],
        "sortBy": Ec2InstanceSortByType,
        "sortOrder": SortOrderType,
    },
    total=False,
)

Ec2MetadataTypeDef = TypedDict(
    "Ec2MetadataTypeDef",
    {
        "amiId": str,
        "platform": Ec2PlatformType,
        "tags": Dict[str, str],
    },
    total=False,
)

EcrContainerImageMetadataTypeDef = TypedDict(
    "EcrContainerImageMetadataTypeDef",
    {
        "tags": List[str],
    },
    total=False,
)

EcrRepositoryMetadataTypeDef = TypedDict(
    "EcrRepositoryMetadataTypeDef",
    {
        "name": str,
        "scanFrequency": EcrScanFrequencyType,
    },
    total=False,
)

_RequiredEnableDelegatedAdminAccountRequestRequestTypeDef = TypedDict(
    "_RequiredEnableDelegatedAdminAccountRequestRequestTypeDef",
    {
        "delegatedAdminAccountId": str,
    },
)
_OptionalEnableDelegatedAdminAccountRequestRequestTypeDef = TypedDict(
    "_OptionalEnableDelegatedAdminAccountRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class EnableDelegatedAdminAccountRequestRequestTypeDef(
    _RequiredEnableDelegatedAdminAccountRequestRequestTypeDef,
    _OptionalEnableDelegatedAdminAccountRequestRequestTypeDef,
):
    pass


EnableDelegatedAdminAccountResponseTypeDef = TypedDict(
    "EnableDelegatedAdminAccountResponseTypeDef",
    {
        "delegatedAdminAccountId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredEnableRequestRequestTypeDef = TypedDict(
    "_RequiredEnableRequestRequestTypeDef",
    {
        "resourceTypes": Sequence[ResourceScanTypeType],
    },
)
_OptionalEnableRequestRequestTypeDef = TypedDict(
    "_OptionalEnableRequestRequestTypeDef",
    {
        "accountIds": Sequence[str],
        "clientToken": str,
    },
    total=False,
)


class EnableRequestRequestTypeDef(
    _RequiredEnableRequestRequestTypeDef, _OptionalEnableRequestRequestTypeDef
):
    pass


EnableResponseTypeDef = TypedDict(
    "EnableResponseTypeDef",
    {
        "accounts": List["AccountTypeDef"],
        "failedAccounts": List["FailedAccountTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredFailedAccountTypeDef = TypedDict(
    "_RequiredFailedAccountTypeDef",
    {
        "accountId": str,
        "errorCode": ErrorCodeType,
        "errorMessage": str,
    },
)
_OptionalFailedAccountTypeDef = TypedDict(
    "_OptionalFailedAccountTypeDef",
    {
        "resourceStatus": "ResourceStatusTypeDef",
        "status": StatusType,
    },
    total=False,
)


class FailedAccountTypeDef(_RequiredFailedAccountTypeDef, _OptionalFailedAccountTypeDef):
    pass


FilterCriteriaTypeDef = TypedDict(
    "FilterCriteriaTypeDef",
    {
        "awsAccountId": Sequence["StringFilterTypeDef"],
        "componentId": Sequence["StringFilterTypeDef"],
        "componentType": Sequence["StringFilterTypeDef"],
        "ec2InstanceImageId": Sequence["StringFilterTypeDef"],
        "ec2InstanceSubnetId": Sequence["StringFilterTypeDef"],
        "ec2InstanceVpcId": Sequence["StringFilterTypeDef"],
        "ecrImageArchitecture": Sequence["StringFilterTypeDef"],
        "ecrImageHash": Sequence["StringFilterTypeDef"],
        "ecrImagePushedAt": Sequence["DateFilterTypeDef"],
        "ecrImageRegistry": Sequence["StringFilterTypeDef"],
        "ecrImageRepositoryName": Sequence["StringFilterTypeDef"],
        "ecrImageTags": Sequence["StringFilterTypeDef"],
        "findingArn": Sequence["StringFilterTypeDef"],
        "findingStatus": Sequence["StringFilterTypeDef"],
        "findingType": Sequence["StringFilterTypeDef"],
        "firstObservedAt": Sequence["DateFilterTypeDef"],
        "inspectorScore": Sequence["NumberFilterTypeDef"],
        "lastObservedAt": Sequence["DateFilterTypeDef"],
        "networkProtocol": Sequence["StringFilterTypeDef"],
        "portRange": Sequence["PortRangeFilterTypeDef"],
        "relatedVulnerabilities": Sequence["StringFilterTypeDef"],
        "resourceId": Sequence["StringFilterTypeDef"],
        "resourceTags": Sequence["MapFilterTypeDef"],
        "resourceType": Sequence["StringFilterTypeDef"],
        "severity": Sequence["StringFilterTypeDef"],
        "title": Sequence["StringFilterTypeDef"],
        "updatedAt": Sequence["DateFilterTypeDef"],
        "vendorSeverity": Sequence["StringFilterTypeDef"],
        "vulnerabilityId": Sequence["StringFilterTypeDef"],
        "vulnerabilitySource": Sequence["StringFilterTypeDef"],
        "vulnerablePackages": Sequence["PackageFilterTypeDef"],
    },
    total=False,
)

_RequiredFilterTypeDef = TypedDict(
    "_RequiredFilterTypeDef",
    {
        "action": FilterActionType,
        "arn": str,
        "createdAt": datetime,
        "criteria": "FilterCriteriaTypeDef",
        "name": str,
        "ownerId": str,
        "updatedAt": datetime,
    },
)
_OptionalFilterTypeDef = TypedDict(
    "_OptionalFilterTypeDef",
    {
        "description": str,
        "reason": str,
        "tags": Dict[str, str],
    },
    total=False,
)


class FilterTypeDef(_RequiredFilterTypeDef, _OptionalFilterTypeDef):
    pass


FindingTypeAggregationResponseTypeDef = TypedDict(
    "FindingTypeAggregationResponseTypeDef",
    {
        "accountId": str,
        "severityCounts": "SeverityCountsTypeDef",
    },
    total=False,
)

FindingTypeAggregationTypeDef = TypedDict(
    "FindingTypeAggregationTypeDef",
    {
        "findingType": AggregationFindingTypeType,
        "resourceType": AggregationResourceTypeType,
        "sortBy": FindingTypeSortByType,
        "sortOrder": SortOrderType,
    },
    total=False,
)

_RequiredFindingTypeDef = TypedDict(
    "_RequiredFindingTypeDef",
    {
        "awsAccountId": str,
        "description": str,
        "findingArn": str,
        "firstObservedAt": datetime,
        "lastObservedAt": datetime,
        "remediation": "RemediationTypeDef",
        "resources": List["ResourceTypeDef"],
        "severity": SeverityType,
        "status": FindingStatusType,
        "type": FindingTypeType,
    },
)
_OptionalFindingTypeDef = TypedDict(
    "_OptionalFindingTypeDef",
    {
        "inspectorScore": float,
        "inspectorScoreDetails": "InspectorScoreDetailsTypeDef",
        "networkReachabilityDetails": "NetworkReachabilityDetailsTypeDef",
        "packageVulnerabilityDetails": "PackageVulnerabilityDetailsTypeDef",
        "title": str,
        "updatedAt": datetime,
    },
    total=False,
)


class FindingTypeDef(_RequiredFindingTypeDef, _OptionalFindingTypeDef):
    pass


FreeTrialAccountInfoTypeDef = TypedDict(
    "FreeTrialAccountInfoTypeDef",
    {
        "accountId": str,
        "freeTrialInfo": List["FreeTrialInfoTypeDef"],
    },
)

FreeTrialInfoErrorTypeDef = TypedDict(
    "FreeTrialInfoErrorTypeDef",
    {
        "accountId": str,
        "code": FreeTrialInfoErrorCodeType,
        "message": str,
    },
)

FreeTrialInfoTypeDef = TypedDict(
    "FreeTrialInfoTypeDef",
    {
        "end": datetime,
        "start": datetime,
        "status": FreeTrialStatusType,
        "type": FreeTrialTypeType,
    },
)

GetDelegatedAdminAccountResponseTypeDef = TypedDict(
    "GetDelegatedAdminAccountResponseTypeDef",
    {
        "delegatedAdmin": "DelegatedAdminTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetFindingsReportStatusRequestRequestTypeDef = TypedDict(
    "GetFindingsReportStatusRequestRequestTypeDef",
    {
        "reportId": str,
    },
    total=False,
)

GetFindingsReportStatusResponseTypeDef = TypedDict(
    "GetFindingsReportStatusResponseTypeDef",
    {
        "destination": "DestinationTypeDef",
        "errorCode": ReportingErrorCodeType,
        "errorMessage": str,
        "filterCriteria": "FilterCriteriaTypeDef",
        "reportId": str,
        "status": ExternalReportStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetMemberRequestRequestTypeDef = TypedDict(
    "GetMemberRequestRequestTypeDef",
    {
        "accountId": str,
    },
)

GetMemberResponseTypeDef = TypedDict(
    "GetMemberResponseTypeDef",
    {
        "member": "MemberTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredImageLayerAggregationResponseTypeDef = TypedDict(
    "_RequiredImageLayerAggregationResponseTypeDef",
    {
        "accountId": str,
        "layerHash": str,
        "repository": str,
        "resourceId": str,
    },
)
_OptionalImageLayerAggregationResponseTypeDef = TypedDict(
    "_OptionalImageLayerAggregationResponseTypeDef",
    {
        "severityCounts": "SeverityCountsTypeDef",
    },
    total=False,
)


class ImageLayerAggregationResponseTypeDef(
    _RequiredImageLayerAggregationResponseTypeDef, _OptionalImageLayerAggregationResponseTypeDef
):
    pass


ImageLayerAggregationTypeDef = TypedDict(
    "ImageLayerAggregationTypeDef",
    {
        "layerHashes": Sequence["StringFilterTypeDef"],
        "repositories": Sequence["StringFilterTypeDef"],
        "resourceIds": Sequence["StringFilterTypeDef"],
        "sortBy": ImageLayerSortByType,
        "sortOrder": SortOrderType,
    },
    total=False,
)

InspectorScoreDetailsTypeDef = TypedDict(
    "InspectorScoreDetailsTypeDef",
    {
        "adjustedCvss": "CvssScoreDetailsTypeDef",
    },
    total=False,
)

ListAccountPermissionsRequestListAccountPermissionsPaginateTypeDef = TypedDict(
    "ListAccountPermissionsRequestListAccountPermissionsPaginateTypeDef",
    {
        "service": ServiceType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListAccountPermissionsRequestRequestTypeDef = TypedDict(
    "ListAccountPermissionsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "service": ServiceType,
    },
    total=False,
)

ListAccountPermissionsResponseTypeDef = TypedDict(
    "ListAccountPermissionsResponseTypeDef",
    {
        "nextToken": str,
        "permissions": List["PermissionTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListCoverageRequestListCoveragePaginateTypeDef = TypedDict(
    "ListCoverageRequestListCoveragePaginateTypeDef",
    {
        "filterCriteria": "CoverageFilterCriteriaTypeDef",
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListCoverageRequestRequestTypeDef = TypedDict(
    "ListCoverageRequestRequestTypeDef",
    {
        "filterCriteria": "CoverageFilterCriteriaTypeDef",
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListCoverageResponseTypeDef = TypedDict(
    "ListCoverageResponseTypeDef",
    {
        "coveredResources": List["CoveredResourceTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListCoverageStatisticsRequestListCoverageStatisticsPaginateTypeDef = TypedDict(
    "ListCoverageStatisticsRequestListCoverageStatisticsPaginateTypeDef",
    {
        "filterCriteria": "CoverageFilterCriteriaTypeDef",
        "groupBy": GroupKeyType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListCoverageStatisticsRequestRequestTypeDef = TypedDict(
    "ListCoverageStatisticsRequestRequestTypeDef",
    {
        "filterCriteria": "CoverageFilterCriteriaTypeDef",
        "groupBy": GroupKeyType,
        "nextToken": str,
    },
    total=False,
)

ListCoverageStatisticsResponseTypeDef = TypedDict(
    "ListCoverageStatisticsResponseTypeDef",
    {
        "countsByGroup": List["CountsTypeDef"],
        "nextToken": str,
        "totalCounts": int,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListDelegatedAdminAccountsRequestListDelegatedAdminAccountsPaginateTypeDef = TypedDict(
    "ListDelegatedAdminAccountsRequestListDelegatedAdminAccountsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListDelegatedAdminAccountsRequestRequestTypeDef = TypedDict(
    "ListDelegatedAdminAccountsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListDelegatedAdminAccountsResponseTypeDef = TypedDict(
    "ListDelegatedAdminAccountsResponseTypeDef",
    {
        "delegatedAdminAccounts": List["DelegatedAdminAccountTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListFiltersRequestListFiltersPaginateTypeDef = TypedDict(
    "ListFiltersRequestListFiltersPaginateTypeDef",
    {
        "action": FilterActionType,
        "arns": Sequence[str],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListFiltersRequestRequestTypeDef = TypedDict(
    "ListFiltersRequestRequestTypeDef",
    {
        "action": FilterActionType,
        "arns": Sequence[str],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListFiltersResponseTypeDef = TypedDict(
    "ListFiltersResponseTypeDef",
    {
        "filters": List["FilterTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListFindingAggregationsRequestListFindingAggregationsPaginateTypeDef = TypedDict(
    "_RequiredListFindingAggregationsRequestListFindingAggregationsPaginateTypeDef",
    {
        "aggregationType": AggregationTypeType,
    },
)
_OptionalListFindingAggregationsRequestListFindingAggregationsPaginateTypeDef = TypedDict(
    "_OptionalListFindingAggregationsRequestListFindingAggregationsPaginateTypeDef",
    {
        "accountIds": Sequence["StringFilterTypeDef"],
        "aggregationRequest": "AggregationRequestTypeDef",
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListFindingAggregationsRequestListFindingAggregationsPaginateTypeDef(
    _RequiredListFindingAggregationsRequestListFindingAggregationsPaginateTypeDef,
    _OptionalListFindingAggregationsRequestListFindingAggregationsPaginateTypeDef,
):
    pass


_RequiredListFindingAggregationsRequestRequestTypeDef = TypedDict(
    "_RequiredListFindingAggregationsRequestRequestTypeDef",
    {
        "aggregationType": AggregationTypeType,
    },
)
_OptionalListFindingAggregationsRequestRequestTypeDef = TypedDict(
    "_OptionalListFindingAggregationsRequestRequestTypeDef",
    {
        "accountIds": Sequence["StringFilterTypeDef"],
        "aggregationRequest": "AggregationRequestTypeDef",
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListFindingAggregationsRequestRequestTypeDef(
    _RequiredListFindingAggregationsRequestRequestTypeDef,
    _OptionalListFindingAggregationsRequestRequestTypeDef,
):
    pass


ListFindingAggregationsResponseTypeDef = TypedDict(
    "ListFindingAggregationsResponseTypeDef",
    {
        "aggregationType": AggregationTypeType,
        "nextToken": str,
        "responses": List["AggregationResponseTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListFindingsRequestListFindingsPaginateTypeDef = TypedDict(
    "ListFindingsRequestListFindingsPaginateTypeDef",
    {
        "filterCriteria": "FilterCriteriaTypeDef",
        "sortCriteria": "SortCriteriaTypeDef",
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListFindingsRequestRequestTypeDef = TypedDict(
    "ListFindingsRequestRequestTypeDef",
    {
        "filterCriteria": "FilterCriteriaTypeDef",
        "maxResults": int,
        "nextToken": str,
        "sortCriteria": "SortCriteriaTypeDef",
    },
    total=False,
)

ListFindingsResponseTypeDef = TypedDict(
    "ListFindingsResponseTypeDef",
    {
        "findings": List["FindingTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListMembersRequestListMembersPaginateTypeDef = TypedDict(
    "ListMembersRequestListMembersPaginateTypeDef",
    {
        "onlyAssociated": bool,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListMembersRequestRequestTypeDef = TypedDict(
    "ListMembersRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "onlyAssociated": bool,
    },
    total=False,
)

ListMembersResponseTypeDef = TypedDict(
    "ListMembersResponseTypeDef",
    {
        "members": List["MemberTypeDef"],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListUsageTotalsRequestListUsageTotalsPaginateTypeDef = TypedDict(
    "ListUsageTotalsRequestListUsageTotalsPaginateTypeDef",
    {
        "accountIds": Sequence[str],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListUsageTotalsRequestRequestTypeDef = TypedDict(
    "ListUsageTotalsRequestRequestTypeDef",
    {
        "accountIds": Sequence[str],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListUsageTotalsResponseTypeDef = TypedDict(
    "ListUsageTotalsResponseTypeDef",
    {
        "nextToken": str,
        "totals": List["UsageTotalTypeDef"],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredMapFilterTypeDef = TypedDict(
    "_RequiredMapFilterTypeDef",
    {
        "comparison": Literal["EQUALS"],
        "key": str,
    },
)
_OptionalMapFilterTypeDef = TypedDict(
    "_OptionalMapFilterTypeDef",
    {
        "value": str,
    },
    total=False,
)


class MapFilterTypeDef(_RequiredMapFilterTypeDef, _OptionalMapFilterTypeDef):
    pass


MemberTypeDef = TypedDict(
    "MemberTypeDef",
    {
        "accountId": str,
        "delegatedAdminAccountId": str,
        "relationshipStatus": RelationshipStatusType,
        "updatedAt": datetime,
    },
    total=False,
)

NetworkPathTypeDef = TypedDict(
    "NetworkPathTypeDef",
    {
        "steps": List["StepTypeDef"],
    },
    total=False,
)

NetworkReachabilityDetailsTypeDef = TypedDict(
    "NetworkReachabilityDetailsTypeDef",
    {
        "networkPath": "NetworkPathTypeDef",
        "openPortRange": "PortRangeTypeDef",
        "protocol": NetworkProtocolType,
    },
)

NumberFilterTypeDef = TypedDict(
    "NumberFilterTypeDef",
    {
        "lowerInclusive": float,
        "upperInclusive": float,
    },
    total=False,
)

_RequiredPackageAggregationResponseTypeDef = TypedDict(
    "_RequiredPackageAggregationResponseTypeDef",
    {
        "packageName": str,
    },
)
_OptionalPackageAggregationResponseTypeDef = TypedDict(
    "_OptionalPackageAggregationResponseTypeDef",
    {
        "accountId": str,
        "severityCounts": "SeverityCountsTypeDef",
    },
    total=False,
)


class PackageAggregationResponseTypeDef(
    _RequiredPackageAggregationResponseTypeDef, _OptionalPackageAggregationResponseTypeDef
):
    pass


PackageAggregationTypeDef = TypedDict(
    "PackageAggregationTypeDef",
    {
        "packageNames": Sequence["StringFilterTypeDef"],
        "sortBy": PackageSortByType,
        "sortOrder": SortOrderType,
    },
    total=False,
)

PackageFilterTypeDef = TypedDict(
    "PackageFilterTypeDef",
    {
        "architecture": "StringFilterTypeDef",
        "epoch": "NumberFilterTypeDef",
        "name": "StringFilterTypeDef",
        "release": "StringFilterTypeDef",
        "sourceLayerHash": "StringFilterTypeDef",
        "version": "StringFilterTypeDef",
    },
    total=False,
)

_RequiredPackageVulnerabilityDetailsTypeDef = TypedDict(
    "_RequiredPackageVulnerabilityDetailsTypeDef",
    {
        "source": str,
        "vulnerabilityId": str,
        "vulnerablePackages": List["VulnerablePackageTypeDef"],
    },
)
_OptionalPackageVulnerabilityDetailsTypeDef = TypedDict(
    "_OptionalPackageVulnerabilityDetailsTypeDef",
    {
        "cvss": List["CvssScoreTypeDef"],
        "referenceUrls": List[str],
        "relatedVulnerabilities": List[str],
        "sourceUrl": str,
        "vendorCreatedAt": datetime,
        "vendorSeverity": str,
        "vendorUpdatedAt": datetime,
    },
    total=False,
)


class PackageVulnerabilityDetailsTypeDef(
    _RequiredPackageVulnerabilityDetailsTypeDef, _OptionalPackageVulnerabilityDetailsTypeDef
):
    pass


PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

PermissionTypeDef = TypedDict(
    "PermissionTypeDef",
    {
        "operation": OperationType,
        "service": ServiceType,
    },
)

PortRangeFilterTypeDef = TypedDict(
    "PortRangeFilterTypeDef",
    {
        "beginInclusive": int,
        "endInclusive": int,
    },
    total=False,
)

PortRangeTypeDef = TypedDict(
    "PortRangeTypeDef",
    {
        "begin": int,
        "end": int,
    },
)

RecommendationTypeDef = TypedDict(
    "RecommendationTypeDef",
    {
        "Url": str,
        "text": str,
    },
    total=False,
)

RemediationTypeDef = TypedDict(
    "RemediationTypeDef",
    {
        "recommendation": "RecommendationTypeDef",
    },
    total=False,
)

_RequiredRepositoryAggregationResponseTypeDef = TypedDict(
    "_RequiredRepositoryAggregationResponseTypeDef",
    {
        "repository": str,
    },
)
_OptionalRepositoryAggregationResponseTypeDef = TypedDict(
    "_OptionalRepositoryAggregationResponseTypeDef",
    {
        "accountId": str,
        "affectedImages": int,
        "severityCounts": "SeverityCountsTypeDef",
    },
    total=False,
)


class RepositoryAggregationResponseTypeDef(
    _RequiredRepositoryAggregationResponseTypeDef, _OptionalRepositoryAggregationResponseTypeDef
):
    pass


RepositoryAggregationTypeDef = TypedDict(
    "RepositoryAggregationTypeDef",
    {
        "repositories": Sequence["StringFilterTypeDef"],
        "sortBy": RepositorySortByType,
        "sortOrder": SortOrderType,
    },
    total=False,
)

ResourceDetailsTypeDef = TypedDict(
    "ResourceDetailsTypeDef",
    {
        "awsEc2Instance": "AwsEc2InstanceDetailsTypeDef",
        "awsEcrContainerImage": "AwsEcrContainerImageDetailsTypeDef",
    },
    total=False,
)

ResourceScanMetadataTypeDef = TypedDict(
    "ResourceScanMetadataTypeDef",
    {
        "ec2": "Ec2MetadataTypeDef",
        "ecrImage": "EcrContainerImageMetadataTypeDef",
        "ecrRepository": "EcrRepositoryMetadataTypeDef",
    },
    total=False,
)

ResourceStateTypeDef = TypedDict(
    "ResourceStateTypeDef",
    {
        "ec2": "StateTypeDef",
        "ecr": "StateTypeDef",
    },
)

ResourceStatusTypeDef = TypedDict(
    "ResourceStatusTypeDef",
    {
        "ec2": StatusType,
        "ecr": StatusType,
    },
)

_RequiredResourceTypeDef = TypedDict(
    "_RequiredResourceTypeDef",
    {
        "id": str,
        "type": ResourceTypeType,
    },
)
_OptionalResourceTypeDef = TypedDict(
    "_OptionalResourceTypeDef",
    {
        "details": "ResourceDetailsTypeDef",
        "partition": str,
        "region": str,
        "tags": Dict[str, str],
    },
    total=False,
)


class ResourceTypeDef(_RequiredResourceTypeDef, _OptionalResourceTypeDef):
    pass


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

ScanStatusTypeDef = TypedDict(
    "ScanStatusTypeDef",
    {
        "reason": ScanStatusReasonType,
        "statusCode": ScanStatusCodeType,
    },
)

SeverityCountsTypeDef = TypedDict(
    "SeverityCountsTypeDef",
    {
        "all": int,
        "critical": int,
        "high": int,
        "medium": int,
    },
    total=False,
)

SortCriteriaTypeDef = TypedDict(
    "SortCriteriaTypeDef",
    {
        "field": SortFieldType,
        "sortOrder": SortOrderType,
    },
)

StateTypeDef = TypedDict(
    "StateTypeDef",
    {
        "errorCode": ErrorCodeType,
        "errorMessage": str,
        "status": StatusType,
    },
)

StepTypeDef = TypedDict(
    "StepTypeDef",
    {
        "componentId": str,
        "componentType": str,
    },
)

StringFilterTypeDef = TypedDict(
    "StringFilterTypeDef",
    {
        "comparison": StringComparisonType,
        "value": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

_RequiredTitleAggregationResponseTypeDef = TypedDict(
    "_RequiredTitleAggregationResponseTypeDef",
    {
        "title": str,
    },
)
_OptionalTitleAggregationResponseTypeDef = TypedDict(
    "_OptionalTitleAggregationResponseTypeDef",
    {
        "accountId": str,
        "severityCounts": "SeverityCountsTypeDef",
        "vulnerabilityId": str,
    },
    total=False,
)


class TitleAggregationResponseTypeDef(
    _RequiredTitleAggregationResponseTypeDef, _OptionalTitleAggregationResponseTypeDef
):
    pass


TitleAggregationTypeDef = TypedDict(
    "TitleAggregationTypeDef",
    {
        "resourceType": AggregationResourceTypeType,
        "sortBy": TitleSortByType,
        "sortOrder": SortOrderType,
        "titles": Sequence["StringFilterTypeDef"],
        "vulnerabilityIds": Sequence["StringFilterTypeDef"],
    },
    total=False,
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateFilterRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFilterRequestRequestTypeDef",
    {
        "filterArn": str,
    },
)
_OptionalUpdateFilterRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFilterRequestRequestTypeDef",
    {
        "action": FilterActionType,
        "description": str,
        "filterCriteria": "FilterCriteriaTypeDef",
        "name": str,
    },
    total=False,
)


class UpdateFilterRequestRequestTypeDef(
    _RequiredUpdateFilterRequestRequestTypeDef, _OptionalUpdateFilterRequestRequestTypeDef
):
    pass


UpdateFilterResponseTypeDef = TypedDict(
    "UpdateFilterResponseTypeDef",
    {
        "arn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateOrganizationConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateOrganizationConfigurationRequestRequestTypeDef",
    {
        "autoEnable": "AutoEnableTypeDef",
    },
)

UpdateOrganizationConfigurationResponseTypeDef = TypedDict(
    "UpdateOrganizationConfigurationResponseTypeDef",
    {
        "autoEnable": "AutoEnableTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UsageTotalTypeDef = TypedDict(
    "UsageTotalTypeDef",
    {
        "accountId": str,
        "usage": List["UsageTypeDef"],
    },
    total=False,
)

UsageTypeDef = TypedDict(
    "UsageTypeDef",
    {
        "currency": Literal["USD"],
        "estimatedMonthlyCost": float,
        "total": float,
        "type": UsageTypeType,
    },
    total=False,
)

_RequiredVulnerablePackageTypeDef = TypedDict(
    "_RequiredVulnerablePackageTypeDef",
    {
        "name": str,
        "version": str,
    },
)
_OptionalVulnerablePackageTypeDef = TypedDict(
    "_OptionalVulnerablePackageTypeDef",
    {
        "arch": str,
        "epoch": int,
        "filePath": str,
        "fixedInVersion": str,
        "packageManager": PackageManagerType,
        "release": str,
        "sourceLayerHash": str,
    },
    total=False,
)


class VulnerablePackageTypeDef(
    _RequiredVulnerablePackageTypeDef, _OptionalVulnerablePackageTypeDef
):
    pass
