"""
Type annotations for rekognition service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_rekognition.client import RekognitionClient
    from types_aiobotocore_rekognition.paginator import (
        DescribeProjectVersionsPaginator,
        DescribeProjectsPaginator,
        ListCollectionsPaginator,
        ListDatasetEntriesPaginator,
        ListDatasetLabelsPaginator,
        ListFacesPaginator,
        ListStreamProcessorsPaginator,
    )

    session = get_session()
    with session.create_client("rekognition") as client:
        client: RekognitionClient

        describe_project_versions_paginator: DescribeProjectVersionsPaginator = client.get_paginator("describe_project_versions")
        describe_projects_paginator: DescribeProjectsPaginator = client.get_paginator("describe_projects")
        list_collections_paginator: ListCollectionsPaginator = client.get_paginator("list_collections")
        list_dataset_entries_paginator: ListDatasetEntriesPaginator = client.get_paginator("list_dataset_entries")
        list_dataset_labels_paginator: ListDatasetLabelsPaginator = client.get_paginator("list_dataset_labels")
        list_faces_paginator: ListFacesPaginator = client.get_paginator("list_faces")
        list_stream_processors_paginator: ListStreamProcessorsPaginator = client.get_paginator("list_stream_processors")
    ```
"""
import sys
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeProjectsResponseTypeDef,
    DescribeProjectVersionsResponseTypeDef,
    ListCollectionsResponseTypeDef,
    ListDatasetEntriesResponseTypeDef,
    ListDatasetLabelsResponseTypeDef,
    ListFacesResponseTypeDef,
    ListStreamProcessorsResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator


__all__ = (
    "DescribeProjectVersionsPaginator",
    "DescribeProjectsPaginator",
    "ListCollectionsPaginator",
    "ListDatasetEntriesPaginator",
    "ListDatasetLabelsPaginator",
    "ListFacesPaginator",
    "ListStreamProcessorsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeProjectVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html#Rekognition.Paginator.DescribeProjectVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#describeprojectversionspaginator)
    """

    def paginate(
        self,
        *,
        ProjectArn: str,
        VersionNames: Sequence[str] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeProjectVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html#Rekognition.Paginator.DescribeProjectVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#describeprojectversionspaginator)
        """


class DescribeProjectsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html#Rekognition.Paginator.DescribeProjects)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#describeprojectspaginator)
    """

    def paginate(
        self, *, ProjectNames: Sequence[str] = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DescribeProjectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html#Rekognition.Paginator.DescribeProjects.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#describeprojectspaginator)
        """


class ListCollectionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html#Rekognition.Paginator.ListCollections)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#listcollectionspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListCollectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html#Rekognition.Paginator.ListCollections.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#listcollectionspaginator)
        """


class ListDatasetEntriesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html#Rekognition.Paginator.ListDatasetEntries)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#listdatasetentriespaginator)
    """

    def paginate(
        self,
        *,
        DatasetArn: str,
        ContainsLabels: Sequence[str] = ...,
        Labeled: bool = ...,
        SourceRefContains: str = ...,
        HasErrors: bool = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListDatasetEntriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html#Rekognition.Paginator.ListDatasetEntries.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#listdatasetentriespaginator)
        """


class ListDatasetLabelsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html#Rekognition.Paginator.ListDatasetLabels)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#listdatasetlabelspaginator)
    """

    def paginate(
        self, *, DatasetArn: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListDatasetLabelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html#Rekognition.Paginator.ListDatasetLabels.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#listdatasetlabelspaginator)
        """


class ListFacesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html#Rekognition.Paginator.ListFaces)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#listfacespaginator)
    """

    def paginate(
        self, *, CollectionId: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListFacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html#Rekognition.Paginator.ListFaces.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#listfacespaginator)
        """


class ListStreamProcessorsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html#Rekognition.Paginator.ListStreamProcessors)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#liststreamprocessorspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListStreamProcessorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html#Rekognition.Paginator.ListStreamProcessors.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#liststreamprocessorspaginator)
        """
