"""
Type annotations for elasticbeanstalk service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_elasticbeanstalk.client import ElasticBeanstalkClient

    session = get_session()
    async with session.create_client("elasticbeanstalk") as client:
        client: ElasticBeanstalkClient
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    ActionStatusType,
    EnvironmentHealthAttributeType,
    EnvironmentInfoTypeType,
    EventSeverityType,
    InstancesHealthAttributeType,
)
from .paginator import (
    DescribeApplicationVersionsPaginator,
    DescribeEnvironmentManagedActionHistoryPaginator,
    DescribeEnvironmentsPaginator,
    DescribeEventsPaginator,
    ListPlatformVersionsPaginator,
)
from .type_defs import (
    ApplicationDescriptionMessageTypeDef,
    ApplicationDescriptionsMessageTypeDef,
    ApplicationResourceLifecycleConfigTypeDef,
    ApplicationResourceLifecycleDescriptionMessageTypeDef,
    ApplicationVersionDescriptionMessageTypeDef,
    ApplicationVersionDescriptionsMessageTypeDef,
    ApplyEnvironmentManagedActionResultTypeDef,
    BuildConfigurationTypeDef,
    CheckDNSAvailabilityResultMessageTypeDef,
    ConfigurationOptionsDescriptionTypeDef,
    ConfigurationOptionSettingTypeDef,
    ConfigurationSettingsDescriptionResponseMetadataTypeDef,
    ConfigurationSettingsDescriptionsTypeDef,
    ConfigurationSettingsValidationMessagesTypeDef,
    CreatePlatformVersionResultTypeDef,
    CreateStorageLocationResultMessageTypeDef,
    DeletePlatformVersionResultTypeDef,
    DescribeAccountAttributesResultTypeDef,
    DescribeEnvironmentHealthResultTypeDef,
    DescribeEnvironmentManagedActionHistoryResultTypeDef,
    DescribeEnvironmentManagedActionsResultTypeDef,
    DescribeInstancesHealthResultTypeDef,
    DescribePlatformVersionResultTypeDef,
    EnvironmentDescriptionResponseMetadataTypeDef,
    EnvironmentDescriptionsMessageTypeDef,
    EnvironmentResourceDescriptionsMessageTypeDef,
    EnvironmentTierTypeDef,
    EventDescriptionsMessageTypeDef,
    ListAvailableSolutionStacksResultMessageTypeDef,
    ListPlatformBranchesResultTypeDef,
    ListPlatformVersionsResultTypeDef,
    OptionSpecificationTypeDef,
    PlatformFilterTypeDef,
    ResourceTagsDescriptionMessageTypeDef,
    RetrieveEnvironmentInfoResultMessageTypeDef,
    S3LocationTypeDef,
    SearchFilterTypeDef,
    SourceBuildInformationTypeDef,
    SourceConfigurationTypeDef,
    TagTypeDef,
)
from .waiter import EnvironmentExistsWaiter, EnvironmentTerminatedWaiter, EnvironmentUpdatedWaiter

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("ElasticBeanstalkClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    CodeBuildNotInServiceRegionException: Type[BotocoreClientError]
    ElasticBeanstalkServiceException: Type[BotocoreClientError]
    InsufficientPrivilegesException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    ManagedActionInvalidStateException: Type[BotocoreClientError]
    OperationInProgressException: Type[BotocoreClientError]
    PlatformVersionStillReferencedException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourceTypeNotSupportedException: Type[BotocoreClientError]
    S3LocationNotInServiceRegionException: Type[BotocoreClientError]
    S3SubscriptionRequiredException: Type[BotocoreClientError]
    SourceBundleDeletionException: Type[BotocoreClientError]
    TooManyApplicationVersionsException: Type[BotocoreClientError]
    TooManyApplicationsException: Type[BotocoreClientError]
    TooManyBucketsException: Type[BotocoreClientError]
    TooManyConfigurationTemplatesException: Type[BotocoreClientError]
    TooManyEnvironmentsException: Type[BotocoreClientError]
    TooManyPlatformsException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]

class ElasticBeanstalkClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ElasticBeanstalkClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#exceptions)
        """
    async def abort_environment_update(
        self, *, EnvironmentId: str = ..., EnvironmentName: str = ...
    ) -> None:
        """
        Cancels in-progress environment configuration update or application version
        deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.abort_environment_update)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#abort_environment_update)
        """
    async def apply_environment_managed_action(
        self, *, ActionId: str, EnvironmentName: str = ..., EnvironmentId: str = ...
    ) -> ApplyEnvironmentManagedActionResultTypeDef:
        """
        Applies a scheduled managed action immediately.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.apply_environment_managed_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#apply_environment_managed_action)
        """
    async def associate_environment_operations_role(
        self, *, EnvironmentName: str, OperationsRole: str
    ) -> None:
        """
        Add or change the operations role used by an environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.associate_environment_operations_role)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#associate_environment_operations_role)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#can_paginate)
        """
    async def check_dns_availability(
        self, *, CNAMEPrefix: str
    ) -> CheckDNSAvailabilityResultMessageTypeDef:
        """
        Checks if the specified CNAME is available.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.check_dns_availability)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#check_dns_availability)
        """
    async def compose_environments(
        self,
        *,
        ApplicationName: str = ...,
        GroupName: str = ...,
        VersionLabels: Sequence[str] = ...
    ) -> EnvironmentDescriptionsMessageTypeDef:
        """
        Create or update a group of environments that each run a separate component of a
        single application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.compose_environments)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#compose_environments)
        """
    async def create_application(
        self,
        *,
        ApplicationName: str,
        Description: str = ...,
        ResourceLifecycleConfig: "ApplicationResourceLifecycleConfigTypeDef" = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> ApplicationDescriptionMessageTypeDef:
        """
        Creates an application that has one configuration template named `default` and
        no application versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.create_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#create_application)
        """
    async def create_application_version(
        self,
        *,
        ApplicationName: str,
        VersionLabel: str,
        Description: str = ...,
        SourceBuildInformation: "SourceBuildInformationTypeDef" = ...,
        SourceBundle: "S3LocationTypeDef" = ...,
        BuildConfiguration: "BuildConfigurationTypeDef" = ...,
        AutoCreateApplication: bool = ...,
        Process: bool = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> ApplicationVersionDescriptionMessageTypeDef:
        """
        Creates an application version for the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.create_application_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#create_application_version)
        """
    async def create_configuration_template(
        self,
        *,
        ApplicationName: str,
        TemplateName: str,
        SolutionStackName: str = ...,
        PlatformArn: str = ...,
        SourceConfiguration: "SourceConfigurationTypeDef" = ...,
        EnvironmentId: str = ...,
        Description: str = ...,
        OptionSettings: Sequence["ConfigurationOptionSettingTypeDef"] = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> ConfigurationSettingsDescriptionResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.create_configuration_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#create_configuration_template)
        """
    async def create_environment(
        self,
        *,
        ApplicationName: str,
        EnvironmentName: str = ...,
        GroupName: str = ...,
        Description: str = ...,
        CNAMEPrefix: str = ...,
        Tier: "EnvironmentTierTypeDef" = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        VersionLabel: str = ...,
        TemplateName: str = ...,
        SolutionStackName: str = ...,
        PlatformArn: str = ...,
        OptionSettings: Sequence["ConfigurationOptionSettingTypeDef"] = ...,
        OptionsToRemove: Sequence["OptionSpecificationTypeDef"] = ...,
        OperationsRole: str = ...
    ) -> EnvironmentDescriptionResponseMetadataTypeDef:
        """
        Launches an AWS Elastic Beanstalk environment for the specified application
        using the specified configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.create_environment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#create_environment)
        """
    async def create_platform_version(
        self,
        *,
        PlatformName: str,
        PlatformVersion: str,
        PlatformDefinitionBundle: "S3LocationTypeDef",
        EnvironmentName: str = ...,
        OptionSettings: Sequence["ConfigurationOptionSettingTypeDef"] = ...,
        Tags: Sequence["TagTypeDef"] = ...
    ) -> CreatePlatformVersionResultTypeDef:
        """
        Create a new version of your custom platform.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.create_platform_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#create_platform_version)
        """
    async def create_storage_location(self) -> CreateStorageLocationResultMessageTypeDef:
        """
        Creates a bucket in Amazon S3 to store application versions, logs, and other
        files used by Elastic Beanstalk environments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.create_storage_location)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#create_storage_location)
        """
    async def delete_application(
        self, *, ApplicationName: str, TerminateEnvByForce: bool = ...
    ) -> None:
        """
        Deletes the specified application along with all associated versions and
        configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.delete_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#delete_application)
        """
    async def delete_application_version(
        self, *, ApplicationName: str, VersionLabel: str, DeleteSourceBundle: bool = ...
    ) -> None:
        """
        Deletes the specified version from the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.delete_application_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#delete_application_version)
        """
    async def delete_configuration_template(
        self, *, ApplicationName: str, TemplateName: str
    ) -> None:
        """
        Deletes the specified configuration template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.delete_configuration_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#delete_configuration_template)
        """
    async def delete_environment_configuration(
        self, *, ApplicationName: str, EnvironmentName: str
    ) -> None:
        """
        Deletes the draft configuration associated with the running environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.delete_environment_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#delete_environment_configuration)
        """
    async def delete_platform_version(
        self, *, PlatformArn: str = ...
    ) -> DeletePlatformVersionResultTypeDef:
        """
        Deletes the specified version of a custom platform.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.delete_platform_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#delete_platform_version)
        """
    async def describe_account_attributes(self) -> DescribeAccountAttributesResultTypeDef:
        """
        Returns attributes related to AWS Elastic Beanstalk that are associated with the
        calling AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.describe_account_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#describe_account_attributes)
        """
    async def describe_application_versions(
        self,
        *,
        ApplicationName: str = ...,
        VersionLabels: Sequence[str] = ...,
        MaxRecords: int = ...,
        NextToken: str = ...
    ) -> ApplicationVersionDescriptionsMessageTypeDef:
        """
        Retrieve a list of application versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.describe_application_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#describe_application_versions)
        """
    async def describe_applications(
        self, *, ApplicationNames: Sequence[str] = ...
    ) -> ApplicationDescriptionsMessageTypeDef:
        """
        Returns the descriptions of existing applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.describe_applications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#describe_applications)
        """
    async def describe_configuration_options(
        self,
        *,
        ApplicationName: str = ...,
        TemplateName: str = ...,
        EnvironmentName: str = ...,
        SolutionStackName: str = ...,
        PlatformArn: str = ...,
        Options: Sequence["OptionSpecificationTypeDef"] = ...
    ) -> ConfigurationOptionsDescriptionTypeDef:
        """
        Describes the configuration options that are used in a particular configuration
        template or environment, or that a specified solution stack defines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.describe_configuration_options)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#describe_configuration_options)
        """
    async def describe_configuration_settings(
        self, *, ApplicationName: str, TemplateName: str = ..., EnvironmentName: str = ...
    ) -> ConfigurationSettingsDescriptionsTypeDef:
        """
        Returns a description of the settings for the specified configuration set, that
        is, either a configuration template or the configuration set associated with a
        running environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.describe_configuration_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#describe_configuration_settings)
        """
    async def describe_environment_health(
        self,
        *,
        EnvironmentName: str = ...,
        EnvironmentId: str = ...,
        AttributeNames: Sequence[EnvironmentHealthAttributeType] = ...
    ) -> DescribeEnvironmentHealthResultTypeDef:
        """
        Returns information about the overall health of the specified environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.describe_environment_health)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#describe_environment_health)
        """
    async def describe_environment_managed_action_history(
        self,
        *,
        EnvironmentId: str = ...,
        EnvironmentName: str = ...,
        NextToken: str = ...,
        MaxItems: int = ...
    ) -> DescribeEnvironmentManagedActionHistoryResultTypeDef:
        """
        Lists an environment's completed and failed managed actions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.describe_environment_managed_action_history)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#describe_environment_managed_action_history)
        """
    async def describe_environment_managed_actions(
        self,
        *,
        EnvironmentName: str = ...,
        EnvironmentId: str = ...,
        Status: ActionStatusType = ...
    ) -> DescribeEnvironmentManagedActionsResultTypeDef:
        """
        Lists an environment's upcoming and in-progress managed actions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.describe_environment_managed_actions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#describe_environment_managed_actions)
        """
    async def describe_environment_resources(
        self, *, EnvironmentId: str = ..., EnvironmentName: str = ...
    ) -> EnvironmentResourceDescriptionsMessageTypeDef:
        """
        Returns AWS resources for this environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.describe_environment_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#describe_environment_resources)
        """
    async def describe_environments(
        self,
        *,
        ApplicationName: str = ...,
        VersionLabel: str = ...,
        EnvironmentIds: Sequence[str] = ...,
        EnvironmentNames: Sequence[str] = ...,
        IncludeDeleted: bool = ...,
        IncludedDeletedBackTo: Union[datetime, str] = ...,
        MaxRecords: int = ...,
        NextToken: str = ...
    ) -> EnvironmentDescriptionsMessageTypeDef:
        """
        Returns descriptions for existing environments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.describe_environments)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#describe_environments)
        """
    async def describe_events(
        self,
        *,
        ApplicationName: str = ...,
        VersionLabel: str = ...,
        TemplateName: str = ...,
        EnvironmentId: str = ...,
        EnvironmentName: str = ...,
        PlatformArn: str = ...,
        RequestId: str = ...,
        Severity: EventSeverityType = ...,
        StartTime: Union[datetime, str] = ...,
        EndTime: Union[datetime, str] = ...,
        MaxRecords: int = ...,
        NextToken: str = ...
    ) -> EventDescriptionsMessageTypeDef:
        """
        Returns list of event descriptions matching criteria up to the last 6 weeks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.describe_events)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#describe_events)
        """
    async def describe_instances_health(
        self,
        *,
        EnvironmentName: str = ...,
        EnvironmentId: str = ...,
        AttributeNames: Sequence[InstancesHealthAttributeType] = ...,
        NextToken: str = ...
    ) -> DescribeInstancesHealthResultTypeDef:
        """
        Retrieves detailed information about the health of instances in your AWS Elastic
        Beanstalk.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.describe_instances_health)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#describe_instances_health)
        """
    async def describe_platform_version(
        self, *, PlatformArn: str = ...
    ) -> DescribePlatformVersionResultTypeDef:
        """
        Describes a platform version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.describe_platform_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#describe_platform_version)
        """
    async def disassociate_environment_operations_role(self, *, EnvironmentName: str) -> None:
        """
        Disassociate the operations role from an environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.disassociate_environment_operations_role)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#disassociate_environment_operations_role)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#generate_presigned_url)
        """
    async def list_available_solution_stacks(
        self,
    ) -> ListAvailableSolutionStacksResultMessageTypeDef:
        """
        Returns a list of the available solution stack names, with the public version
        first and then in reverse chronological order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.list_available_solution_stacks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#list_available_solution_stacks)
        """
    async def list_platform_branches(
        self,
        *,
        Filters: Sequence["SearchFilterTypeDef"] = ...,
        MaxRecords: int = ...,
        NextToken: str = ...
    ) -> ListPlatformBranchesResultTypeDef:
        """
        Lists the platform branches available for your account in an AWS Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.list_platform_branches)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#list_platform_branches)
        """
    async def list_platform_versions(
        self,
        *,
        Filters: Sequence["PlatformFilterTypeDef"] = ...,
        MaxRecords: int = ...,
        NextToken: str = ...
    ) -> ListPlatformVersionsResultTypeDef:
        """
        Lists the platform versions available for your account in an AWS Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.list_platform_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#list_platform_versions)
        """
    async def list_tags_for_resource(
        self, *, ResourceArn: str
    ) -> ResourceTagsDescriptionMessageTypeDef:
        """
        Return the tags applied to an AWS Elastic Beanstalk resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#list_tags_for_resource)
        """
    async def rebuild_environment(
        self, *, EnvironmentId: str = ..., EnvironmentName: str = ...
    ) -> None:
        """
        Deletes and recreates all of the AWS resources (for example: the Auto Scaling
        group, load balancer, etc.) for a specified environment and forces a restart.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.rebuild_environment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#rebuild_environment)
        """
    async def request_environment_info(
        self,
        *,
        InfoType: EnvironmentInfoTypeType,
        EnvironmentId: str = ...,
        EnvironmentName: str = ...
    ) -> None:
        """
        Initiates a request to compile the specified type of information of the deployed
        environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.request_environment_info)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#request_environment_info)
        """
    async def restart_app_server(
        self, *, EnvironmentId: str = ..., EnvironmentName: str = ...
    ) -> None:
        """
        Causes the environment to restart the application container server running on
        each Amazon EC2 instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.restart_app_server)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#restart_app_server)
        """
    async def retrieve_environment_info(
        self,
        *,
        InfoType: EnvironmentInfoTypeType,
        EnvironmentId: str = ...,
        EnvironmentName: str = ...
    ) -> RetrieveEnvironmentInfoResultMessageTypeDef:
        """
        Retrieves the compiled information from a  RequestEnvironmentInfo request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.retrieve_environment_info)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#retrieve_environment_info)
        """
    async def swap_environment_cnames(
        self,
        *,
        SourceEnvironmentId: str = ...,
        SourceEnvironmentName: str = ...,
        DestinationEnvironmentId: str = ...,
        DestinationEnvironmentName: str = ...
    ) -> None:
        """
        Swaps the CNAMEs of two environments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.swap_environment_cnames)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#swap_environment_cnames)
        """
    async def terminate_environment(
        self,
        *,
        EnvironmentId: str = ...,
        EnvironmentName: str = ...,
        TerminateResources: bool = ...,
        ForceTerminate: bool = ...
    ) -> EnvironmentDescriptionResponseMetadataTypeDef:
        """
        Terminates the specified environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.terminate_environment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#terminate_environment)
        """
    async def update_application(
        self, *, ApplicationName: str, Description: str = ...
    ) -> ApplicationDescriptionMessageTypeDef:
        """
        Updates the specified application to have the specified properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.update_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#update_application)
        """
    async def update_application_resource_lifecycle(
        self,
        *,
        ApplicationName: str,
        ResourceLifecycleConfig: "ApplicationResourceLifecycleConfigTypeDef"
    ) -> ApplicationResourceLifecycleDescriptionMessageTypeDef:
        """
        Modifies lifecycle settings for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.update_application_resource_lifecycle)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#update_application_resource_lifecycle)
        """
    async def update_application_version(
        self, *, ApplicationName: str, VersionLabel: str, Description: str = ...
    ) -> ApplicationVersionDescriptionMessageTypeDef:
        """
        Updates the specified application version to have the specified properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.update_application_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#update_application_version)
        """
    async def update_configuration_template(
        self,
        *,
        ApplicationName: str,
        TemplateName: str,
        Description: str = ...,
        OptionSettings: Sequence["ConfigurationOptionSettingTypeDef"] = ...,
        OptionsToRemove: Sequence["OptionSpecificationTypeDef"] = ...
    ) -> ConfigurationSettingsDescriptionResponseMetadataTypeDef:
        """
        Updates the specified configuration template to have the specified properties or
        configuration option values.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.update_configuration_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#update_configuration_template)
        """
    async def update_environment(
        self,
        *,
        ApplicationName: str = ...,
        EnvironmentId: str = ...,
        EnvironmentName: str = ...,
        GroupName: str = ...,
        Description: str = ...,
        Tier: "EnvironmentTierTypeDef" = ...,
        VersionLabel: str = ...,
        TemplateName: str = ...,
        SolutionStackName: str = ...,
        PlatformArn: str = ...,
        OptionSettings: Sequence["ConfigurationOptionSettingTypeDef"] = ...,
        OptionsToRemove: Sequence["OptionSpecificationTypeDef"] = ...
    ) -> EnvironmentDescriptionResponseMetadataTypeDef:
        """
        Updates the environment description, deploys a new application version, updates
        the configuration settings to an entirely new configuration template, or updates
        select configuration option values in the running environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.update_environment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#update_environment)
        """
    async def update_tags_for_resource(
        self,
        *,
        ResourceArn: str,
        TagsToAdd: Sequence["TagTypeDef"] = ...,
        TagsToRemove: Sequence[str] = ...
    ) -> None:
        """
        Update the list of tags applied to an AWS Elastic Beanstalk resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.update_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#update_tags_for_resource)
        """
    async def validate_configuration_settings(
        self,
        *,
        ApplicationName: str,
        OptionSettings: Sequence["ConfigurationOptionSettingTypeDef"],
        TemplateName: str = ...,
        EnvironmentName: str = ...
    ) -> ConfigurationSettingsValidationMessagesTypeDef:
        """
        Takes a set of configuration settings and either a configuration template or
        environment, and determines whether those values are valid.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.validate_configuration_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#validate_configuration_settings)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["describe_application_versions"]
    ) -> DescribeApplicationVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["describe_environment_managed_action_history"]
    ) -> DescribeEnvironmentManagedActionHistoryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["describe_environments"]
    ) -> DescribeEnvironmentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["describe_events"]) -> DescribeEventsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_platform_versions"]
    ) -> ListPlatformVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#get_paginator)
        """
    @overload
    def get_waiter(self, waiter_name: Literal["environment_exists"]) -> EnvironmentExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#get_waiter)
        """
    @overload
    def get_waiter(
        self, waiter_name: Literal["environment_terminated"]
    ) -> EnvironmentTerminatedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#get_waiter)
        """
    @overload
    def get_waiter(self, waiter_name: Literal["environment_updated"]) -> EnvironmentUpdatedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/#get_waiter)
        """
    async def __aenter__(self) -> "ElasticBeanstalkClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticbeanstalk.html#ElasticBeanstalk.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticbeanstalk/client/)
        """
