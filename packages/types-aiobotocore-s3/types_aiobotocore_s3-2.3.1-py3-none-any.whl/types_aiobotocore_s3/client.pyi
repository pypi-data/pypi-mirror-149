"""
Type annotations for s3 service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_s3.client import S3Client

    session = get_session()
    async with session.create_client("s3") as client:
        client: S3Client
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Callable, Dict, List, Mapping, Sequence, Type, Union, overload

from aiobotocore.client import AioBaseClient
from boto3.s3.transfer import TransferConfig
from botocore.client import BaseClient, ClientMeta
from botocore.response import StreamingBody

from .literals import (
    BucketCannedACLType,
    ChecksumAlgorithmType,
    MetadataDirectiveType,
    ObjectAttributesType,
    ObjectCannedACLType,
    ObjectLockLegalHoldStatusType,
    ObjectLockModeType,
    ObjectOwnershipType,
    ReplicationStatusType,
    ServerSideEncryptionType,
    StorageClassType,
    TaggingDirectiveType,
)
from .paginator import (
    ListMultipartUploadsPaginator,
    ListObjectsPaginator,
    ListObjectsV2Paginator,
    ListObjectVersionsPaginator,
    ListPartsPaginator,
)
from .type_defs import (
    AbortMultipartUploadOutputTypeDef,
    AccelerateConfigurationTypeDef,
    AccessControlPolicyTypeDef,
    AnalyticsConfigurationTypeDef,
    BucketLifecycleConfigurationTypeDef,
    BucketLoggingStatusTypeDef,
    CompletedMultipartUploadTypeDef,
    CompleteMultipartUploadOutputTypeDef,
    CopyObjectOutputTypeDef,
    CopySourceTypeDef,
    CORSConfigurationTypeDef,
    CreateBucketConfigurationTypeDef,
    CreateBucketOutputTypeDef,
    CreateMultipartUploadOutputTypeDef,
    DeleteObjectOutputTypeDef,
    DeleteObjectsOutputTypeDef,
    DeleteObjectTaggingOutputTypeDef,
    DeleteTypeDef,
    GetBucketAccelerateConfigurationOutputTypeDef,
    GetBucketAclOutputTypeDef,
    GetBucketAnalyticsConfigurationOutputTypeDef,
    GetBucketCorsOutputTypeDef,
    GetBucketEncryptionOutputTypeDef,
    GetBucketIntelligentTieringConfigurationOutputTypeDef,
    GetBucketInventoryConfigurationOutputTypeDef,
    GetBucketLifecycleConfigurationOutputTypeDef,
    GetBucketLifecycleOutputTypeDef,
    GetBucketLocationOutputTypeDef,
    GetBucketLoggingOutputTypeDef,
    GetBucketMetricsConfigurationOutputTypeDef,
    GetBucketOwnershipControlsOutputTypeDef,
    GetBucketPolicyOutputTypeDef,
    GetBucketPolicyStatusOutputTypeDef,
    GetBucketReplicationOutputTypeDef,
    GetBucketRequestPaymentOutputTypeDef,
    GetBucketTaggingOutputTypeDef,
    GetBucketVersioningOutputTypeDef,
    GetBucketWebsiteOutputTypeDef,
    GetObjectAclOutputTypeDef,
    GetObjectAttributesOutputTypeDef,
    GetObjectLegalHoldOutputTypeDef,
    GetObjectLockConfigurationOutputTypeDef,
    GetObjectOutputTypeDef,
    GetObjectRetentionOutputTypeDef,
    GetObjectTaggingOutputTypeDef,
    GetObjectTorrentOutputTypeDef,
    GetPublicAccessBlockOutputTypeDef,
    HeadObjectOutputTypeDef,
    InputSerializationTypeDef,
    IntelligentTieringConfigurationTypeDef,
    InventoryConfigurationTypeDef,
    LifecycleConfigurationTypeDef,
    ListBucketAnalyticsConfigurationsOutputTypeDef,
    ListBucketIntelligentTieringConfigurationsOutputTypeDef,
    ListBucketInventoryConfigurationsOutputTypeDef,
    ListBucketMetricsConfigurationsOutputTypeDef,
    ListBucketsOutputTypeDef,
    ListMultipartUploadsOutputTypeDef,
    ListObjectsOutputTypeDef,
    ListObjectsV2OutputTypeDef,
    ListObjectVersionsOutputTypeDef,
    ListPartsOutputTypeDef,
    MetricsConfigurationTypeDef,
    NotificationConfigurationDeprecatedResponseMetadataTypeDef,
    NotificationConfigurationDeprecatedTypeDef,
    NotificationConfigurationResponseMetadataTypeDef,
    NotificationConfigurationTypeDef,
    ObjectLockConfigurationTypeDef,
    ObjectLockLegalHoldTypeDef,
    ObjectLockRetentionTypeDef,
    OutputSerializationTypeDef,
    OwnershipControlsTypeDef,
    PublicAccessBlockConfigurationTypeDef,
    PutObjectAclOutputTypeDef,
    PutObjectLegalHoldOutputTypeDef,
    PutObjectLockConfigurationOutputTypeDef,
    PutObjectOutputTypeDef,
    PutObjectRetentionOutputTypeDef,
    PutObjectTaggingOutputTypeDef,
    ReplicationConfigurationTypeDef,
    RequestPaymentConfigurationTypeDef,
    RequestProgressTypeDef,
    RestoreObjectOutputTypeDef,
    RestoreRequestTypeDef,
    ScanRangeTypeDef,
    SelectObjectContentOutputTypeDef,
    ServerSideEncryptionConfigurationTypeDef,
    TaggingTypeDef,
    UploadPartCopyOutputTypeDef,
    UploadPartOutputTypeDef,
    VersioningConfigurationTypeDef,
    WebsiteConfigurationTypeDef,
)
from .waiter import (
    BucketExistsWaiter,
    BucketNotExistsWaiter,
    ObjectExistsWaiter,
    ObjectNotExistsWaiter,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("S3Client",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    BucketAlreadyExists: Type[BotocoreClientError]
    BucketAlreadyOwnedByYou: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InvalidObjectState: Type[BotocoreClientError]
    NoSuchBucket: Type[BotocoreClientError]
    NoSuchKey: Type[BotocoreClientError]
    NoSuchUpload: Type[BotocoreClientError]
    ObjectAlreadyInActiveTierError: Type[BotocoreClientError]
    ObjectNotInActiveTierError: Type[BotocoreClientError]

class S3Client(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        S3Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#exceptions)
        """
    async def abort_multipart_upload(
        self,
        *,
        Bucket: str,
        Key: str,
        UploadId: str,
        RequestPayer: Literal["requester"] = ...,
        ExpectedBucketOwner: str = ...
    ) -> AbortMultipartUploadOutputTypeDef:
        """
        This action aborts a multipart upload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.abort_multipart_upload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#abort_multipart_upload)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#can_paginate)
        """
    async def complete_multipart_upload(
        self,
        *,
        Bucket: str,
        Key: str,
        UploadId: str,
        MultipartUpload: "CompletedMultipartUploadTypeDef" = ...,
        ChecksumCRC32: str = ...,
        ChecksumCRC32C: str = ...,
        ChecksumSHA1: str = ...,
        ChecksumSHA256: str = ...,
        RequestPayer: Literal["requester"] = ...,
        ExpectedBucketOwner: str = ...,
        SSECustomerAlgorithm: str = ...,
        SSECustomerKey: str = ...,
        SSECustomerKeyMD5: str = ...
    ) -> CompleteMultipartUploadOutputTypeDef:
        """
        Completes a multipart upload by assembling previously uploaded parts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.complete_multipart_upload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#complete_multipart_upload)
        """
    async def copy(
        self,
        CopySource: "CopySourceTypeDef",
        Bucket: str,
        Key: str,
        ExtraArgs: Dict[str, Any] = ...,
        Callback: Callable[..., Any] = ...,
        SourceClient: BaseClient = ...,
        Config: TransferConfig = ...,
    ) -> None:
        """
        Copy an object from one S3 location to another.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.copy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#copy)
        """
    async def copy_object(
        self,
        *,
        Bucket: str,
        CopySource: Union[str, "CopySourceTypeDef"],
        Key: str,
        ACL: ObjectCannedACLType = ...,
        CacheControl: str = ...,
        ChecksumAlgorithm: ChecksumAlgorithmType = ...,
        ContentDisposition: str = ...,
        ContentEncoding: str = ...,
        ContentLanguage: str = ...,
        ContentType: str = ...,
        CopySourceIfMatch: str = ...,
        CopySourceIfModifiedSince: Union[datetime, str] = ...,
        CopySourceIfNoneMatch: str = ...,
        CopySourceIfUnmodifiedSince: Union[datetime, str] = ...,
        Expires: Union[datetime, str] = ...,
        GrantFullControl: str = ...,
        GrantRead: str = ...,
        GrantReadACP: str = ...,
        GrantWriteACP: str = ...,
        Metadata: Mapping[str, str] = ...,
        MetadataDirective: MetadataDirectiveType = ...,
        TaggingDirective: TaggingDirectiveType = ...,
        ServerSideEncryption: ServerSideEncryptionType = ...,
        StorageClass: StorageClassType = ...,
        WebsiteRedirectLocation: str = ...,
        SSECustomerAlgorithm: str = ...,
        SSECustomerKey: str = ...,
        SSECustomerKeyMD5: str = ...,
        SSEKMSKeyId: str = ...,
        SSEKMSEncryptionContext: str = ...,
        BucketKeyEnabled: bool = ...,
        CopySourceSSECustomerAlgorithm: str = ...,
        CopySourceSSECustomerKey: str = ...,
        CopySourceSSECustomerKeyMD5: str = ...,
        RequestPayer: Literal["requester"] = ...,
        Tagging: str = ...,
        ObjectLockMode: ObjectLockModeType = ...,
        ObjectLockRetainUntilDate: Union[datetime, str] = ...,
        ObjectLockLegalHoldStatus: ObjectLockLegalHoldStatusType = ...,
        ExpectedBucketOwner: str = ...,
        ExpectedSourceBucketOwner: str = ...
    ) -> CopyObjectOutputTypeDef:
        """
        Creates a copy of an object that is already stored in Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.copy_object)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#copy_object)
        """
    async def create_bucket(
        self,
        *,
        Bucket: str,
        ACL: BucketCannedACLType = ...,
        CreateBucketConfiguration: "CreateBucketConfigurationTypeDef" = ...,
        GrantFullControl: str = ...,
        GrantRead: str = ...,
        GrantReadACP: str = ...,
        GrantWrite: str = ...,
        GrantWriteACP: str = ...,
        ObjectLockEnabledForBucket: bool = ...,
        ObjectOwnership: ObjectOwnershipType = ...
    ) -> CreateBucketOutputTypeDef:
        """
        Creates a new S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.create_bucket)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#create_bucket)
        """
    async def create_multipart_upload(
        self,
        *,
        Bucket: str,
        Key: str,
        ACL: ObjectCannedACLType = ...,
        CacheControl: str = ...,
        ContentDisposition: str = ...,
        ContentEncoding: str = ...,
        ContentLanguage: str = ...,
        ContentType: str = ...,
        Expires: Union[datetime, str] = ...,
        GrantFullControl: str = ...,
        GrantRead: str = ...,
        GrantReadACP: str = ...,
        GrantWriteACP: str = ...,
        Metadata: Mapping[str, str] = ...,
        ServerSideEncryption: ServerSideEncryptionType = ...,
        StorageClass: StorageClassType = ...,
        WebsiteRedirectLocation: str = ...,
        SSECustomerAlgorithm: str = ...,
        SSECustomerKey: str = ...,
        SSECustomerKeyMD5: str = ...,
        SSEKMSKeyId: str = ...,
        SSEKMSEncryptionContext: str = ...,
        BucketKeyEnabled: bool = ...,
        RequestPayer: Literal["requester"] = ...,
        Tagging: str = ...,
        ObjectLockMode: ObjectLockModeType = ...,
        ObjectLockRetainUntilDate: Union[datetime, str] = ...,
        ObjectLockLegalHoldStatus: ObjectLockLegalHoldStatusType = ...,
        ExpectedBucketOwner: str = ...,
        ChecksumAlgorithm: ChecksumAlgorithmType = ...
    ) -> CreateMultipartUploadOutputTypeDef:
        """
        This action initiates a multipart upload and returns an upload ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.create_multipart_upload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#create_multipart_upload)
        """
    async def delete_bucket(self, *, Bucket: str, ExpectedBucketOwner: str = ...) -> None:
        """
        Deletes the S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_bucket)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_bucket)
        """
    async def delete_bucket_analytics_configuration(
        self, *, Bucket: str, Id: str, ExpectedBucketOwner: str = ...
    ) -> None:
        """
        Deletes an analytics configuration for the bucket (specified by the analytics
        configuration ID).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_bucket_analytics_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_bucket_analytics_configuration)
        """
    async def delete_bucket_cors(self, *, Bucket: str, ExpectedBucketOwner: str = ...) -> None:
        """
        Deletes the `cors` configuration information set for the bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_bucket_cors)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_bucket_cors)
        """
    async def delete_bucket_encryption(
        self, *, Bucket: str, ExpectedBucketOwner: str = ...
    ) -> None:
        """
        This implementation of the DELETE action removes default encryption from the
        bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_bucket_encryption)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_bucket_encryption)
        """
    async def delete_bucket_intelligent_tiering_configuration(
        self, *, Bucket: str, Id: str
    ) -> None:
        """
        Deletes the S3 Intelligent-Tiering configuration from the specified bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_bucket_intelligent_tiering_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_bucket_intelligent_tiering_configuration)
        """
    async def delete_bucket_inventory_configuration(
        self, *, Bucket: str, Id: str, ExpectedBucketOwner: str = ...
    ) -> None:
        """
        Deletes an inventory configuration (identified by the inventory ID) from the
        bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_bucket_inventory_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_bucket_inventory_configuration)
        """
    async def delete_bucket_lifecycle(self, *, Bucket: str, ExpectedBucketOwner: str = ...) -> None:
        """
        Deletes the lifecycle configuration from the specified bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_bucket_lifecycle)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_bucket_lifecycle)
        """
    async def delete_bucket_metrics_configuration(
        self, *, Bucket: str, Id: str, ExpectedBucketOwner: str = ...
    ) -> None:
        """
        Deletes a metrics configuration for the Amazon CloudWatch request metrics
        (specified by the metrics configuration ID) from the bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_bucket_metrics_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_bucket_metrics_configuration)
        """
    async def delete_bucket_ownership_controls(
        self, *, Bucket: str, ExpectedBucketOwner: str = ...
    ) -> None:
        """
        Removes `OwnershipControls` for an Amazon S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_bucket_ownership_controls)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_bucket_ownership_controls)
        """
    async def delete_bucket_policy(self, *, Bucket: str, ExpectedBucketOwner: str = ...) -> None:
        """
        This implementation of the DELETE action uses the policy subresource to delete
        the policy of a specified bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_bucket_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_bucket_policy)
        """
    async def delete_bucket_replication(
        self, *, Bucket: str, ExpectedBucketOwner: str = ...
    ) -> None:
        """
        Deletes the replication configuration from the bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_bucket_replication)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_bucket_replication)
        """
    async def delete_bucket_tagging(self, *, Bucket: str, ExpectedBucketOwner: str = ...) -> None:
        """
        Deletes the tags from the bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_bucket_tagging)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_bucket_tagging)
        """
    async def delete_bucket_website(self, *, Bucket: str, ExpectedBucketOwner: str = ...) -> None:
        """
        This action removes the website configuration for a bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_bucket_website)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_bucket_website)
        """
    async def delete_object(
        self,
        *,
        Bucket: str,
        Key: str,
        MFA: str = ...,
        VersionId: str = ...,
        RequestPayer: Literal["requester"] = ...,
        BypassGovernanceRetention: bool = ...,
        ExpectedBucketOwner: str = ...
    ) -> DeleteObjectOutputTypeDef:
        """
        Removes the null version (if there is one) of an object and inserts a delete
        marker, which becomes the latest version of the object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_object)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_object)
        """
    async def delete_object_tagging(
        self, *, Bucket: str, Key: str, VersionId: str = ..., ExpectedBucketOwner: str = ...
    ) -> DeleteObjectTaggingOutputTypeDef:
        """
        Removes the entire tag set from the specified object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_object_tagging)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_object_tagging)
        """
    async def delete_objects(
        self,
        *,
        Bucket: str,
        Delete: "DeleteTypeDef",
        MFA: str = ...,
        RequestPayer: Literal["requester"] = ...,
        BypassGovernanceRetention: bool = ...,
        ExpectedBucketOwner: str = ...,
        ChecksumAlgorithm: ChecksumAlgorithmType = ...
    ) -> DeleteObjectsOutputTypeDef:
        """
        This action enables you to delete multiple objects from a bucket using a single
        HTTP request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_objects)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_objects)
        """
    async def delete_public_access_block(
        self, *, Bucket: str, ExpectedBucketOwner: str = ...
    ) -> None:
        """
        Removes the `PublicAccessBlock` configuration for an Amazon S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_public_access_block)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#delete_public_access_block)
        """
    async def download_file(
        self,
        Bucket: str,
        Key: str,
        Filename: str,
        ExtraArgs: Dict[str, Any] = ...,
        Callback: Callable[..., Any] = ...,
        Config: TransferConfig = ...,
    ) -> None:
        """
        Download an S3 object to a file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.download_file)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#download_file)
        """
    async def download_fileobj(
        self,
        Bucket: str,
        Key: str,
        Fileobj: Union[IO[Any], StreamingBody],
        ExtraArgs: Dict[str, Any] = ...,
        Callback: Callable[..., Any] = ...,
        Config: TransferConfig = ...,
    ) -> None:
        """
        Download an object from S3 to a file-like object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.download_fileobj)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#download_fileobj)
        """
    async def generate_presigned_post(
        self,
        Bucket: str,
        Key: str,
        Fields: Dict[str, Any] = ...,
        Conditions: List[Any] = ...,
        ExpiresIn: int = 3600,
    ) -> Dict[str, Any]:
        """
        Builds the url and the form fields used for a presigned s3 post.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.generate_presigned_post)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#generate_presigned_post)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#generate_presigned_url)
        """
    async def get_bucket_accelerate_configuration(
        self, *, Bucket: str, ExpectedBucketOwner: str = ...
    ) -> GetBucketAccelerateConfigurationOutputTypeDef:
        """
        This implementation of the GET action uses the `accelerate` subresource to
        return the Transfer Acceleration state of a bucket, which is either `Enabled` or
        `Suspended`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_accelerate_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_accelerate_configuration)
        """
    async def get_bucket_acl(
        self, *, Bucket: str, ExpectedBucketOwner: str = ...
    ) -> GetBucketAclOutputTypeDef:
        """
        This implementation of the `GET` action uses the `acl` subresource to return the
        access control list (ACL) of a bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_acl)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_acl)
        """
    async def get_bucket_analytics_configuration(
        self, *, Bucket: str, Id: str, ExpectedBucketOwner: str = ...
    ) -> GetBucketAnalyticsConfigurationOutputTypeDef:
        """
        This implementation of the GET action returns an analytics configuration
        (identified by the analytics configuration ID) from the bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_analytics_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_analytics_configuration)
        """
    async def get_bucket_cors(
        self, *, Bucket: str, ExpectedBucketOwner: str = ...
    ) -> GetBucketCorsOutputTypeDef:
        """
        Returns the Cross-Origin Resource Sharing (CORS) configuration information set
        for the bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_cors)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_cors)
        """
    async def get_bucket_encryption(
        self, *, Bucket: str, ExpectedBucketOwner: str = ...
    ) -> GetBucketEncryptionOutputTypeDef:
        """
        Returns the default encryption configuration for an Amazon S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_encryption)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_encryption)
        """
    async def get_bucket_intelligent_tiering_configuration(
        self, *, Bucket: str, Id: str
    ) -> GetBucketIntelligentTieringConfigurationOutputTypeDef:
        """
        Gets the S3 Intelligent-Tiering configuration from the specified bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_intelligent_tiering_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_intelligent_tiering_configuration)
        """
    async def get_bucket_inventory_configuration(
        self, *, Bucket: str, Id: str, ExpectedBucketOwner: str = ...
    ) -> GetBucketInventoryConfigurationOutputTypeDef:
        """
        Returns an inventory configuration (identified by the inventory configuration
        ID) from the bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_inventory_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_inventory_configuration)
        """
    async def get_bucket_lifecycle(
        self, *, Bucket: str, ExpectedBucketOwner: str = ...
    ) -> GetBucketLifecycleOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_lifecycle)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_lifecycle)
        """
    async def get_bucket_lifecycle_configuration(
        self, *, Bucket: str, ExpectedBucketOwner: str = ...
    ) -> GetBucketLifecycleConfigurationOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_lifecycle_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_lifecycle_configuration)
        """
    async def get_bucket_location(
        self, *, Bucket: str, ExpectedBucketOwner: str = ...
    ) -> GetBucketLocationOutputTypeDef:
        """
        Returns the Region the bucket resides in.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_location)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_location)
        """
    async def get_bucket_logging(
        self, *, Bucket: str, ExpectedBucketOwner: str = ...
    ) -> GetBucketLoggingOutputTypeDef:
        """
        Returns the logging status of a bucket and the permissions users have to view
        and modify that status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_logging)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_logging)
        """
    async def get_bucket_metrics_configuration(
        self, *, Bucket: str, Id: str, ExpectedBucketOwner: str = ...
    ) -> GetBucketMetricsConfigurationOutputTypeDef:
        """
        Gets a metrics configuration (specified by the metrics configuration ID) from
        the bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_metrics_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_metrics_configuration)
        """
    async def get_bucket_notification(
        self, *, Bucket: str, ExpectedBucketOwner: str = ...
    ) -> NotificationConfigurationDeprecatedResponseMetadataTypeDef:
        """
        No longer used, see
        [GetBucketNotificationConfiguration](https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetBucketNotificationConfiguration.html)_
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_notification)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_notification)
        """
    async def get_bucket_notification_configuration(
        self, *, Bucket: str, ExpectedBucketOwner: str = ...
    ) -> NotificationConfigurationResponseMetadataTypeDef:
        """
        Returns the notification configuration of a bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_notification_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_notification_configuration)
        """
    async def get_bucket_ownership_controls(
        self, *, Bucket: str, ExpectedBucketOwner: str = ...
    ) -> GetBucketOwnershipControlsOutputTypeDef:
        """
        Retrieves `OwnershipControls` for an Amazon S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_ownership_controls)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_ownership_controls)
        """
    async def get_bucket_policy(
        self, *, Bucket: str, ExpectedBucketOwner: str = ...
    ) -> GetBucketPolicyOutputTypeDef:
        """
        Returns the policy of a specified bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_policy)
        """
    async def get_bucket_policy_status(
        self, *, Bucket: str, ExpectedBucketOwner: str = ...
    ) -> GetBucketPolicyStatusOutputTypeDef:
        """
        Retrieves the policy status for an Amazon S3 bucket, indicating whether the
        bucket is public.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_policy_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_policy_status)
        """
    async def get_bucket_replication(
        self, *, Bucket: str, ExpectedBucketOwner: str = ...
    ) -> GetBucketReplicationOutputTypeDef:
        """
        Returns the replication configuration of a bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_replication)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_replication)
        """
    async def get_bucket_request_payment(
        self, *, Bucket: str, ExpectedBucketOwner: str = ...
    ) -> GetBucketRequestPaymentOutputTypeDef:
        """
        Returns the request payment configuration of a bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_request_payment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_request_payment)
        """
    async def get_bucket_tagging(
        self, *, Bucket: str, ExpectedBucketOwner: str = ...
    ) -> GetBucketTaggingOutputTypeDef:
        """
        Returns the tag set associated with the bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_tagging)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_tagging)
        """
    async def get_bucket_versioning(
        self, *, Bucket: str, ExpectedBucketOwner: str = ...
    ) -> GetBucketVersioningOutputTypeDef:
        """
        Returns the versioning state of a bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_versioning)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_versioning)
        """
    async def get_bucket_website(
        self, *, Bucket: str, ExpectedBucketOwner: str = ...
    ) -> GetBucketWebsiteOutputTypeDef:
        """
        Returns the website configuration for a bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_website)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_bucket_website)
        """
    async def get_object(
        self,
        *,
        Bucket: str,
        Key: str,
        IfMatch: str = ...,
        IfModifiedSince: Union[datetime, str] = ...,
        IfNoneMatch: str = ...,
        IfUnmodifiedSince: Union[datetime, str] = ...,
        Range: str = ...,
        ResponseCacheControl: str = ...,
        ResponseContentDisposition: str = ...,
        ResponseContentEncoding: str = ...,
        ResponseContentLanguage: str = ...,
        ResponseContentType: str = ...,
        ResponseExpires: Union[datetime, str] = ...,
        VersionId: str = ...,
        SSECustomerAlgorithm: str = ...,
        SSECustomerKey: str = ...,
        SSECustomerKeyMD5: str = ...,
        RequestPayer: Literal["requester"] = ...,
        PartNumber: int = ...,
        ExpectedBucketOwner: str = ...,
        ChecksumMode: Literal["ENABLED"] = ...
    ) -> GetObjectOutputTypeDef:
        """
        Retrieves objects from Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_object)
        """
    async def get_object_acl(
        self,
        *,
        Bucket: str,
        Key: str,
        VersionId: str = ...,
        RequestPayer: Literal["requester"] = ...,
        ExpectedBucketOwner: str = ...
    ) -> GetObjectAclOutputTypeDef:
        """
        Returns the access control list (ACL) of an object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object_acl)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_object_acl)
        """
    async def get_object_attributes(
        self,
        *,
        Bucket: str,
        Key: str,
        ObjectAttributes: Sequence[ObjectAttributesType],
        VersionId: str = ...,
        MaxParts: int = ...,
        PartNumberMarker: int = ...,
        SSECustomerAlgorithm: str = ...,
        SSECustomerKey: str = ...,
        SSECustomerKeyMD5: str = ...,
        RequestPayer: Literal["requester"] = ...,
        ExpectedBucketOwner: str = ...
    ) -> GetObjectAttributesOutputTypeDef:
        """
        Retrieves all the metadata from an object without returning the object itself.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_object_attributes)
        """
    async def get_object_legal_hold(
        self,
        *,
        Bucket: str,
        Key: str,
        VersionId: str = ...,
        RequestPayer: Literal["requester"] = ...,
        ExpectedBucketOwner: str = ...
    ) -> GetObjectLegalHoldOutputTypeDef:
        """
        Gets an object's current legal hold status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object_legal_hold)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_object_legal_hold)
        """
    async def get_object_lock_configuration(
        self, *, Bucket: str, ExpectedBucketOwner: str = ...
    ) -> GetObjectLockConfigurationOutputTypeDef:
        """
        Gets the Object Lock configuration for a bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object_lock_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_object_lock_configuration)
        """
    async def get_object_retention(
        self,
        *,
        Bucket: str,
        Key: str,
        VersionId: str = ...,
        RequestPayer: Literal["requester"] = ...,
        ExpectedBucketOwner: str = ...
    ) -> GetObjectRetentionOutputTypeDef:
        """
        Retrieves an object's retention settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object_retention)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_object_retention)
        """
    async def get_object_tagging(
        self,
        *,
        Bucket: str,
        Key: str,
        VersionId: str = ...,
        ExpectedBucketOwner: str = ...,
        RequestPayer: Literal["requester"] = ...
    ) -> GetObjectTaggingOutputTypeDef:
        """
        Returns the tag-set of an object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object_tagging)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_object_tagging)
        """
    async def get_object_torrent(
        self,
        *,
        Bucket: str,
        Key: str,
        RequestPayer: Literal["requester"] = ...,
        ExpectedBucketOwner: str = ...
    ) -> GetObjectTorrentOutputTypeDef:
        """
        Returns torrent files from a bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object_torrent)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_object_torrent)
        """
    async def get_public_access_block(
        self, *, Bucket: str, ExpectedBucketOwner: str = ...
    ) -> GetPublicAccessBlockOutputTypeDef:
        """
        Retrieves the `PublicAccessBlock` configuration for an Amazon S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_public_access_block)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_public_access_block)
        """
    async def head_bucket(self, *, Bucket: str, ExpectedBucketOwner: str = ...) -> None:
        """
        This action is useful to determine if a bucket exists and you have permission to
        access it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.head_bucket)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#head_bucket)
        """
    async def head_object(
        self,
        *,
        Bucket: str,
        Key: str,
        IfMatch: str = ...,
        IfModifiedSince: Union[datetime, str] = ...,
        IfNoneMatch: str = ...,
        IfUnmodifiedSince: Union[datetime, str] = ...,
        Range: str = ...,
        VersionId: str = ...,
        SSECustomerAlgorithm: str = ...,
        SSECustomerKey: str = ...,
        SSECustomerKeyMD5: str = ...,
        RequestPayer: Literal["requester"] = ...,
        PartNumber: int = ...,
        ExpectedBucketOwner: str = ...,
        ChecksumMode: Literal["ENABLED"] = ...
    ) -> HeadObjectOutputTypeDef:
        """
        The HEAD action retrieves metadata from an object without returning the object
        itself.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.head_object)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#head_object)
        """
    async def list_bucket_analytics_configurations(
        self, *, Bucket: str, ContinuationToken: str = ..., ExpectedBucketOwner: str = ...
    ) -> ListBucketAnalyticsConfigurationsOutputTypeDef:
        """
        Lists the analytics configurations for the bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_bucket_analytics_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#list_bucket_analytics_configurations)
        """
    async def list_bucket_intelligent_tiering_configurations(
        self, *, Bucket: str, ContinuationToken: str = ...
    ) -> ListBucketIntelligentTieringConfigurationsOutputTypeDef:
        """
        Lists the S3 Intelligent-Tiering configuration from the specified bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_bucket_intelligent_tiering_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#list_bucket_intelligent_tiering_configurations)
        """
    async def list_bucket_inventory_configurations(
        self, *, Bucket: str, ContinuationToken: str = ..., ExpectedBucketOwner: str = ...
    ) -> ListBucketInventoryConfigurationsOutputTypeDef:
        """
        Returns a list of inventory configurations for the bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_bucket_inventory_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#list_bucket_inventory_configurations)
        """
    async def list_bucket_metrics_configurations(
        self, *, Bucket: str, ContinuationToken: str = ..., ExpectedBucketOwner: str = ...
    ) -> ListBucketMetricsConfigurationsOutputTypeDef:
        """
        Lists the metrics configurations for the bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_bucket_metrics_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#list_bucket_metrics_configurations)
        """
    async def list_buckets(self) -> ListBucketsOutputTypeDef:
        """
        Returns a list of all buckets owned by the authenticated sender of the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_buckets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#list_buckets)
        """
    async def list_multipart_uploads(
        self,
        *,
        Bucket: str,
        Delimiter: str = ...,
        EncodingType: Literal["url"] = ...,
        KeyMarker: str = ...,
        MaxUploads: int = ...,
        Prefix: str = ...,
        UploadIdMarker: str = ...,
        ExpectedBucketOwner: str = ...
    ) -> ListMultipartUploadsOutputTypeDef:
        """
        This action lists in-progress multipart uploads.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_multipart_uploads)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#list_multipart_uploads)
        """
    async def list_object_versions(
        self,
        *,
        Bucket: str,
        Delimiter: str = ...,
        EncodingType: Literal["url"] = ...,
        KeyMarker: str = ...,
        MaxKeys: int = ...,
        Prefix: str = ...,
        VersionIdMarker: str = ...,
        ExpectedBucketOwner: str = ...
    ) -> ListObjectVersionsOutputTypeDef:
        """
        Returns metadata about all versions of the objects in a bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_object_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#list_object_versions)
        """
    async def list_objects(
        self,
        *,
        Bucket: str,
        Delimiter: str = ...,
        EncodingType: Literal["url"] = ...,
        Marker: str = ...,
        MaxKeys: int = ...,
        Prefix: str = ...,
        RequestPayer: Literal["requester"] = ...,
        ExpectedBucketOwner: str = ...
    ) -> ListObjectsOutputTypeDef:
        """
        Returns some or all (up to 1,000) of the objects in a bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_objects)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#list_objects)
        """
    async def list_objects_v2(
        self,
        *,
        Bucket: str,
        Delimiter: str = ...,
        EncodingType: Literal["url"] = ...,
        MaxKeys: int = ...,
        Prefix: str = ...,
        ContinuationToken: str = ...,
        FetchOwner: bool = ...,
        StartAfter: str = ...,
        RequestPayer: Literal["requester"] = ...,
        ExpectedBucketOwner: str = ...
    ) -> ListObjectsV2OutputTypeDef:
        """
        Returns some or all (up to 1,000) of the objects in a bucket with each request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_objects_v2)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#list_objects_v2)
        """
    async def list_parts(
        self,
        *,
        Bucket: str,
        Key: str,
        UploadId: str,
        MaxParts: int = ...,
        PartNumberMarker: int = ...,
        RequestPayer: Literal["requester"] = ...,
        ExpectedBucketOwner: str = ...,
        SSECustomerAlgorithm: str = ...,
        SSECustomerKey: str = ...,
        SSECustomerKeyMD5: str = ...
    ) -> ListPartsOutputTypeDef:
        """
        Lists the parts that have been uploaded for a specific multipart upload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_parts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#list_parts)
        """
    async def put_bucket_accelerate_configuration(
        self,
        *,
        Bucket: str,
        AccelerateConfiguration: "AccelerateConfigurationTypeDef",
        ExpectedBucketOwner: str = ...,
        ChecksumAlgorithm: ChecksumAlgorithmType = ...
    ) -> None:
        """
        Sets the accelerate configuration of an existing bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_accelerate_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_accelerate_configuration)
        """
    async def put_bucket_acl(
        self,
        *,
        Bucket: str,
        ACL: BucketCannedACLType = ...,
        AccessControlPolicy: "AccessControlPolicyTypeDef" = ...,
        ChecksumAlgorithm: ChecksumAlgorithmType = ...,
        GrantFullControl: str = ...,
        GrantRead: str = ...,
        GrantReadACP: str = ...,
        GrantWrite: str = ...,
        GrantWriteACP: str = ...,
        ExpectedBucketOwner: str = ...
    ) -> None:
        """
        Sets the permissions on an existing bucket using access control lists (ACL).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_acl)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_acl)
        """
    async def put_bucket_analytics_configuration(
        self,
        *,
        Bucket: str,
        Id: str,
        AnalyticsConfiguration: "AnalyticsConfigurationTypeDef",
        ExpectedBucketOwner: str = ...
    ) -> None:
        """
        Sets an analytics configuration for the bucket (specified by the analytics
        configuration ID).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_analytics_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_analytics_configuration)
        """
    async def put_bucket_cors(
        self,
        *,
        Bucket: str,
        CORSConfiguration: "CORSConfigurationTypeDef",
        ChecksumAlgorithm: ChecksumAlgorithmType = ...,
        ExpectedBucketOwner: str = ...
    ) -> None:
        """
        Sets the `cors` configuration for your bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_cors)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_cors)
        """
    async def put_bucket_encryption(
        self,
        *,
        Bucket: str,
        ServerSideEncryptionConfiguration: "ServerSideEncryptionConfigurationTypeDef",
        ContentMD5: str = ...,
        ChecksumAlgorithm: ChecksumAlgorithmType = ...,
        ExpectedBucketOwner: str = ...
    ) -> None:
        """
        This action uses the `encryption` subresource to configure default encryption
        and Amazon S3 Bucket Key for an existing bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_encryption)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_encryption)
        """
    async def put_bucket_intelligent_tiering_configuration(
        self,
        *,
        Bucket: str,
        Id: str,
        IntelligentTieringConfiguration: "IntelligentTieringConfigurationTypeDef"
    ) -> None:
        """
        Puts a S3 Intelligent-Tiering configuration to the specified bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_intelligent_tiering_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_intelligent_tiering_configuration)
        """
    async def put_bucket_inventory_configuration(
        self,
        *,
        Bucket: str,
        Id: str,
        InventoryConfiguration: "InventoryConfigurationTypeDef",
        ExpectedBucketOwner: str = ...
    ) -> None:
        """
        This implementation of the `PUT` action adds an inventory configuration
        (identified by the inventory ID) to the bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_inventory_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_inventory_configuration)
        """
    async def put_bucket_lifecycle(
        self,
        *,
        Bucket: str,
        ChecksumAlgorithm: ChecksumAlgorithmType = ...,
        LifecycleConfiguration: "LifecycleConfigurationTypeDef" = ...,
        ExpectedBucketOwner: str = ...
    ) -> None:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_lifecycle)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_lifecycle)
        """
    async def put_bucket_lifecycle_configuration(
        self,
        *,
        Bucket: str,
        ChecksumAlgorithm: ChecksumAlgorithmType = ...,
        LifecycleConfiguration: "BucketLifecycleConfigurationTypeDef" = ...,
        ExpectedBucketOwner: str = ...
    ) -> None:
        """
        Creates a new lifecycle configuration for the bucket or replaces an existing
        lifecycle configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_lifecycle_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_lifecycle_configuration)
        """
    async def put_bucket_logging(
        self,
        *,
        Bucket: str,
        BucketLoggingStatus: "BucketLoggingStatusTypeDef",
        ChecksumAlgorithm: ChecksumAlgorithmType = ...,
        ExpectedBucketOwner: str = ...
    ) -> None:
        """
        Set the logging parameters for a bucket and to specify permissions for who can
        view and modify the logging parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_logging)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_logging)
        """
    async def put_bucket_metrics_configuration(
        self,
        *,
        Bucket: str,
        Id: str,
        MetricsConfiguration: "MetricsConfigurationTypeDef",
        ExpectedBucketOwner: str = ...
    ) -> None:
        """
        Sets a metrics configuration (specified by the metrics configuration ID) for the
        bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_metrics_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_metrics_configuration)
        """
    async def put_bucket_notification(
        self,
        *,
        Bucket: str,
        NotificationConfiguration: "NotificationConfigurationDeprecatedTypeDef",
        ChecksumAlgorithm: ChecksumAlgorithmType = ...,
        ExpectedBucketOwner: str = ...
    ) -> None:
        """
        No longer used, see the
        [PutBucketNotificationConfiguration](https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketNotificationConfiguration.html)_
        operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_notification)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_notification)
        """
    async def put_bucket_notification_configuration(
        self,
        *,
        Bucket: str,
        NotificationConfiguration: "NotificationConfigurationTypeDef",
        ExpectedBucketOwner: str = ...,
        SkipDestinationValidation: bool = ...
    ) -> None:
        """
        Enables notifications of specified events for a bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_notification_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_notification_configuration)
        """
    async def put_bucket_ownership_controls(
        self,
        *,
        Bucket: str,
        OwnershipControls: "OwnershipControlsTypeDef",
        ContentMD5: str = ...,
        ExpectedBucketOwner: str = ...
    ) -> None:
        """
        Creates or modifies `OwnershipControls` for an Amazon S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_ownership_controls)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_ownership_controls)
        """
    async def put_bucket_policy(
        self,
        *,
        Bucket: str,
        Policy: str,
        ChecksumAlgorithm: ChecksumAlgorithmType = ...,
        ConfirmRemoveSelfBucketAccess: bool = ...,
        ExpectedBucketOwner: str = ...
    ) -> None:
        """
        Applies an Amazon S3 bucket policy to an Amazon S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_policy)
        """
    async def put_bucket_replication(
        self,
        *,
        Bucket: str,
        ReplicationConfiguration: "ReplicationConfigurationTypeDef",
        ChecksumAlgorithm: ChecksumAlgorithmType = ...,
        Token: str = ...,
        ExpectedBucketOwner: str = ...
    ) -> None:
        """
        Creates a replication configuration or replaces an existing one.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_replication)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_replication)
        """
    async def put_bucket_request_payment(
        self,
        *,
        Bucket: str,
        RequestPaymentConfiguration: "RequestPaymentConfigurationTypeDef",
        ChecksumAlgorithm: ChecksumAlgorithmType = ...,
        ExpectedBucketOwner: str = ...
    ) -> None:
        """
        Sets the request payment configuration for a bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_request_payment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_request_payment)
        """
    async def put_bucket_tagging(
        self,
        *,
        Bucket: str,
        Tagging: "TaggingTypeDef",
        ChecksumAlgorithm: ChecksumAlgorithmType = ...,
        ExpectedBucketOwner: str = ...
    ) -> None:
        """
        Sets the tags for a bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_tagging)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_tagging)
        """
    async def put_bucket_versioning(
        self,
        *,
        Bucket: str,
        VersioningConfiguration: "VersioningConfigurationTypeDef",
        ChecksumAlgorithm: ChecksumAlgorithmType = ...,
        MFA: str = ...,
        ExpectedBucketOwner: str = ...
    ) -> None:
        """
        Sets the versioning state of an existing bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_versioning)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_versioning)
        """
    async def put_bucket_website(
        self,
        *,
        Bucket: str,
        WebsiteConfiguration: "WebsiteConfigurationTypeDef",
        ChecksumAlgorithm: ChecksumAlgorithmType = ...,
        ExpectedBucketOwner: str = ...
    ) -> None:
        """
        Sets the configuration of the website that is specified in the `website`
        subresource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_website)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_bucket_website)
        """
    async def put_object(
        self,
        *,
        Bucket: str,
        Key: str,
        ACL: ObjectCannedACLType = ...,
        Body: Union[str, bytes, IO[Any], StreamingBody] = ...,
        CacheControl: str = ...,
        ContentDisposition: str = ...,
        ContentEncoding: str = ...,
        ContentLanguage: str = ...,
        ContentLength: int = ...,
        ContentMD5: str = ...,
        ContentType: str = ...,
        ChecksumAlgorithm: ChecksumAlgorithmType = ...,
        ChecksumCRC32: str = ...,
        ChecksumCRC32C: str = ...,
        ChecksumSHA1: str = ...,
        ChecksumSHA256: str = ...,
        Expires: Union[datetime, str] = ...,
        GrantFullControl: str = ...,
        GrantRead: str = ...,
        GrantReadACP: str = ...,
        GrantWriteACP: str = ...,
        Metadata: Mapping[str, str] = ...,
        ServerSideEncryption: ServerSideEncryptionType = ...,
        StorageClass: StorageClassType = ...,
        WebsiteRedirectLocation: str = ...,
        SSECustomerAlgorithm: str = ...,
        SSECustomerKey: str = ...,
        SSECustomerKeyMD5: str = ...,
        SSEKMSKeyId: str = ...,
        SSEKMSEncryptionContext: str = ...,
        BucketKeyEnabled: bool = ...,
        RequestPayer: Literal["requester"] = ...,
        Tagging: str = ...,
        ObjectLockMode: ObjectLockModeType = ...,
        ObjectLockRetainUntilDate: Union[datetime, str] = ...,
        ObjectLockLegalHoldStatus: ObjectLockLegalHoldStatusType = ...,
        ExpectedBucketOwner: str = ...
    ) -> PutObjectOutputTypeDef:
        """
        Adds an object to a bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_object)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_object)
        """
    async def put_object_acl(
        self,
        *,
        Bucket: str,
        Key: str,
        ACL: ObjectCannedACLType = ...,
        AccessControlPolicy: "AccessControlPolicyTypeDef" = ...,
        ChecksumAlgorithm: ChecksumAlgorithmType = ...,
        GrantFullControl: str = ...,
        GrantRead: str = ...,
        GrantReadACP: str = ...,
        GrantWrite: str = ...,
        GrantWriteACP: str = ...,
        RequestPayer: Literal["requester"] = ...,
        VersionId: str = ...,
        ExpectedBucketOwner: str = ...
    ) -> PutObjectAclOutputTypeDef:
        """
        Uses the `acl` subresource to set the access control list (ACL) permissions for
        a new or existing object in an S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_object_acl)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_object_acl)
        """
    async def put_object_legal_hold(
        self,
        *,
        Bucket: str,
        Key: str,
        LegalHold: "ObjectLockLegalHoldTypeDef" = ...,
        RequestPayer: Literal["requester"] = ...,
        VersionId: str = ...,
        ContentMD5: str = ...,
        ChecksumAlgorithm: ChecksumAlgorithmType = ...,
        ExpectedBucketOwner: str = ...
    ) -> PutObjectLegalHoldOutputTypeDef:
        """
        Applies a legal hold configuration to the specified object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_object_legal_hold)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_object_legal_hold)
        """
    async def put_object_lock_configuration(
        self,
        *,
        Bucket: str,
        ObjectLockConfiguration: "ObjectLockConfigurationTypeDef" = ...,
        RequestPayer: Literal["requester"] = ...,
        Token: str = ...,
        ContentMD5: str = ...,
        ChecksumAlgorithm: ChecksumAlgorithmType = ...,
        ExpectedBucketOwner: str = ...
    ) -> PutObjectLockConfigurationOutputTypeDef:
        """
        Places an Object Lock configuration on the specified bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_object_lock_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_object_lock_configuration)
        """
    async def put_object_retention(
        self,
        *,
        Bucket: str,
        Key: str,
        Retention: "ObjectLockRetentionTypeDef" = ...,
        RequestPayer: Literal["requester"] = ...,
        VersionId: str = ...,
        BypassGovernanceRetention: bool = ...,
        ContentMD5: str = ...,
        ChecksumAlgorithm: ChecksumAlgorithmType = ...,
        ExpectedBucketOwner: str = ...
    ) -> PutObjectRetentionOutputTypeDef:
        """
        Places an Object Retention configuration on an object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_object_retention)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_object_retention)
        """
    async def put_object_tagging(
        self,
        *,
        Bucket: str,
        Key: str,
        Tagging: "TaggingTypeDef",
        VersionId: str = ...,
        ContentMD5: str = ...,
        ChecksumAlgorithm: ChecksumAlgorithmType = ...,
        ExpectedBucketOwner: str = ...,
        RequestPayer: Literal["requester"] = ...
    ) -> PutObjectTaggingOutputTypeDef:
        """
        Sets the supplied tag-set to an object that already exists in a bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_object_tagging)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_object_tagging)
        """
    async def put_public_access_block(
        self,
        *,
        Bucket: str,
        PublicAccessBlockConfiguration: "PublicAccessBlockConfigurationTypeDef",
        ContentMD5: str = ...,
        ChecksumAlgorithm: ChecksumAlgorithmType = ...,
        ExpectedBucketOwner: str = ...
    ) -> None:
        """
        Creates or modifies the `PublicAccessBlock` configuration for an Amazon S3
        bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_public_access_block)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#put_public_access_block)
        """
    async def restore_object(
        self,
        *,
        Bucket: str,
        Key: str,
        VersionId: str = ...,
        RestoreRequest: "RestoreRequestTypeDef" = ...,
        RequestPayer: Literal["requester"] = ...,
        ChecksumAlgorithm: ChecksumAlgorithmType = ...,
        ExpectedBucketOwner: str = ...
    ) -> RestoreObjectOutputTypeDef:
        """
        Restores an archived copy of an object back into Amazon S3 This action is not
        supported by Amazon S3 on Outposts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.restore_object)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#restore_object)
        """
    async def select_object_content(
        self,
        *,
        Bucket: str,
        Key: str,
        Expression: str,
        ExpressionType: Literal["SQL"],
        InputSerialization: "InputSerializationTypeDef",
        OutputSerialization: "OutputSerializationTypeDef",
        SSECustomerAlgorithm: str = ...,
        SSECustomerKey: str = ...,
        SSECustomerKeyMD5: str = ...,
        RequestProgress: "RequestProgressTypeDef" = ...,
        ScanRange: "ScanRangeTypeDef" = ...,
        ExpectedBucketOwner: str = ...
    ) -> SelectObjectContentOutputTypeDef:
        """
        This action filters the contents of an Amazon S3 object based on a simple
        structured query language (SQL) statement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.select_object_content)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#select_object_content)
        """
    async def upload_file(
        self,
        Filename: str,
        Bucket: str,
        Key: str,
        ExtraArgs: Dict[str, Any] = ...,
        Callback: Callable[..., Any] = ...,
        Config: TransferConfig = ...,
    ) -> None:
        """
        Upload a file to an S3 object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.upload_file)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#upload_file)
        """
    async def upload_fileobj(
        self,
        Fileobj: Union[IO[Any], StreamingBody],
        Bucket: str,
        Key: str,
        ExtraArgs: Dict[str, Any] = ...,
        Callback: Callable[..., Any] = ...,
        Config: TransferConfig = ...,
    ) -> None:
        """
        Upload a file-like object to S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.upload_fileobj)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#upload_fileobj)
        """
    async def upload_part(
        self,
        *,
        Bucket: str,
        Key: str,
        PartNumber: int,
        UploadId: str,
        Body: Union[str, bytes, IO[Any], StreamingBody] = ...,
        ContentLength: int = ...,
        ContentMD5: str = ...,
        ChecksumAlgorithm: ChecksumAlgorithmType = ...,
        ChecksumCRC32: str = ...,
        ChecksumCRC32C: str = ...,
        ChecksumSHA1: str = ...,
        ChecksumSHA256: str = ...,
        SSECustomerAlgorithm: str = ...,
        SSECustomerKey: str = ...,
        SSECustomerKeyMD5: str = ...,
        RequestPayer: Literal["requester"] = ...,
        ExpectedBucketOwner: str = ...
    ) -> UploadPartOutputTypeDef:
        """
        Uploads a part in a multipart upload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.upload_part)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#upload_part)
        """
    async def upload_part_copy(
        self,
        *,
        Bucket: str,
        CopySource: Union[str, "CopySourceTypeDef"],
        Key: str,
        PartNumber: int,
        UploadId: str,
        CopySourceIfMatch: str = ...,
        CopySourceIfModifiedSince: Union[datetime, str] = ...,
        CopySourceIfNoneMatch: str = ...,
        CopySourceIfUnmodifiedSince: Union[datetime, str] = ...,
        CopySourceRange: str = ...,
        SSECustomerAlgorithm: str = ...,
        SSECustomerKey: str = ...,
        SSECustomerKeyMD5: str = ...,
        CopySourceSSECustomerAlgorithm: str = ...,
        CopySourceSSECustomerKey: str = ...,
        CopySourceSSECustomerKeyMD5: str = ...,
        RequestPayer: Literal["requester"] = ...,
        ExpectedBucketOwner: str = ...,
        ExpectedSourceBucketOwner: str = ...
    ) -> UploadPartCopyOutputTypeDef:
        """
        Uploads a part by copying data from an existing object as data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.upload_part_copy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#upload_part_copy)
        """
    async def write_get_object_response(
        self,
        *,
        RequestRoute: str,
        RequestToken: str,
        Body: Union[str, bytes, IO[Any], StreamingBody] = ...,
        StatusCode: int = ...,
        ErrorCode: str = ...,
        ErrorMessage: str = ...,
        AcceptRanges: str = ...,
        CacheControl: str = ...,
        ContentDisposition: str = ...,
        ContentEncoding: str = ...,
        ContentLanguage: str = ...,
        ContentLength: int = ...,
        ContentRange: str = ...,
        ContentType: str = ...,
        ChecksumCRC32: str = ...,
        ChecksumCRC32C: str = ...,
        ChecksumSHA1: str = ...,
        ChecksumSHA256: str = ...,
        DeleteMarker: bool = ...,
        ETag: str = ...,
        Expires: Union[datetime, str] = ...,
        Expiration: str = ...,
        LastModified: Union[datetime, str] = ...,
        MissingMeta: int = ...,
        Metadata: Mapping[str, str] = ...,
        ObjectLockMode: ObjectLockModeType = ...,
        ObjectLockLegalHoldStatus: ObjectLockLegalHoldStatusType = ...,
        ObjectLockRetainUntilDate: Union[datetime, str] = ...,
        PartsCount: int = ...,
        ReplicationStatus: ReplicationStatusType = ...,
        RequestCharged: Literal["requester"] = ...,
        Restore: str = ...,
        ServerSideEncryption: ServerSideEncryptionType = ...,
        SSECustomerAlgorithm: str = ...,
        SSEKMSKeyId: str = ...,
        SSECustomerKeyMD5: str = ...,
        StorageClass: StorageClassType = ...,
        TagCount: int = ...,
        VersionId: str = ...,
        BucketKeyEnabled: bool = ...
    ) -> None:
        """
        Passes transformed objects to a `GetObject` operation when using Object Lambda
        access points.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.write_get_object_response)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#write_get_object_response)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_multipart_uploads"]
    ) -> ListMultipartUploadsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_object_versions"]
    ) -> ListObjectVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_objects"]) -> ListObjectsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_objects_v2"]) -> ListObjectsV2Paginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_parts"]) -> ListPartsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_paginator)
        """
    @overload
    def get_waiter(self, waiter_name: Literal["bucket_exists"]) -> BucketExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_waiter)
        """
    @overload
    def get_waiter(self, waiter_name: Literal["bucket_not_exists"]) -> BucketNotExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_waiter)
        """
    @overload
    def get_waiter(self, waiter_name: Literal["object_exists"]) -> ObjectExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_waiter)
        """
    @overload
    def get_waiter(self, waiter_name: Literal["object_not_exists"]) -> ObjectNotExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/#get_waiter)
        """
    async def __aenter__(self) -> "S3Client":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3/client/)
        """
