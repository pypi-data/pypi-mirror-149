"""
Type annotations for s3 service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_s3.client import S3Client
    from types_aiobotocore_s3.paginator import (
        ListMultipartUploadsPaginator,
        ListObjectVersionsPaginator,
        ListObjectsPaginator,
        ListObjectsV2Paginator,
        ListPartsPaginator,
    )

    session = get_session()
    with session.create_client("s3") as client:
        client: S3Client

        list_multipart_uploads_paginator: ListMultipartUploadsPaginator = client.get_paginator("list_multipart_uploads")
        list_object_versions_paginator: ListObjectVersionsPaginator = client.get_paginator("list_object_versions")
        list_objects_paginator: ListObjectsPaginator = client.get_paginator("list_objects")
        list_objects_v2_paginator: ListObjectsV2Paginator = client.get_paginator("list_objects_v2")
        list_parts_paginator: ListPartsPaginator = client.get_paginator("list_parts")
    ```
"""
import sys
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListMultipartUploadsOutputTypeDef,
    ListObjectsOutputTypeDef,
    ListObjectsV2OutputTypeDef,
    ListObjectVersionsOutputTypeDef,
    ListPartsOutputTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator
if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "ListMultipartUploadsPaginator",
    "ListObjectVersionsPaginator",
    "ListObjectsPaginator",
    "ListObjectsV2Paginator",
    "ListPartsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListMultipartUploadsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Paginator.ListMultipartUploads)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/paginators/#listmultipartuploadspaginator)
    """

    def paginate(
        self,
        *,
        Bucket: str,
        Delimiter: str = ...,
        EncodingType: Literal["url"] = ...,
        Prefix: str = ...,
        ExpectedBucketOwner: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListMultipartUploadsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Paginator.ListMultipartUploads.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/paginators/#listmultipartuploadspaginator)
        """


class ListObjectVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Paginator.ListObjectVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/paginators/#listobjectversionspaginator)
    """

    def paginate(
        self,
        *,
        Bucket: str,
        Delimiter: str = ...,
        EncodingType: Literal["url"] = ...,
        Prefix: str = ...,
        ExpectedBucketOwner: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListObjectVersionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Paginator.ListObjectVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/paginators/#listobjectversionspaginator)
        """


class ListObjectsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Paginator.ListObjects)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/paginators/#listobjectspaginator)
    """

    def paginate(
        self,
        *,
        Bucket: str,
        Delimiter: str = ...,
        EncodingType: Literal["url"] = ...,
        Prefix: str = ...,
        RequestPayer: Literal["requester"] = ...,
        ExpectedBucketOwner: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListObjectsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Paginator.ListObjects.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/paginators/#listobjectspaginator)
        """


class ListObjectsV2Paginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Paginator.ListObjectsV2)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/paginators/#listobjectsv2paginator)
    """

    def paginate(
        self,
        *,
        Bucket: str,
        Delimiter: str = ...,
        EncodingType: Literal["url"] = ...,
        Prefix: str = ...,
        FetchOwner: bool = ...,
        StartAfter: str = ...,
        RequestPayer: Literal["requester"] = ...,
        ExpectedBucketOwner: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListObjectsV2OutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Paginator.ListObjectsV2.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/paginators/#listobjectsv2paginator)
        """


class ListPartsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Paginator.ListParts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/paginators/#listpartspaginator)
    """

    def paginate(
        self,
        *,
        Bucket: str,
        Key: str,
        UploadId: str,
        RequestPayer: Literal["requester"] = ...,
        ExpectedBucketOwner: str = ...,
        SSECustomerAlgorithm: str = ...,
        SSECustomerKey: str = ...,
        SSECustomerKeyMD5: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListPartsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Paginator.ListParts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/paginators/#listpartspaginator)
        """
