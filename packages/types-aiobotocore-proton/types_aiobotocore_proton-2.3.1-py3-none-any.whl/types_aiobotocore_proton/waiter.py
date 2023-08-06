"""
Type annotations for proton service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_proton.client import ProtonClient
    from types_aiobotocore_proton.waiter import (
        EnvironmentDeployedWaiter,
        EnvironmentTemplateVersionRegisteredWaiter,
        ServiceCreatedWaiter,
        ServiceDeletedWaiter,
        ServiceInstanceDeployedWaiter,
        ServicePipelineDeployedWaiter,
        ServiceTemplateVersionRegisteredWaiter,
        ServiceUpdatedWaiter,
    )

    session = get_session()
    async with session.create_client("proton") as client:
        client: ProtonClient

        environment_deployed_waiter: EnvironmentDeployedWaiter = client.get_waiter("environment_deployed")
        environment_template_version_registered_waiter: EnvironmentTemplateVersionRegisteredWaiter = client.get_waiter("environment_template_version_registered")
        service_created_waiter: ServiceCreatedWaiter = client.get_waiter("service_created")
        service_deleted_waiter: ServiceDeletedWaiter = client.get_waiter("service_deleted")
        service_instance_deployed_waiter: ServiceInstanceDeployedWaiter = client.get_waiter("service_instance_deployed")
        service_pipeline_deployed_waiter: ServicePipelineDeployedWaiter = client.get_waiter("service_pipeline_deployed")
        service_template_version_registered_waiter: ServiceTemplateVersionRegisteredWaiter = client.get_waiter("service_template_version_registered")
        service_updated_waiter: ServiceUpdatedWaiter = client.get_waiter("service_updated")
    ```
"""
from aiobotocore.waiter import AIOWaiter

from .type_defs import WaiterConfigTypeDef

__all__ = (
    "EnvironmentDeployedWaiter",
    "EnvironmentTemplateVersionRegisteredWaiter",
    "ServiceCreatedWaiter",
    "ServiceDeletedWaiter",
    "ServiceInstanceDeployedWaiter",
    "ServicePipelineDeployedWaiter",
    "ServiceTemplateVersionRegisteredWaiter",
    "ServiceUpdatedWaiter",
)


class EnvironmentDeployedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Waiter.EnvironmentDeployed)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#environmentdeployedwaiter)
    """

    async def wait(self, *, name: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Waiter.EnvironmentDeployed.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#environmentdeployedwaiter)
        """


class EnvironmentTemplateVersionRegisteredWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Waiter.EnvironmentTemplateVersionRegistered)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#environmenttemplateversionregisteredwaiter)
    """

    async def wait(
        self,
        *,
        majorVersion: str,
        minorVersion: str,
        templateName: str,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Waiter.EnvironmentTemplateVersionRegistered.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#environmenttemplateversionregisteredwaiter)
        """


class ServiceCreatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Waiter.ServiceCreated)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#servicecreatedwaiter)
    """

    async def wait(self, *, name: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Waiter.ServiceCreated.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#servicecreatedwaiter)
        """


class ServiceDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Waiter.ServiceDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#servicedeletedwaiter)
    """

    async def wait(self, *, name: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Waiter.ServiceDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#servicedeletedwaiter)
        """


class ServiceInstanceDeployedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Waiter.ServiceInstanceDeployed)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#serviceinstancedeployedwaiter)
    """

    async def wait(
        self, *, name: str, serviceName: str, WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Waiter.ServiceInstanceDeployed.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#serviceinstancedeployedwaiter)
        """


class ServicePipelineDeployedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Waiter.ServicePipelineDeployed)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#servicepipelinedeployedwaiter)
    """

    async def wait(self, *, name: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Waiter.ServicePipelineDeployed.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#servicepipelinedeployedwaiter)
        """


class ServiceTemplateVersionRegisteredWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Waiter.ServiceTemplateVersionRegistered)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#servicetemplateversionregisteredwaiter)
    """

    async def wait(
        self,
        *,
        majorVersion: str,
        minorVersion: str,
        templateName: str,
        WaiterConfig: "WaiterConfigTypeDef" = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Waiter.ServiceTemplateVersionRegistered.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#servicetemplateversionregisteredwaiter)
        """


class ServiceUpdatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Waiter.ServiceUpdated)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#serviceupdatedwaiter)
    """

    async def wait(self, *, name: str, WaiterConfig: "WaiterConfigTypeDef" = ...) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Waiter.ServiceUpdated.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#serviceupdatedwaiter)
        """
