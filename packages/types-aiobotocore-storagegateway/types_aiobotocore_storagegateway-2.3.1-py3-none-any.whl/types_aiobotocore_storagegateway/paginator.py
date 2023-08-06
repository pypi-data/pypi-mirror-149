"""
Type annotations for storagegateway service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_storagegateway/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_storagegateway.client import StorageGatewayClient
    from types_aiobotocore_storagegateway.paginator import (
        DescribeTapeArchivesPaginator,
        DescribeTapeRecoveryPointsPaginator,
        DescribeTapesPaginator,
        DescribeVTLDevicesPaginator,
        ListFileSharesPaginator,
        ListFileSystemAssociationsPaginator,
        ListGatewaysPaginator,
        ListTagsForResourcePaginator,
        ListTapePoolsPaginator,
        ListTapesPaginator,
        ListVolumesPaginator,
    )

    session = get_session()
    with session.create_client("storagegateway") as client:
        client: StorageGatewayClient

        describe_tape_archives_paginator: DescribeTapeArchivesPaginator = client.get_paginator("describe_tape_archives")
        describe_tape_recovery_points_paginator: DescribeTapeRecoveryPointsPaginator = client.get_paginator("describe_tape_recovery_points")
        describe_tapes_paginator: DescribeTapesPaginator = client.get_paginator("describe_tapes")
        describe_vtl_devices_paginator: DescribeVTLDevicesPaginator = client.get_paginator("describe_vtl_devices")
        list_file_shares_paginator: ListFileSharesPaginator = client.get_paginator("list_file_shares")
        list_file_system_associations_paginator: ListFileSystemAssociationsPaginator = client.get_paginator("list_file_system_associations")
        list_gateways_paginator: ListGatewaysPaginator = client.get_paginator("list_gateways")
        list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
        list_tape_pools_paginator: ListTapePoolsPaginator = client.get_paginator("list_tape_pools")
        list_tapes_paginator: ListTapesPaginator = client.get_paginator("list_tapes")
        list_volumes_paginator: ListVolumesPaginator = client.get_paginator("list_volumes")
    ```
"""
import sys
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeTapeArchivesOutputTypeDef,
    DescribeTapeRecoveryPointsOutputTypeDef,
    DescribeTapesOutputTypeDef,
    DescribeVTLDevicesOutputTypeDef,
    ListFileSharesOutputTypeDef,
    ListFileSystemAssociationsOutputTypeDef,
    ListGatewaysOutputTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListTapePoolsOutputTypeDef,
    ListTapesOutputTypeDef,
    ListVolumesOutputTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator


__all__ = (
    "DescribeTapeArchivesPaginator",
    "DescribeTapeRecoveryPointsPaginator",
    "DescribeTapesPaginator",
    "DescribeVTLDevicesPaginator",
    "ListFileSharesPaginator",
    "ListFileSystemAssociationsPaginator",
    "ListGatewaysPaginator",
    "ListTagsForResourcePaginator",
    "ListTapePoolsPaginator",
    "ListTapesPaginator",
    "ListVolumesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeTapeArchivesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.DescribeTapeArchives)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_storagegateway/paginators/#describetapearchivespaginator)
    """

    def paginate(
        self, *, TapeARNs: Sequence[str] = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeTapeArchivesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.DescribeTapeArchives.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_storagegateway/paginators/#describetapearchivespaginator)
        """


class DescribeTapeRecoveryPointsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.DescribeTapeRecoveryPoints)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_storagegateway/paginators/#describetaperecoverypointspaginator)
    """

    def paginate(
        self, *, GatewayARN: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeTapeRecoveryPointsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.DescribeTapeRecoveryPoints.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_storagegateway/paginators/#describetaperecoverypointspaginator)
        """


class DescribeTapesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.DescribeTapes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_storagegateway/paginators/#describetapespaginator)
    """

    def paginate(
        self,
        *,
        GatewayARN: str,
        TapeARNs: Sequence[str] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeTapesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.DescribeTapes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_storagegateway/paginators/#describetapespaginator)
        """


class DescribeVTLDevicesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.DescribeVTLDevices)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_storagegateway/paginators/#describevtldevicespaginator)
    """

    def paginate(
        self,
        *,
        GatewayARN: str,
        VTLDeviceARNs: Sequence[str] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeVTLDevicesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.DescribeVTLDevices.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_storagegateway/paginators/#describevtldevicespaginator)
        """


class ListFileSharesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.ListFileShares)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_storagegateway/paginators/#listfilesharespaginator)
    """

    def paginate(
        self, *, GatewayARN: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListFileSharesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.ListFileShares.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_storagegateway/paginators/#listfilesharespaginator)
        """


class ListFileSystemAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.ListFileSystemAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_storagegateway/paginators/#listfilesystemassociationspaginator)
    """

    def paginate(
        self, *, GatewayARN: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListFileSystemAssociationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.ListFileSystemAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_storagegateway/paginators/#listfilesystemassociationspaginator)
        """


class ListGatewaysPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.ListGateways)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_storagegateway/paginators/#listgatewayspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListGatewaysOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.ListGateways.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_storagegateway/paginators/#listgatewayspaginator)
        """


class ListTagsForResourcePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.ListTagsForResource)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_storagegateway/paginators/#listtagsforresourcepaginator)
    """

    def paginate(
        self, *, ResourceARN: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListTagsForResourceOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.ListTagsForResource.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_storagegateway/paginators/#listtagsforresourcepaginator)
        """


class ListTapePoolsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.ListTapePools)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_storagegateway/paginators/#listtapepoolspaginator)
    """

    def paginate(
        self, *, PoolARNs: Sequence[str] = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListTapePoolsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.ListTapePools.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_storagegateway/paginators/#listtapepoolspaginator)
        """


class ListTapesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.ListTapes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_storagegateway/paginators/#listtapespaginator)
    """

    def paginate(
        self, *, TapeARNs: Sequence[str] = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListTapesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.ListTapes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_storagegateway/paginators/#listtapespaginator)
        """


class ListVolumesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.ListVolumes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_storagegateway/paginators/#listvolumespaginator)
    """

    def paginate(
        self, *, GatewayARN: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListVolumesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/storagegateway.html#StorageGateway.Paginator.ListVolumes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_storagegateway/paginators/#listvolumespaginator)
        """
