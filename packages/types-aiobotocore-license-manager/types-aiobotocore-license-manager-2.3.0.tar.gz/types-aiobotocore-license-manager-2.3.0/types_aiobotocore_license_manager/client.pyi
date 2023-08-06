"""
Type annotations for license-manager service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_license_manager.client import LicenseManagerClient

    session = get_session()
    async with session.create_client("license-manager") as client:
        client: LicenseManagerClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    AllowedOperationType,
    CheckoutTypeType,
    GrantStatusType,
    LicenseConfigurationStatusType,
    LicenseCountingTypeType,
    LicenseStatusType,
    ReportTypeType,
)
from .paginator import (
    ListAssociationsForLicenseConfigurationPaginator,
    ListLicenseConfigurationsPaginator,
    ListLicenseSpecificationsForResourcePaginator,
    ListResourceInventoryPaginator,
    ListUsageForLicenseConfigurationPaginator,
)
from .type_defs import (
    AcceptGrantResponseTypeDef,
    CheckoutBorrowLicenseResponseTypeDef,
    CheckoutLicenseResponseTypeDef,
    ConsumptionConfigurationTypeDef,
    CreateGrantResponseTypeDef,
    CreateGrantVersionResponseTypeDef,
    CreateLicenseConfigurationResponseTypeDef,
    CreateLicenseConversionTaskForResourceResponseTypeDef,
    CreateLicenseManagerReportGeneratorResponseTypeDef,
    CreateLicenseResponseTypeDef,
    CreateLicenseVersionResponseTypeDef,
    CreateTokenResponseTypeDef,
    DatetimeRangeTypeDef,
    DeleteGrantResponseTypeDef,
    DeleteLicenseResponseTypeDef,
    EntitlementDataTypeDef,
    EntitlementTypeDef,
    ExtendLicenseConsumptionResponseTypeDef,
    FilterTypeDef,
    GetAccessTokenResponseTypeDef,
    GetGrantResponseTypeDef,
    GetLicenseConfigurationResponseTypeDef,
    GetLicenseConversionTaskResponseTypeDef,
    GetLicenseManagerReportGeneratorResponseTypeDef,
    GetLicenseResponseTypeDef,
    GetLicenseUsageResponseTypeDef,
    GetServiceSettingsResponseTypeDef,
    InventoryFilterTypeDef,
    IssuerTypeDef,
    LicenseConversionContextTypeDef,
    LicenseSpecificationTypeDef,
    ListAssociationsForLicenseConfigurationResponseTypeDef,
    ListDistributedGrantsResponseTypeDef,
    ListFailuresForLicenseConfigurationOperationsResponseTypeDef,
    ListLicenseConfigurationsResponseTypeDef,
    ListLicenseConversionTasksResponseTypeDef,
    ListLicenseManagerReportGeneratorsResponseTypeDef,
    ListLicenseSpecificationsForResourceResponseTypeDef,
    ListLicensesResponseTypeDef,
    ListLicenseVersionsResponseTypeDef,
    ListReceivedGrantsResponseTypeDef,
    ListReceivedLicensesResponseTypeDef,
    ListResourceInventoryResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTokensResponseTypeDef,
    ListUsageForLicenseConfigurationResponseTypeDef,
    MetadataTypeDef,
    OrganizationConfigurationTypeDef,
    ProductInformationTypeDef,
    RejectGrantResponseTypeDef,
    ReportContextTypeDef,
    ReportFrequencyTypeDef,
    TagTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("LicenseManagerClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    AuthorizationException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    EntitlementNotAllowedException: Type[BotocoreClientError]
    FailedDependencyException: Type[BotocoreClientError]
    FilterLimitExceededException: Type[BotocoreClientError]
    InvalidParameterValueException: Type[BotocoreClientError]
    InvalidResourceStateException: Type[BotocoreClientError]
    LicenseUsageException: Type[BotocoreClientError]
    NoEntitlementsAllowedException: Type[BotocoreClientError]
    RateLimitExceededException: Type[BotocoreClientError]
    RedirectException: Type[BotocoreClientError]
    ResourceLimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServerInternalException: Type[BotocoreClientError]
    UnsupportedDigitalSignatureMethodException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class LicenseManagerClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LicenseManagerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#exceptions)
        """
    async def accept_grant(self, *, GrantArn: str) -> AcceptGrantResponseTypeDef:
        """
        Accepts the specified grant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.accept_grant)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#accept_grant)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#can_paginate)
        """
    async def check_in_license(
        self, *, LicenseConsumptionToken: str, Beneficiary: str = ...
    ) -> Dict[str, Any]:
        """
        Checks in the specified license.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.check_in_license)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#check_in_license)
        """
    async def checkout_borrow_license(
        self,
        *,
        LicenseArn: str,
        Entitlements: Sequence["EntitlementDataTypeDef"],
        DigitalSignatureMethod: Literal["JWT_PS384"],
        ClientToken: str,
        NodeId: str = ...,
        CheckoutMetadata: Sequence["MetadataTypeDef"] = ...
    ) -> CheckoutBorrowLicenseResponseTypeDef:
        """
        Checks out the specified license for offline use.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.checkout_borrow_license)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#checkout_borrow_license)
        """
    async def checkout_license(
        self,
        *,
        ProductSKU: str,
        CheckoutType: CheckoutTypeType,
        KeyFingerprint: str,
        Entitlements: Sequence["EntitlementDataTypeDef"],
        ClientToken: str,
        Beneficiary: str = ...,
        NodeId: str = ...
    ) -> CheckoutLicenseResponseTypeDef:
        """
        Checks out the specified license.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.checkout_license)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#checkout_license)
        """
    async def create_grant(
        self,
        *,
        ClientToken: str,
        GrantName: str,
        LicenseArn: str,
        Principals: Sequence[str],
        HomeRegion: str,
        AllowedOperations: Sequence[AllowedOperationType]
    ) -> CreateGrantResponseTypeDef:
        """
        Creates a grant for the specified license.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.create_grant)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#create_grant)
        """
    async def create_grant_version(
        self,
        *,
        ClientToken: str,
        GrantArn: str,
        GrantName: str = ...,
        AllowedOperations: Sequence[AllowedOperationType] = ...,
        Status: GrantStatusType = ...,
        StatusReason: str = ...,
        SourceVersion: str = ...
    ) -> CreateGrantVersionResponseTypeDef:
        """
        Creates a new version of the specified grant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.create_grant_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#create_grant_version)
        """
    async def create_license(
        self,
        *,
        LicenseName: str,
        ProductName: str,
        ProductSKU: str,
        Issuer: "IssuerTypeDef",
        HomeRegion: str,
        Validity: "DatetimeRangeTypeDef",
        Entitlements: Sequence["EntitlementTypeDef"],
        Beneficiary: str,
        ConsumptionConfiguration: "ConsumptionConfigurationTypeDef",
        ClientToken: str,
        LicenseMetadata: Sequence["MetadataTypeDef"] = ...
    ) -> CreateLicenseResponseTypeDef:
        """
        Creates a license.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.create_license)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#create_license)
        """
    async def create_license_configuration(
        self,
        *,
        Name: str,
        LicenseCountingType: LicenseCountingTypeType,
        Description: str = ...,
        LicenseCount: int = ...,
        LicenseCountHardLimit: bool = ...,
        LicenseRules: Sequence[str] = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        DisassociateWhenNotFound: bool = ...,
        ProductInformationList: Sequence["ProductInformationTypeDef"] = ...
    ) -> CreateLicenseConfigurationResponseTypeDef:
        """
        Creates a license configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.create_license_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#create_license_configuration)
        """
    async def create_license_conversion_task_for_resource(
        self,
        *,
        ResourceArn: str,
        SourceLicenseContext: "LicenseConversionContextTypeDef",
        DestinationLicenseContext: "LicenseConversionContextTypeDef"
    ) -> CreateLicenseConversionTaskForResourceResponseTypeDef:
        """
        Creates a new license conversion task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.create_license_conversion_task_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#create_license_conversion_task_for_resource)
        """
    async def create_license_manager_report_generator(
        self,
        *,
        ReportGeneratorName: str,
        Type: Sequence[ReportTypeType],
        ReportContext: "ReportContextTypeDef",
        ReportFrequency: "ReportFrequencyTypeDef",
        ClientToken: str,
        Description: str = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreateLicenseManagerReportGeneratorResponseTypeDef:
        """
        Creates a report generator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.create_license_manager_report_generator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#create_license_manager_report_generator)
        """
    async def create_license_version(
        self,
        *,
        LicenseArn: str,
        LicenseName: str,
        ProductName: str,
        Issuer: "IssuerTypeDef",
        HomeRegion: str,
        Validity: "DatetimeRangeTypeDef",
        Entitlements: Sequence["EntitlementTypeDef"],
        ConsumptionConfiguration: "ConsumptionConfigurationTypeDef",
        Status: LicenseStatusType,
        ClientToken: str,
        LicenseMetadata: Sequence["MetadataTypeDef"] = ...,
        SourceVersion: str = ...
    ) -> CreateLicenseVersionResponseTypeDef:
        """
        Creates a new version of the specified license.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.create_license_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#create_license_version)
        """
    async def create_token(
        self,
        *,
        LicenseArn: str,
        ClientToken: str,
        RoleArns: Sequence[str] = ...,
        ExpirationInDays: int = ...,
        TokenProperties: Sequence[str] = ...
    ) -> CreateTokenResponseTypeDef:
        """
        Creates a long-lived token.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.create_token)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#create_token)
        """
    async def delete_grant(
        self, *, GrantArn: str, Version: str, StatusReason: str = ...
    ) -> DeleteGrantResponseTypeDef:
        """
        Deletes the specified grant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.delete_grant)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#delete_grant)
        """
    async def delete_license(
        self, *, LicenseArn: str, SourceVersion: str
    ) -> DeleteLicenseResponseTypeDef:
        """
        Deletes the specified license.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.delete_license)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#delete_license)
        """
    async def delete_license_configuration(self, *, LicenseConfigurationArn: str) -> Dict[str, Any]:
        """
        Deletes the specified license configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.delete_license_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#delete_license_configuration)
        """
    async def delete_license_manager_report_generator(
        self, *, LicenseManagerReportGeneratorArn: str
    ) -> Dict[str, Any]:
        """
        Deletes the specified report generator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.delete_license_manager_report_generator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#delete_license_manager_report_generator)
        """
    async def delete_token(self, *, TokenId: str) -> Dict[str, Any]:
        """
        Deletes the specified token.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.delete_token)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#delete_token)
        """
    async def extend_license_consumption(
        self, *, LicenseConsumptionToken: str, DryRun: bool = ...
    ) -> ExtendLicenseConsumptionResponseTypeDef:
        """
        Extends the expiration date for license consumption.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.extend_license_consumption)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#extend_license_consumption)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#generate_presigned_url)
        """
    async def get_access_token(
        self, *, Token: str, TokenProperties: Sequence[str] = ...
    ) -> GetAccessTokenResponseTypeDef:
        """
        Gets a temporary access token to use with AssumeRoleWithWebIdentity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.get_access_token)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#get_access_token)
        """
    async def get_grant(self, *, GrantArn: str, Version: str = ...) -> GetGrantResponseTypeDef:
        """
        Gets detailed information about the specified grant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.get_grant)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#get_grant)
        """
    async def get_license(
        self, *, LicenseArn: str, Version: str = ...
    ) -> GetLicenseResponseTypeDef:
        """
        Gets detailed information about the specified license.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.get_license)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#get_license)
        """
    async def get_license_configuration(
        self, *, LicenseConfigurationArn: str
    ) -> GetLicenseConfigurationResponseTypeDef:
        """
        Gets detailed information about the specified license configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.get_license_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#get_license_configuration)
        """
    async def get_license_conversion_task(
        self, *, LicenseConversionTaskId: str
    ) -> GetLicenseConversionTaskResponseTypeDef:
        """
        Gets information about the specified license type conversion task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.get_license_conversion_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#get_license_conversion_task)
        """
    async def get_license_manager_report_generator(
        self, *, LicenseManagerReportGeneratorArn: str
    ) -> GetLicenseManagerReportGeneratorResponseTypeDef:
        """
        Gets information about the specified report generator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.get_license_manager_report_generator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#get_license_manager_report_generator)
        """
    async def get_license_usage(self, *, LicenseArn: str) -> GetLicenseUsageResponseTypeDef:
        """
        Gets detailed information about the usage of the specified license.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.get_license_usage)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#get_license_usage)
        """
    async def get_service_settings(self) -> GetServiceSettingsResponseTypeDef:
        """
        Gets the License Manager settings for the current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.get_service_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#get_service_settings)
        """
    async def list_associations_for_license_configuration(
        self, *, LicenseConfigurationArn: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListAssociationsForLicenseConfigurationResponseTypeDef:
        """
        Lists the resource associations for the specified license configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.list_associations_for_license_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#list_associations_for_license_configuration)
        """
    async def list_distributed_grants(
        self,
        *,
        GrantArns: Sequence[str] = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListDistributedGrantsResponseTypeDef:
        """
        Lists the grants distributed for the specified license.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.list_distributed_grants)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#list_distributed_grants)
        """
    async def list_failures_for_license_configuration_operations(
        self, *, LicenseConfigurationArn: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListFailuresForLicenseConfigurationOperationsResponseTypeDef:
        """
        Lists the license configuration operations that failed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.list_failures_for_license_configuration_operations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#list_failures_for_license_configuration_operations)
        """
    async def list_license_configurations(
        self,
        *,
        LicenseConfigurationArns: Sequence[str] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...
    ) -> ListLicenseConfigurationsResponseTypeDef:
        """
        Lists the license configurations for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.list_license_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#list_license_configurations)
        """
    async def list_license_conversion_tasks(
        self,
        *,
        NextToken: str = ...,
        MaxResults: int = ...,
        Filters: Sequence["FilterTypeDef"] = ...
    ) -> ListLicenseConversionTasksResponseTypeDef:
        """
        Lists the license type conversion tasks for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.list_license_conversion_tasks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#list_license_conversion_tasks)
        """
    async def list_license_manager_report_generators(
        self,
        *,
        Filters: Sequence["FilterTypeDef"] = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListLicenseManagerReportGeneratorsResponseTypeDef:
        """
        Lists the report generators for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.list_license_manager_report_generators)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#list_license_manager_report_generators)
        """
    async def list_license_specifications_for_resource(
        self, *, ResourceArn: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListLicenseSpecificationsForResourceResponseTypeDef:
        """
        Describes the license configurations for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.list_license_specifications_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#list_license_specifications_for_resource)
        """
    async def list_license_versions(
        self, *, LicenseArn: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListLicenseVersionsResponseTypeDef:
        """
        Lists all versions of the specified license.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.list_license_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#list_license_versions)
        """
    async def list_licenses(
        self,
        *,
        LicenseArns: Sequence[str] = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListLicensesResponseTypeDef:
        """
        Lists the licenses for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.list_licenses)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#list_licenses)
        """
    async def list_received_grants(
        self,
        *,
        GrantArns: Sequence[str] = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListReceivedGrantsResponseTypeDef:
        """
        Lists grants that are received but not accepted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.list_received_grants)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#list_received_grants)
        """
    async def list_received_licenses(
        self,
        *,
        LicenseArns: Sequence[str] = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListReceivedLicensesResponseTypeDef:
        """
        Lists received licenses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.list_received_licenses)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#list_received_licenses)
        """
    async def list_resource_inventory(
        self,
        *,
        MaxResults: int = ...,
        NextToken: str = ...,
        Filters: Sequence["InventoryFilterTypeDef"] = ...
    ) -> ListResourceInventoryResponseTypeDef:
        """
        Lists resources managed using Systems Manager inventory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.list_resource_inventory)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#list_resource_inventory)
        """
    async def list_tags_for_resource(
        self, *, ResourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for the specified license configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#list_tags_for_resource)
        """
    async def list_tokens(
        self,
        *,
        TokenIds: Sequence[str] = ...,
        Filters: Sequence["FilterTypeDef"] = ...,
        NextToken: str = ...,
        MaxResults: int = ...
    ) -> ListTokensResponseTypeDef:
        """
        Lists your tokens.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.list_tokens)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#list_tokens)
        """
    async def list_usage_for_license_configuration(
        self,
        *,
        LicenseConfigurationArn: str,
        MaxResults: int = ...,
        NextToken: str = ...,
        Filters: Sequence["FilterTypeDef"] = ...
    ) -> ListUsageForLicenseConfigurationResponseTypeDef:
        """
        Lists all license usage records for a license configuration, displaying license
        consumption details by resource at a selected point in time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.list_usage_for_license_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#list_usage_for_license_configuration)
        """
    async def reject_grant(self, *, GrantArn: str) -> RejectGrantResponseTypeDef:
        """
        Rejects the specified grant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.reject_grant)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#reject_grant)
        """
    async def tag_resource(
        self, *, ResourceArn: str, Tags: Sequence["TagTypeDef"]
    ) -> Dict[str, Any]:
        """
        Adds the specified tags to the specified license configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#tag_resource)
        """
    async def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes the specified tags from the specified license configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#untag_resource)
        """
    async def update_license_configuration(
        self,
        *,
        LicenseConfigurationArn: str,
        LicenseConfigurationStatus: LicenseConfigurationStatusType = ...,
        LicenseRules: Sequence[str] = ...,
        LicenseCount: int = ...,
        LicenseCountHardLimit: bool = ...,
        Name: str = ...,
        Description: str = ...,
        ProductInformationList: Sequence["ProductInformationTypeDef"] = ...,
        DisassociateWhenNotFound: bool = ...
    ) -> Dict[str, Any]:
        """
        Modifies the attributes of an existing license configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.update_license_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#update_license_configuration)
        """
    async def update_license_manager_report_generator(
        self,
        *,
        LicenseManagerReportGeneratorArn: str,
        ReportGeneratorName: str,
        Type: Sequence[ReportTypeType],
        ReportContext: "ReportContextTypeDef",
        ReportFrequency: "ReportFrequencyTypeDef",
        ClientToken: str,
        Description: str = ...
    ) -> Dict[str, Any]:
        """
        Updates a report generator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.update_license_manager_report_generator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#update_license_manager_report_generator)
        """
    async def update_license_specifications_for_resource(
        self,
        *,
        ResourceArn: str,
        AddLicenseSpecifications: Sequence["LicenseSpecificationTypeDef"] = ...,
        RemoveLicenseSpecifications: Sequence["LicenseSpecificationTypeDef"] = ...
    ) -> Dict[str, Any]:
        """
        Adds or removes the specified license configurations for the specified Amazon
        Web Services resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.update_license_specifications_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#update_license_specifications_for_resource)
        """
    async def update_service_settings(
        self,
        *,
        S3BucketArn: str = ...,
        SnsTopicArn: str = ...,
        OrganizationConfiguration: "OrganizationConfigurationTypeDef" = ...,
        EnableCrossAccountsDiscovery: bool = ...
    ) -> Dict[str, Any]:
        """
        Updates License Manager settings for the current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.update_service_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#update_service_settings)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_associations_for_license_configuration"]
    ) -> ListAssociationsForLicenseConfigurationPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_license_configurations"]
    ) -> ListLicenseConfigurationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_license_specifications_for_resource"]
    ) -> ListLicenseSpecificationsForResourcePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_resource_inventory"]
    ) -> ListResourceInventoryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_usage_for_license_configuration"]
    ) -> ListUsageForLicenseConfigurationPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/#get_paginator)
        """
    async def __aenter__(self) -> "LicenseManagerClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager.html#LicenseManager.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_license_manager/client/)
        """
