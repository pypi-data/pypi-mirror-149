"""
Type annotations for greengrassv2 service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_greengrassv2.client import GreengrassV2Client
    from types_aiobotocore_greengrassv2.paginator import (
        ListClientDevicesAssociatedWithCoreDevicePaginator,
        ListComponentVersionsPaginator,
        ListComponentsPaginator,
        ListCoreDevicesPaginator,
        ListDeploymentsPaginator,
        ListEffectiveDeploymentsPaginator,
        ListInstalledComponentsPaginator,
    )

    session = get_session()
    with session.create_client("greengrassv2") as client:
        client: GreengrassV2Client

        list_client_devices_associated_with_core_device_paginator: ListClientDevicesAssociatedWithCoreDevicePaginator = client.get_paginator("list_client_devices_associated_with_core_device")
        list_component_versions_paginator: ListComponentVersionsPaginator = client.get_paginator("list_component_versions")
        list_components_paginator: ListComponentsPaginator = client.get_paginator("list_components")
        list_core_devices_paginator: ListCoreDevicesPaginator = client.get_paginator("list_core_devices")
        list_deployments_paginator: ListDeploymentsPaginator = client.get_paginator("list_deployments")
        list_effective_deployments_paginator: ListEffectiveDeploymentsPaginator = client.get_paginator("list_effective_deployments")
        list_installed_components_paginator: ListInstalledComponentsPaginator = client.get_paginator("list_installed_components")
    ```
"""
import sys
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import (
    ComponentVisibilityScopeType,
    CoreDeviceStatusType,
    DeploymentHistoryFilterType,
)
from .type_defs import (
    ListClientDevicesAssociatedWithCoreDeviceResponseTypeDef,
    ListComponentsResponseTypeDef,
    ListComponentVersionsResponseTypeDef,
    ListCoreDevicesResponseTypeDef,
    ListDeploymentsResponseTypeDef,
    ListEffectiveDeploymentsResponseTypeDef,
    ListInstalledComponentsResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator

__all__ = (
    "ListClientDevicesAssociatedWithCoreDevicePaginator",
    "ListComponentVersionsPaginator",
    "ListComponentsPaginator",
    "ListCoreDevicesPaginator",
    "ListDeploymentsPaginator",
    "ListEffectiveDeploymentsPaginator",
    "ListInstalledComponentsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListClientDevicesAssociatedWithCoreDevicePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListClientDevicesAssociatedWithCoreDevice)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/paginators/#listclientdevicesassociatedwithcoredevicepaginator)
    """

    def paginate(
        self, *, coreDeviceThingName: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListClientDevicesAssociatedWithCoreDeviceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListClientDevicesAssociatedWithCoreDevice.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/paginators/#listclientdevicesassociatedwithcoredevicepaginator)
        """

class ListComponentVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListComponentVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/paginators/#listcomponentversionspaginator)
    """

    def paginate(
        self, *, arn: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListComponentVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListComponentVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/paginators/#listcomponentversionspaginator)
        """

class ListComponentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListComponents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/paginators/#listcomponentspaginator)
    """

    def paginate(
        self,
        *,
        scope: ComponentVisibilityScopeType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListComponentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListComponents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/paginators/#listcomponentspaginator)
        """

class ListCoreDevicesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListCoreDevices)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/paginators/#listcoredevicespaginator)
    """

    def paginate(
        self,
        *,
        thingGroupArn: str = ...,
        status: CoreDeviceStatusType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListCoreDevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListCoreDevices.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/paginators/#listcoredevicespaginator)
        """

class ListDeploymentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListDeployments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/paginators/#listdeploymentspaginator)
    """

    def paginate(
        self,
        *,
        targetArn: str = ...,
        historyFilter: DeploymentHistoryFilterType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListDeploymentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListDeployments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/paginators/#listdeploymentspaginator)
        """

class ListEffectiveDeploymentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListEffectiveDeployments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/paginators/#listeffectivedeploymentspaginator)
    """

    def paginate(
        self, *, coreDeviceThingName: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListEffectiveDeploymentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListEffectiveDeployments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/paginators/#listeffectivedeploymentspaginator)
        """

class ListInstalledComponentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListInstalledComponents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/paginators/#listinstalledcomponentspaginator)
    """

    def paginate(
        self, *, coreDeviceThingName: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListInstalledComponentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Paginator.ListInstalledComponents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/paginators/#listinstalledcomponentspaginator)
        """
