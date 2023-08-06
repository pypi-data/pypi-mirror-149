"""
Type annotations for proton service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_proton.client import ProtonClient

    session = get_session()
    async with session.create_client("proton") as client:
        client: ProtonClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    DeploymentUpdateTypeType,
    EnvironmentAccountConnectionRequesterAccountTypeType,
    EnvironmentAccountConnectionStatusType,
    RepositoryProviderType,
    ResourceDeploymentStatusType,
    TemplateTypeType,
    TemplateVersionStatusType,
)
from .paginator import (
    ListEnvironmentAccountConnectionsPaginator,
    ListEnvironmentOutputsPaginator,
    ListEnvironmentProvisionedResourcesPaginator,
    ListEnvironmentsPaginator,
    ListEnvironmentTemplatesPaginator,
    ListEnvironmentTemplateVersionsPaginator,
    ListRepositoriesPaginator,
    ListRepositorySyncDefinitionsPaginator,
    ListServiceInstanceOutputsPaginator,
    ListServiceInstanceProvisionedResourcesPaginator,
    ListServiceInstancesPaginator,
    ListServicePipelineOutputsPaginator,
    ListServicePipelineProvisionedResourcesPaginator,
    ListServicesPaginator,
    ListServiceTemplatesPaginator,
    ListServiceTemplateVersionsPaginator,
    ListTagsForResourcePaginator,
)
from .type_defs import (
    AcceptEnvironmentAccountConnectionOutputTypeDef,
    CancelEnvironmentDeploymentOutputTypeDef,
    CancelServiceInstanceDeploymentOutputTypeDef,
    CancelServicePipelineDeploymentOutputTypeDef,
    CompatibleEnvironmentTemplateInputTypeDef,
    CreateEnvironmentAccountConnectionOutputTypeDef,
    CreateEnvironmentOutputTypeDef,
    CreateEnvironmentTemplateOutputTypeDef,
    CreateEnvironmentTemplateVersionOutputTypeDef,
    CreateRepositoryOutputTypeDef,
    CreateServiceOutputTypeDef,
    CreateServiceTemplateOutputTypeDef,
    CreateServiceTemplateVersionOutputTypeDef,
    CreateTemplateSyncConfigOutputTypeDef,
    DeleteEnvironmentAccountConnectionOutputTypeDef,
    DeleteEnvironmentOutputTypeDef,
    DeleteEnvironmentTemplateOutputTypeDef,
    DeleteEnvironmentTemplateVersionOutputTypeDef,
    DeleteRepositoryOutputTypeDef,
    DeleteServiceOutputTypeDef,
    DeleteServiceTemplateOutputTypeDef,
    DeleteServiceTemplateVersionOutputTypeDef,
    DeleteTemplateSyncConfigOutputTypeDef,
    EnvironmentTemplateFilterTypeDef,
    GetAccountSettingsOutputTypeDef,
    GetEnvironmentAccountConnectionOutputTypeDef,
    GetEnvironmentOutputTypeDef,
    GetEnvironmentTemplateOutputTypeDef,
    GetEnvironmentTemplateVersionOutputTypeDef,
    GetRepositoryOutputTypeDef,
    GetRepositorySyncStatusOutputTypeDef,
    GetServiceInstanceOutputTypeDef,
    GetServiceOutputTypeDef,
    GetServiceTemplateOutputTypeDef,
    GetServiceTemplateVersionOutputTypeDef,
    GetTemplateSyncConfigOutputTypeDef,
    GetTemplateSyncStatusOutputTypeDef,
    ListEnvironmentAccountConnectionsOutputTypeDef,
    ListEnvironmentOutputsOutputTypeDef,
    ListEnvironmentProvisionedResourcesOutputTypeDef,
    ListEnvironmentsOutputTypeDef,
    ListEnvironmentTemplatesOutputTypeDef,
    ListEnvironmentTemplateVersionsOutputTypeDef,
    ListRepositoriesOutputTypeDef,
    ListRepositorySyncDefinitionsOutputTypeDef,
    ListServiceInstanceOutputsOutputTypeDef,
    ListServiceInstanceProvisionedResourcesOutputTypeDef,
    ListServiceInstancesOutputTypeDef,
    ListServicePipelineOutputsOutputTypeDef,
    ListServicePipelineProvisionedResourcesOutputTypeDef,
    ListServicesOutputTypeDef,
    ListServiceTemplatesOutputTypeDef,
    ListServiceTemplateVersionsOutputTypeDef,
    ListTagsForResourceOutputTypeDef,
    OutputTypeDef,
    RejectEnvironmentAccountConnectionOutputTypeDef,
    RepositoryBranchInputTypeDef,
    TagTypeDef,
    TemplateVersionSourceInputTypeDef,
    UpdateAccountSettingsOutputTypeDef,
    UpdateEnvironmentAccountConnectionOutputTypeDef,
    UpdateEnvironmentOutputTypeDef,
    UpdateEnvironmentTemplateOutputTypeDef,
    UpdateEnvironmentTemplateVersionOutputTypeDef,
    UpdateServiceInstanceOutputTypeDef,
    UpdateServiceOutputTypeDef,
    UpdateServicePipelineOutputTypeDef,
    UpdateServiceTemplateOutputTypeDef,
    UpdateServiceTemplateVersionOutputTypeDef,
    UpdateTemplateSyncConfigOutputTypeDef,
)
from .waiter import (
    EnvironmentDeployedWaiter,
    EnvironmentTemplateVersionRegisteredWaiter,
    ServiceCreatedWaiter,
    ServiceDeletedWaiter,
    ServiceInstanceDeployedWaiter,
    ServicePipelineDeployedWaiter,
    ServiceTemplateVersionRegisteredWaiter,
    ServiceUpdatedWaiter,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("ProtonClient",)

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
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class ProtonClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ProtonClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#exceptions)
        """
    async def accept_environment_account_connection(
        self, *, id: str
    ) -> AcceptEnvironmentAccountConnectionOutputTypeDef:
        """
        In a management account, an environment account connection request is accepted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.accept_environment_account_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#accept_environment_account_connection)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#can_paginate)
        """
    async def cancel_environment_deployment(
        self, *, environmentName: str
    ) -> CancelEnvironmentDeploymentOutputTypeDef:
        """
        Attempts to cancel an environment deployment on an  UpdateEnvironment action, if
        the deployment is `IN_PROGRESS`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.cancel_environment_deployment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#cancel_environment_deployment)
        """
    async def cancel_service_instance_deployment(
        self, *, serviceInstanceName: str, serviceName: str
    ) -> CancelServiceInstanceDeploymentOutputTypeDef:
        """
        Attempts to cancel a service instance deployment on an  UpdateServiceInstance
        action, if the deployment is `IN_PROGRESS`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.cancel_service_instance_deployment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#cancel_service_instance_deployment)
        """
    async def cancel_service_pipeline_deployment(
        self, *, serviceName: str
    ) -> CancelServicePipelineDeploymentOutputTypeDef:
        """
        Attempts to cancel a service pipeline deployment on an  UpdateServicePipeline
        action, if the deployment is `IN_PROGRESS`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.cancel_service_pipeline_deployment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#cancel_service_pipeline_deployment)
        """
    async def create_environment(
        self,
        *,
        name: str,
        spec: str,
        templateMajorVersion: str,
        templateName: str,
        description: str = ...,
        environmentAccountConnectionId: str = ...,
        protonServiceRoleArn: str = ...,
        provisioningRepository: "RepositoryBranchInputTypeDef" = ...,
        tags: Sequence["TagTypeDef"] = ...,
        templateMinorVersion: str = ...
    ) -> CreateEnvironmentOutputTypeDef:
        """
        Deploy a new environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.create_environment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#create_environment)
        """
    async def create_environment_account_connection(
        self,
        *,
        environmentName: str,
        managementAccountId: str,
        roleArn: str,
        clientToken: str = ...,
        tags: Sequence["TagTypeDef"] = ...
    ) -> CreateEnvironmentAccountConnectionOutputTypeDef:
        """
        Create an environment account connection in an environment account so that
        environment infrastructure resources can be provisioned in the environment
        account from a management account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.create_environment_account_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#create_environment_account_connection)
        """
    async def create_environment_template(
        self,
        *,
        name: str,
        description: str = ...,
        displayName: str = ...,
        encryptionKey: str = ...,
        provisioning: Literal["CUSTOMER_MANAGED"] = ...,
        tags: Sequence["TagTypeDef"] = ...
    ) -> CreateEnvironmentTemplateOutputTypeDef:
        """
        Create an environment template for Proton.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.create_environment_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#create_environment_template)
        """
    async def create_environment_template_version(
        self,
        *,
        source: "TemplateVersionSourceInputTypeDef",
        templateName: str,
        clientToken: str = ...,
        description: str = ...,
        majorVersion: str = ...,
        tags: Sequence["TagTypeDef"] = ...
    ) -> CreateEnvironmentTemplateVersionOutputTypeDef:
        """
        Create a new major or minor version of an environment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.create_environment_template_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#create_environment_template_version)
        """
    async def create_repository(
        self,
        *,
        connectionArn: str,
        name: str,
        provider: RepositoryProviderType,
        encryptionKey: str = ...
    ) -> CreateRepositoryOutputTypeDef:
        """
        Create and register a link to a repository that can be used with pull request
        provisioning or template sync configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.create_repository)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#create_repository)
        """
    async def create_service(
        self,
        *,
        name: str,
        spec: str,
        templateMajorVersion: str,
        templateName: str,
        branchName: str = ...,
        description: str = ...,
        repositoryConnectionArn: str = ...,
        repositoryId: str = ...,
        tags: Sequence["TagTypeDef"] = ...,
        templateMinorVersion: str = ...
    ) -> CreateServiceOutputTypeDef:
        """
        Create an Proton service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.create_service)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#create_service)
        """
    async def create_service_template(
        self,
        *,
        name: str,
        description: str = ...,
        displayName: str = ...,
        encryptionKey: str = ...,
        pipelineProvisioning: Literal["CUSTOMER_MANAGED"] = ...,
        tags: Sequence["TagTypeDef"] = ...
    ) -> CreateServiceTemplateOutputTypeDef:
        """
        Create a service template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.create_service_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#create_service_template)
        """
    async def create_service_template_version(
        self,
        *,
        compatibleEnvironmentTemplates: Sequence["CompatibleEnvironmentTemplateInputTypeDef"],
        source: "TemplateVersionSourceInputTypeDef",
        templateName: str,
        clientToken: str = ...,
        description: str = ...,
        majorVersion: str = ...,
        tags: Sequence["TagTypeDef"] = ...
    ) -> CreateServiceTemplateVersionOutputTypeDef:
        """
        Create a new major or minor version of a service template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.create_service_template_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#create_service_template_version)
        """
    async def create_template_sync_config(
        self,
        *,
        branch: str,
        repositoryName: str,
        repositoryProvider: RepositoryProviderType,
        templateName: str,
        templateType: TemplateTypeType,
        subdirectory: str = ...
    ) -> CreateTemplateSyncConfigOutputTypeDef:
        """
        Set up a template for automated template version creation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.create_template_sync_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#create_template_sync_config)
        """
    async def delete_environment(self, *, name: str) -> DeleteEnvironmentOutputTypeDef:
        """
        Delete an environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.delete_environment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#delete_environment)
        """
    async def delete_environment_account_connection(
        self, *, id: str
    ) -> DeleteEnvironmentAccountConnectionOutputTypeDef:
        """
        In an environment account, delete an environment account connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.delete_environment_account_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#delete_environment_account_connection)
        """
    async def delete_environment_template(
        self, *, name: str
    ) -> DeleteEnvironmentTemplateOutputTypeDef:
        """
        If no other major or minor versions of an environment template exist, delete the
        environment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.delete_environment_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#delete_environment_template)
        """
    async def delete_environment_template_version(
        self, *, majorVersion: str, minorVersion: str, templateName: str
    ) -> DeleteEnvironmentTemplateVersionOutputTypeDef:
        """
        If no other minor versions of an environment template exist, delete a major
        version of the environment template if it's not the `Recommended` version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.delete_environment_template_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#delete_environment_template_version)
        """
    async def delete_repository(
        self, *, name: str, provider: RepositoryProviderType
    ) -> DeleteRepositoryOutputTypeDef:
        """
        De-register and unlink your repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.delete_repository)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#delete_repository)
        """
    async def delete_service(self, *, name: str) -> DeleteServiceOutputTypeDef:
        """
        Delete a service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.delete_service)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#delete_service)
        """
    async def delete_service_template(self, *, name: str) -> DeleteServiceTemplateOutputTypeDef:
        """
        If no other major or minor versions of the service template exist, delete the
        service template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.delete_service_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#delete_service_template)
        """
    async def delete_service_template_version(
        self, *, majorVersion: str, minorVersion: str, templateName: str
    ) -> DeleteServiceTemplateVersionOutputTypeDef:
        """
        If no other minor versions of a service template exist, delete a major version
        of the service template if it's not the `Recommended` version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.delete_service_template_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#delete_service_template_version)
        """
    async def delete_template_sync_config(
        self, *, templateName: str, templateType: TemplateTypeType
    ) -> DeleteTemplateSyncConfigOutputTypeDef:
        """
        Delete a template sync configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.delete_template_sync_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#delete_template_sync_config)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#generate_presigned_url)
        """
    async def get_account_settings(self) -> GetAccountSettingsOutputTypeDef:
        """
        Get detail data for the Proton pipeline service role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_account_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_account_settings)
        """
    async def get_environment(self, *, name: str) -> GetEnvironmentOutputTypeDef:
        """
        Get detail data for an environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_environment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_environment)
        """
    async def get_environment_account_connection(
        self, *, id: str
    ) -> GetEnvironmentAccountConnectionOutputTypeDef:
        """
        In an environment account, view the detail data for an environment account
        connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_environment_account_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_environment_account_connection)
        """
    async def get_environment_template(self, *, name: str) -> GetEnvironmentTemplateOutputTypeDef:
        """
        Get detail data for an environment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_environment_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_environment_template)
        """
    async def get_environment_template_version(
        self, *, majorVersion: str, minorVersion: str, templateName: str
    ) -> GetEnvironmentTemplateVersionOutputTypeDef:
        """
        View detail data for a major or minor version of an environment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_environment_template_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_environment_template_version)
        """
    async def get_repository(
        self, *, name: str, provider: RepositoryProviderType
    ) -> GetRepositoryOutputTypeDef:
        """
        Get detail data for a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_repository)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_repository)
        """
    async def get_repository_sync_status(
        self,
        *,
        branch: str,
        repositoryName: str,
        repositoryProvider: RepositoryProviderType,
        syncType: Literal["TEMPLATE_SYNC"]
    ) -> GetRepositorySyncStatusOutputTypeDef:
        """
        Get the repository sync status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_repository_sync_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_repository_sync_status)
        """
    async def get_service(self, *, name: str) -> GetServiceOutputTypeDef:
        """
        Get detail data for a service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_service)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_service)
        """
    async def get_service_instance(
        self, *, name: str, serviceName: str
    ) -> GetServiceInstanceOutputTypeDef:
        """
        Get detail data for a service instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_service_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_service_instance)
        """
    async def get_service_template(self, *, name: str) -> GetServiceTemplateOutputTypeDef:
        """
        Get detail data for a service template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_service_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_service_template)
        """
    async def get_service_template_version(
        self, *, majorVersion: str, minorVersion: str, templateName: str
    ) -> GetServiceTemplateVersionOutputTypeDef:
        """
        View detail data for a major or minor version of a service template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_service_template_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_service_template_version)
        """
    async def get_template_sync_config(
        self, *, templateName: str, templateType: TemplateTypeType
    ) -> GetTemplateSyncConfigOutputTypeDef:
        """
        Get detail data for a template sync configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_template_sync_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_template_sync_config)
        """
    async def get_template_sync_status(
        self, *, templateName: str, templateType: TemplateTypeType, templateVersion: str
    ) -> GetTemplateSyncStatusOutputTypeDef:
        """
        Get the status of a template sync.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_template_sync_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_template_sync_status)
        """
    async def list_environment_account_connections(
        self,
        *,
        requestedBy: EnvironmentAccountConnectionRequesterAccountTypeType,
        environmentName: str = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        statuses: Sequence[EnvironmentAccountConnectionStatusType] = ...
    ) -> ListEnvironmentAccountConnectionsOutputTypeDef:
        """
        View a list of environment account connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_environment_account_connections)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_environment_account_connections)
        """
    async def list_environment_outputs(
        self, *, environmentName: str, nextToken: str = ...
    ) -> ListEnvironmentOutputsOutputTypeDef:
        """
        List the infrastructure as code outputs for your environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_environment_outputs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_environment_outputs)
        """
    async def list_environment_provisioned_resources(
        self, *, environmentName: str, nextToken: str = ...
    ) -> ListEnvironmentProvisionedResourcesOutputTypeDef:
        """
        List the provisioned resources for your environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_environment_provisioned_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_environment_provisioned_resources)
        """
    async def list_environment_template_versions(
        self,
        *,
        templateName: str,
        majorVersion: str = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListEnvironmentTemplateVersionsOutputTypeDef:
        """
        List major or minor versions of an environment template with detail data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_environment_template_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_environment_template_versions)
        """
    async def list_environment_templates(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListEnvironmentTemplatesOutputTypeDef:
        """
        List environment templates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_environment_templates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_environment_templates)
        """
    async def list_environments(
        self,
        *,
        environmentTemplates: Sequence["EnvironmentTemplateFilterTypeDef"] = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListEnvironmentsOutputTypeDef:
        """
        List environments with detail data summaries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_environments)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_environments)
        """
    async def list_repositories(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListRepositoriesOutputTypeDef:
        """
        List repositories with detail data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_repositories)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_repositories)
        """
    async def list_repository_sync_definitions(
        self,
        *,
        repositoryName: str,
        repositoryProvider: RepositoryProviderType,
        syncType: Literal["TEMPLATE_SYNC"],
        nextToken: str = ...
    ) -> ListRepositorySyncDefinitionsOutputTypeDef:
        """
        List repository sync definitions with detail data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_repository_sync_definitions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_repository_sync_definitions)
        """
    async def list_service_instance_outputs(
        self, *, serviceInstanceName: str, serviceName: str, nextToken: str = ...
    ) -> ListServiceInstanceOutputsOutputTypeDef:
        """
        View a list service instance infrastructure as code outputs with detail data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_service_instance_outputs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_service_instance_outputs)
        """
    async def list_service_instance_provisioned_resources(
        self, *, serviceInstanceName: str, serviceName: str, nextToken: str = ...
    ) -> ListServiceInstanceProvisionedResourcesOutputTypeDef:
        """
        List provisioned resources for a service instance with details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_service_instance_provisioned_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_service_instance_provisioned_resources)
        """
    async def list_service_instances(
        self, *, maxResults: int = ..., nextToken: str = ..., serviceName: str = ...
    ) -> ListServiceInstancesOutputTypeDef:
        """
        List service instances with summaries of detail data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_service_instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_service_instances)
        """
    async def list_service_pipeline_outputs(
        self, *, serviceName: str, nextToken: str = ...
    ) -> ListServicePipelineOutputsOutputTypeDef:
        """
        View a list service pipeline infrastructure as code outputs with detail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_service_pipeline_outputs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_service_pipeline_outputs)
        """
    async def list_service_pipeline_provisioned_resources(
        self, *, serviceName: str, nextToken: str = ...
    ) -> ListServicePipelineProvisionedResourcesOutputTypeDef:
        """
        List provisioned resources for a service and pipeline with details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_service_pipeline_provisioned_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_service_pipeline_provisioned_resources)
        """
    async def list_service_template_versions(
        self,
        *,
        templateName: str,
        majorVersion: str = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListServiceTemplateVersionsOutputTypeDef:
        """
        List major or minor versions of a service template with detail data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_service_template_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_service_template_versions)
        """
    async def list_service_templates(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListServiceTemplatesOutputTypeDef:
        """
        List service templates with detail data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_service_templates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_service_templates)
        """
    async def list_services(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListServicesOutputTypeDef:
        """
        List services with summaries of detail data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_services)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_services)
        """
    async def list_tags_for_resource(
        self, *, resourceArn: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListTagsForResourceOutputTypeDef:
        """
        List tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_tags_for_resource)
        """
    async def notify_resource_deployment_status_change(
        self,
        *,
        resourceArn: str,
        status: ResourceDeploymentStatusType,
        deploymentId: str = ...,
        outputs: Sequence["OutputTypeDef"] = ...,
        statusMessage: str = ...
    ) -> Dict[str, Any]:
        """
        Notify Proton of status changes to a provisioned resource when you use pull
        request provisioning.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.notify_resource_deployment_status_change)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#notify_resource_deployment_status_change)
        """
    async def reject_environment_account_connection(
        self, *, id: str
    ) -> RejectEnvironmentAccountConnectionOutputTypeDef:
        """
        In a management account, reject an environment account connection from another
        environment account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.reject_environment_account_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#reject_environment_account_connection)
        """
    async def tag_resource(
        self, *, resourceArn: str, tags: Sequence["TagTypeDef"]
    ) -> Dict[str, Any]:
        """
        Tag a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#tag_resource)
        """
    async def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Remove a tag from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#untag_resource)
        """
    async def update_account_settings(
        self,
        *,
        pipelineProvisioningRepository: "RepositoryBranchInputTypeDef" = ...,
        pipelineServiceRoleArn: str = ...
    ) -> UpdateAccountSettingsOutputTypeDef:
        """
        Update the Proton service pipeline role or repository settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.update_account_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#update_account_settings)
        """
    async def update_environment(
        self,
        *,
        deploymentType: DeploymentUpdateTypeType,
        name: str,
        description: str = ...,
        environmentAccountConnectionId: str = ...,
        protonServiceRoleArn: str = ...,
        provisioningRepository: "RepositoryBranchInputTypeDef" = ...,
        spec: str = ...,
        templateMajorVersion: str = ...,
        templateMinorVersion: str = ...
    ) -> UpdateEnvironmentOutputTypeDef:
        """
        Update an environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.update_environment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#update_environment)
        """
    async def update_environment_account_connection(
        self, *, id: str, roleArn: str
    ) -> UpdateEnvironmentAccountConnectionOutputTypeDef:
        """
        In an environment account, update an environment account connection to use a new
        IAM role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.update_environment_account_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#update_environment_account_connection)
        """
    async def update_environment_template(
        self, *, name: str, description: str = ..., displayName: str = ...
    ) -> UpdateEnvironmentTemplateOutputTypeDef:
        """
        Update an environment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.update_environment_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#update_environment_template)
        """
    async def update_environment_template_version(
        self,
        *,
        majorVersion: str,
        minorVersion: str,
        templateName: str,
        description: str = ...,
        status: TemplateVersionStatusType = ...
    ) -> UpdateEnvironmentTemplateVersionOutputTypeDef:
        """
        Update a major or minor version of an environment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.update_environment_template_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#update_environment_template_version)
        """
    async def update_service(
        self, *, name: str, description: str = ..., spec: str = ...
    ) -> UpdateServiceOutputTypeDef:
        """
        Edit a service description or use a spec to add and delete service instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.update_service)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#update_service)
        """
    async def update_service_instance(
        self,
        *,
        deploymentType: DeploymentUpdateTypeType,
        name: str,
        serviceName: str,
        spec: str = ...,
        templateMajorVersion: str = ...,
        templateMinorVersion: str = ...
    ) -> UpdateServiceInstanceOutputTypeDef:
        """
        Update a service instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.update_service_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#update_service_instance)
        """
    async def update_service_pipeline(
        self,
        *,
        deploymentType: DeploymentUpdateTypeType,
        serviceName: str,
        spec: str,
        templateMajorVersion: str = ...,
        templateMinorVersion: str = ...
    ) -> UpdateServicePipelineOutputTypeDef:
        """
        Update the service pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.update_service_pipeline)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#update_service_pipeline)
        """
    async def update_service_template(
        self, *, name: str, description: str = ..., displayName: str = ...
    ) -> UpdateServiceTemplateOutputTypeDef:
        """
        Update a service template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.update_service_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#update_service_template)
        """
    async def update_service_template_version(
        self,
        *,
        majorVersion: str,
        minorVersion: str,
        templateName: str,
        compatibleEnvironmentTemplates: Sequence["CompatibleEnvironmentTemplateInputTypeDef"] = ...,
        description: str = ...,
        status: TemplateVersionStatusType = ...
    ) -> UpdateServiceTemplateVersionOutputTypeDef:
        """
        Update a major or minor version of a service template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.update_service_template_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#update_service_template_version)
        """
    async def update_template_sync_config(
        self,
        *,
        branch: str,
        repositoryName: str,
        repositoryProvider: RepositoryProviderType,
        templateName: str,
        templateType: TemplateTypeType,
        subdirectory: str = ...
    ) -> UpdateTemplateSyncConfigOutputTypeDef:
        """
        Update template sync configuration parameters, except for the `templateName` and
        `templateType` .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.update_template_sync_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#update_template_sync_config)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_environment_account_connections"]
    ) -> ListEnvironmentAccountConnectionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_environment_outputs"]
    ) -> ListEnvironmentOutputsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_environment_provisioned_resources"]
    ) -> ListEnvironmentProvisionedResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_environment_template_versions"]
    ) -> ListEnvironmentTemplateVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_environment_templates"]
    ) -> ListEnvironmentTemplatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_environments"]
    ) -> ListEnvironmentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_repositories"]
    ) -> ListRepositoriesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_repository_sync_definitions"]
    ) -> ListRepositorySyncDefinitionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_instance_outputs"]
    ) -> ListServiceInstanceOutputsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_instance_provisioned_resources"]
    ) -> ListServiceInstanceProvisionedResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_instances"]
    ) -> ListServiceInstancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_pipeline_outputs"]
    ) -> ListServicePipelineOutputsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_pipeline_provisioned_resources"]
    ) -> ListServicePipelineProvisionedResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_template_versions"]
    ) -> ListServiceTemplateVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_service_templates"]
    ) -> ListServiceTemplatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_services"]) -> ListServicesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """
    @overload
    def get_waiter(self, waiter_name: Literal["environment_deployed"]) -> EnvironmentDeployedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_waiter)
        """
    @overload
    def get_waiter(
        self, waiter_name: Literal["environment_template_version_registered"]
    ) -> EnvironmentTemplateVersionRegisteredWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_waiter)
        """
    @overload
    def get_waiter(self, waiter_name: Literal["service_created"]) -> ServiceCreatedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_waiter)
        """
    @overload
    def get_waiter(self, waiter_name: Literal["service_deleted"]) -> ServiceDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_waiter)
        """
    @overload
    def get_waiter(
        self, waiter_name: Literal["service_instance_deployed"]
    ) -> ServiceInstanceDeployedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_waiter)
        """
    @overload
    def get_waiter(
        self, waiter_name: Literal["service_pipeline_deployed"]
    ) -> ServicePipelineDeployedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_waiter)
        """
    @overload
    def get_waiter(
        self, waiter_name: Literal["service_template_version_registered"]
    ) -> ServiceTemplateVersionRegisteredWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_waiter)
        """
    @overload
    def get_waiter(self, waiter_name: Literal["service_updated"]) -> ServiceUpdatedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_waiter)
        """
    async def __aenter__(self) -> "ProtonClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/)
        """
