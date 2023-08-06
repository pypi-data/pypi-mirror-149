"""
Type annotations for greengrassv2 service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_greengrassv2.client import GreengrassV2Client

    session = get_session()
    async with session.create_client("greengrassv2") as client:
        client: GreengrassV2Client
    ```
"""
import sys
from typing import IO, Any, Dict, Mapping, Sequence, Type, Union, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.response import StreamingBody

from .literals import (
    ComponentVisibilityScopeType,
    CoreDeviceStatusType,
    DeploymentHistoryFilterType,
    RecipeOutputFormatType,
)
from .paginator import (
    ListClientDevicesAssociatedWithCoreDevicePaginator,
    ListComponentsPaginator,
    ListComponentVersionsPaginator,
    ListCoreDevicesPaginator,
    ListDeploymentsPaginator,
    ListEffectiveDeploymentsPaginator,
    ListInstalledComponentsPaginator,
)
from .type_defs import (
    AssociateClientDeviceWithCoreDeviceEntryTypeDef,
    AssociateServiceRoleToAccountResponseTypeDef,
    BatchAssociateClientDeviceWithCoreDeviceResponseTypeDef,
    BatchDisassociateClientDeviceFromCoreDeviceResponseTypeDef,
    CancelDeploymentResponseTypeDef,
    ComponentCandidateTypeDef,
    ComponentDeploymentSpecificationTypeDef,
    ComponentPlatformTypeDef,
    ConnectivityInfoTypeDef,
    CreateComponentVersionResponseTypeDef,
    CreateDeploymentResponseTypeDef,
    DeploymentIoTJobConfigurationTypeDef,
    DeploymentPoliciesTypeDef,
    DescribeComponentResponseTypeDef,
    DisassociateClientDeviceFromCoreDeviceEntryTypeDef,
    DisassociateServiceRoleFromAccountResponseTypeDef,
    GetComponentResponseTypeDef,
    GetComponentVersionArtifactResponseTypeDef,
    GetConnectivityInfoResponseTypeDef,
    GetCoreDeviceResponseTypeDef,
    GetDeploymentResponseTypeDef,
    GetServiceRoleForAccountResponseTypeDef,
    LambdaFunctionRecipeSourceTypeDef,
    ListClientDevicesAssociatedWithCoreDeviceResponseTypeDef,
    ListComponentsResponseTypeDef,
    ListComponentVersionsResponseTypeDef,
    ListCoreDevicesResponseTypeDef,
    ListDeploymentsResponseTypeDef,
    ListEffectiveDeploymentsResponseTypeDef,
    ListInstalledComponentsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ResolveComponentCandidatesResponseTypeDef,
    UpdateConnectivityInfoResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("GreengrassV2Client",)


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
    RequestAlreadyInProgressException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class GreengrassV2Client(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        GreengrassV2Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#exceptions)
        """

    async def associate_service_role_to_account(
        self, *, roleArn: str
    ) -> AssociateServiceRoleToAccountResponseTypeDef:
        """
        Associates a Greengrass service role with IoT Greengrass for your Amazon Web
        Services account in this Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.associate_service_role_to_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#associate_service_role_to_account)
        """

    async def batch_associate_client_device_with_core_device(
        self,
        *,
        coreDeviceThingName: str,
        entries: Sequence["AssociateClientDeviceWithCoreDeviceEntryTypeDef"] = ...
    ) -> BatchAssociateClientDeviceWithCoreDeviceResponseTypeDef:
        """
        Associates a list of client devices with a core device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.batch_associate_client_device_with_core_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#batch_associate_client_device_with_core_device)
        """

    async def batch_disassociate_client_device_from_core_device(
        self,
        *,
        coreDeviceThingName: str,
        entries: Sequence["DisassociateClientDeviceFromCoreDeviceEntryTypeDef"] = ...
    ) -> BatchDisassociateClientDeviceFromCoreDeviceResponseTypeDef:
        """
        Disassociates a list of client devices from a core device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.batch_disassociate_client_device_from_core_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#batch_disassociate_client_device_from_core_device)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#can_paginate)
        """

    async def cancel_deployment(self, *, deploymentId: str) -> CancelDeploymentResponseTypeDef:
        """
        Cancels a deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.cancel_deployment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#cancel_deployment)
        """

    async def create_component_version(
        self,
        *,
        inlineRecipe: Union[str, bytes, IO[Any], StreamingBody] = ...,
        lambdaFunction: "LambdaFunctionRecipeSourceTypeDef" = ...,
        tags: Mapping[str, str] = ...,
        clientToken: str = ...
    ) -> CreateComponentVersionResponseTypeDef:
        """
        Creates a component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.create_component_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#create_component_version)
        """

    async def create_deployment(
        self,
        *,
        targetArn: str,
        deploymentName: str = ...,
        components: Mapping[str, "ComponentDeploymentSpecificationTypeDef"] = ...,
        iotJobConfiguration: "DeploymentIoTJobConfigurationTypeDef" = ...,
        deploymentPolicies: "DeploymentPoliciesTypeDef" = ...,
        tags: Mapping[str, str] = ...,
        clientToken: str = ...
    ) -> CreateDeploymentResponseTypeDef:
        """
        Creates a continuous deployment for a target, which is a Greengrass core device
        or group of core devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.create_deployment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#create_deployment)
        """

    async def delete_component(self, *, arn: str) -> None:
        """
        Deletes a version of a component from IoT Greengrass.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.delete_component)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#delete_component)
        """

    async def delete_core_device(self, *, coreDeviceThingName: str) -> None:
        """
        Deletes a Greengrass core device, which is an IoT thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.delete_core_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#delete_core_device)
        """

    async def describe_component(self, *, arn: str) -> DescribeComponentResponseTypeDef:
        """
        Retrieves metadata for a version of a component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.describe_component)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#describe_component)
        """

    async def disassociate_service_role_from_account(
        self,
    ) -> DisassociateServiceRoleFromAccountResponseTypeDef:
        """
        Disassociates the Greengrass service role from IoT Greengrass for your Amazon
        Web Services account in this Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.disassociate_service_role_from_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#disassociate_service_role_from_account)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#generate_presigned_url)
        """

    async def get_component(
        self, *, arn: str, recipeOutputFormat: RecipeOutputFormatType = ...
    ) -> GetComponentResponseTypeDef:
        """
        Gets the recipe for a version of a component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.get_component)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#get_component)
        """

    async def get_component_version_artifact(
        self, *, arn: str, artifactName: str
    ) -> GetComponentVersionArtifactResponseTypeDef:
        """
        Gets the pre-signed URL to download a public component artifact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.get_component_version_artifact)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#get_component_version_artifact)
        """

    async def get_connectivity_info(self, *, thingName: str) -> GetConnectivityInfoResponseTypeDef:
        """
        Retrieves connectivity information for a Greengrass core device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.get_connectivity_info)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#get_connectivity_info)
        """

    async def get_core_device(self, *, coreDeviceThingName: str) -> GetCoreDeviceResponseTypeDef:
        """
        Retrieves metadata for a Greengrass core device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.get_core_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#get_core_device)
        """

    async def get_deployment(self, *, deploymentId: str) -> GetDeploymentResponseTypeDef:
        """
        Gets a deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.get_deployment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#get_deployment)
        """

    async def get_service_role_for_account(self) -> GetServiceRoleForAccountResponseTypeDef:
        """
        Gets the service role associated with IoT Greengrass for your Amazon Web
        Services account in this Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.get_service_role_for_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#get_service_role_for_account)
        """

    async def list_client_devices_associated_with_core_device(
        self, *, coreDeviceThingName: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListClientDevicesAssociatedWithCoreDeviceResponseTypeDef:
        """
        Retrieves a paginated list of client devices that are associated with a core
        device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.list_client_devices_associated_with_core_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#list_client_devices_associated_with_core_device)
        """

    async def list_component_versions(
        self, *, arn: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListComponentVersionsResponseTypeDef:
        """
        Retrieves a paginated list of all versions for a component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.list_component_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#list_component_versions)
        """

    async def list_components(
        self,
        *,
        scope: ComponentVisibilityScopeType = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListComponentsResponseTypeDef:
        """
        Retrieves a paginated list of component summaries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.list_components)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#list_components)
        """

    async def list_core_devices(
        self,
        *,
        thingGroupArn: str = ...,
        status: CoreDeviceStatusType = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListCoreDevicesResponseTypeDef:
        """
        Retrieves a paginated list of Greengrass core devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.list_core_devices)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#list_core_devices)
        """

    async def list_deployments(
        self,
        *,
        targetArn: str = ...,
        historyFilter: DeploymentHistoryFilterType = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListDeploymentsResponseTypeDef:
        """
        Retrieves a paginated list of deployments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.list_deployments)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#list_deployments)
        """

    async def list_effective_deployments(
        self, *, coreDeviceThingName: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListEffectiveDeploymentsResponseTypeDef:
        """
        Retrieves a paginated list of deployment jobs that IoT Greengrass sends to
        Greengrass core devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.list_effective_deployments)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#list_effective_deployments)
        """

    async def list_installed_components(
        self, *, coreDeviceThingName: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListInstalledComponentsResponseTypeDef:
        """
        Retrieves a paginated list of the components that a Greengrass core device runs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.list_installed_components)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#list_installed_components)
        """

    async def list_tags_for_resource(
        self, *, resourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves the list of tags for an IoT Greengrass resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#list_tags_for_resource)
        """

    async def resolve_component_candidates(
        self,
        *,
        platform: "ComponentPlatformTypeDef",
        componentCandidates: Sequence["ComponentCandidateTypeDef"]
    ) -> ResolveComponentCandidatesResponseTypeDef:
        """
        Retrieves a list of components that meet the component, version, and platform
        requirements of a deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.resolve_component_candidates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#resolve_component_candidates)
        """

    async def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds tags to an IoT Greengrass resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#tag_resource)
        """

    async def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes a tag from an IoT Greengrass resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#untag_resource)
        """

    async def update_connectivity_info(
        self, *, thingName: str, connectivityInfo: Sequence["ConnectivityInfoTypeDef"]
    ) -> UpdateConnectivityInfoResponseTypeDef:
        """
        Updates connectivity information for a Greengrass core device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.update_connectivity_info)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#update_connectivity_info)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_client_devices_associated_with_core_device"]
    ) -> ListClientDevicesAssociatedWithCoreDevicePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_component_versions"]
    ) -> ListComponentVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_components"]) -> ListComponentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_core_devices"]
    ) -> ListCoreDevicesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_deployments"]
    ) -> ListDeploymentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_effective_deployments"]
    ) -> ListEffectiveDeploymentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_installed_components"]
    ) -> ListInstalledComponentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#get_paginator)
        """

    async def __aenter__(self) -> "GreengrassV2Client":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/)
        """
