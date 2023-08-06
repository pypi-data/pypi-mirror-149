"""
Type annotations for glacier service ServiceResource

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_glacier.service_resource import GlacierServiceResource
    import types_aiobotocore_glacier.service_resource as glacier_resources

    session = get_session()
    async with session.resource("glacier") as resource:
        resource: GlacierServiceResource

        my_account: glacier_resources.Account = resource.Account(...)
        my_archive: glacier_resources.Archive = resource.Archive(...)
        my_job: glacier_resources.Job = resource.Job(...)
        my_multipart_upload: glacier_resources.MultipartUpload = resource.MultipartUpload(...)
        my_notification: glacier_resources.Notification = resource.Notification(...)
        my_vault: glacier_resources.Vault = resource.Vault(...)
```
"""
from typing import IO, Any, Iterator, List, Sequence, Union

from boto3.resources.base import ResourceMeta
from boto3.resources.base import ServiceResource as Boto3ServiceResource
from boto3.resources.collection import ResourceCollection
from botocore.response import StreamingBody

from .client import GlacierClient
from .literals import ActionCodeType, StatusCodeType
from .type_defs import (
    ArchiveCreationOutputTypeDef,
    CreateVaultOutputTypeDef,
    GetJobOutputOutputTypeDef,
    InventoryRetrievalJobDescriptionResponseMetadataTypeDef,
    ListPartsOutputTypeDef,
    OutputLocationResponseMetadataTypeDef,
    SelectParametersResponseMetadataTypeDef,
    UploadMultipartPartOutputTypeDef,
    VaultNotificationConfigTypeDef,
)

__all__ = (
    "GlacierServiceResource",
    "Account",
    "Archive",
    "Job",
    "MultipartUpload",
    "Notification",
    "Vault",
    "ServiceResourceVaultsCollection",
    "AccountVaultsCollection",
    "VaultCompletedJobsCollection",
    "VaultFailedJobsCollection",
    "VaultJobsCollection",
    "VaultJobsInProgressCollection",
    "VaultMultipartUplaodsCollection",
    "VaultMultipartUploadsCollection",
    "VaultSucceededJobsCollection",
)

class ServiceResourceVaultsCollection(ResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.vaults)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#serviceresourcevaultscollection)
    """

    async def all(self) -> "ServiceResourceVaultsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.vaults)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#serviceresourcevaultscollection)
        """
    async def filter(  # type: ignore
        self, *, marker: str = ..., limit: str = ...
    ) -> "ServiceResourceVaultsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.vaults)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#serviceresourcevaultscollection)
        """
    async def limit(self, count: int) -> "ServiceResourceVaultsCollection":
        """
        Return at most this many Vaults.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.vaults)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#serviceresourcevaultscollection)
        """
    async def page_size(self, count: int) -> "ServiceResourceVaultsCollection":
        """
        Fetch at most this many Vaults per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.vaults)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#serviceresourcevaultscollection)
        """
    async def pages(self) -> Iterator[List["Vault"]]:
        """
        A generator which yields pages of Vaults.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.vaults)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#serviceresourcevaultscollection)
        """
    async def __iter__(self) -> Iterator["Vault"]:
        """
        A generator which yields Vaults.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.vaults)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#serviceresourcevaultscollection)
        """

class AccountVaultsCollection(ResourceCollection):
    async def all(self) -> "AccountVaultsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """
    async def filter(  # type: ignore
        self, *, marker: str = ..., limit: str = ...
    ) -> "AccountVaultsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """
    async def limit(self, count: int) -> "AccountVaultsCollection":
        """
        Return at most this many Vaults.
        """
    async def page_size(self, count: int) -> "AccountVaultsCollection":
        """
        Fetch at most this many Vaults per service request.
        """
    async def pages(self) -> Iterator[List["Vault"]]:
        """
        A generator which yields pages of Vaults.
        """
    async def __iter__(self) -> Iterator["Vault"]:
        """
        A generator which yields Vaults.
        """

class VaultCompletedJobsCollection(ResourceCollection):
    async def all(self) -> "VaultCompletedJobsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """
    async def filter(  # type: ignore
        self, *, limit: str = ..., marker: str = ..., statuscode: str = ..., completed: str = ...
    ) -> "VaultCompletedJobsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """
    async def limit(self, count: int) -> "VaultCompletedJobsCollection":
        """
        Return at most this many Jobs.
        """
    async def page_size(self, count: int) -> "VaultCompletedJobsCollection":
        """
        Fetch at most this many Jobs per service request.
        """
    async def pages(self) -> Iterator[List["Job"]]:
        """
        A generator which yields pages of Jobs.
        """
    async def __iter__(self) -> Iterator["Job"]:
        """
        A generator which yields Jobs.
        """

class VaultFailedJobsCollection(ResourceCollection):
    async def all(self) -> "VaultFailedJobsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """
    async def filter(  # type: ignore
        self, *, limit: str = ..., marker: str = ..., statuscode: str = ..., completed: str = ...
    ) -> "VaultFailedJobsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """
    async def limit(self, count: int) -> "VaultFailedJobsCollection":
        """
        Return at most this many Jobs.
        """
    async def page_size(self, count: int) -> "VaultFailedJobsCollection":
        """
        Fetch at most this many Jobs per service request.
        """
    async def pages(self) -> Iterator[List["Job"]]:
        """
        A generator which yields pages of Jobs.
        """
    async def __iter__(self) -> Iterator["Job"]:
        """
        A generator which yields Jobs.
        """

class VaultJobsCollection(ResourceCollection):
    async def all(self) -> "VaultJobsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """
    async def filter(  # type: ignore
        self, *, limit: str = ..., marker: str = ..., statuscode: str = ..., completed: str = ...
    ) -> "VaultJobsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """
    async def limit(self, count: int) -> "VaultJobsCollection":
        """
        Return at most this many Jobs.
        """
    async def page_size(self, count: int) -> "VaultJobsCollection":
        """
        Fetch at most this many Jobs per service request.
        """
    async def pages(self) -> Iterator[List["Job"]]:
        """
        A generator which yields pages of Jobs.
        """
    async def __iter__(self) -> Iterator["Job"]:
        """
        A generator which yields Jobs.
        """

class VaultJobsInProgressCollection(ResourceCollection):
    async def all(self) -> "VaultJobsInProgressCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """
    async def filter(  # type: ignore
        self, *, limit: str = ..., marker: str = ..., statuscode: str = ..., completed: str = ...
    ) -> "VaultJobsInProgressCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """
    async def limit(self, count: int) -> "VaultJobsInProgressCollection":
        """
        Return at most this many Jobs.
        """
    async def page_size(self, count: int) -> "VaultJobsInProgressCollection":
        """
        Fetch at most this many Jobs per service request.
        """
    async def pages(self) -> Iterator[List["Job"]]:
        """
        A generator which yields pages of Jobs.
        """
    async def __iter__(self) -> Iterator["Job"]:
        """
        A generator which yields Jobs.
        """

class VaultMultipartUplaodsCollection(ResourceCollection):
    async def all(self) -> "VaultMultipartUplaodsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """
    async def filter(  # type: ignore
        self, *, marker: str = ..., limit: str = ...
    ) -> "VaultMultipartUplaodsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """
    async def limit(self, count: int) -> "VaultMultipartUplaodsCollection":
        """
        Return at most this many MultipartUploads.
        """
    async def page_size(self, count: int) -> "VaultMultipartUplaodsCollection":
        """
        Fetch at most this many MultipartUploads per service request.
        """
    async def pages(self) -> Iterator[List["MultipartUpload"]]:
        """
        A generator which yields pages of MultipartUploads.
        """
    async def __iter__(self) -> Iterator["MultipartUpload"]:
        """
        A generator which yields MultipartUploads.
        """

class VaultMultipartUploadsCollection(ResourceCollection):
    async def all(self) -> "VaultMultipartUploadsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """
    async def filter(  # type: ignore
        self, *, marker: str = ..., limit: str = ...
    ) -> "VaultMultipartUploadsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """
    async def limit(self, count: int) -> "VaultMultipartUploadsCollection":
        """
        Return at most this many MultipartUploads.
        """
    async def page_size(self, count: int) -> "VaultMultipartUploadsCollection":
        """
        Fetch at most this many MultipartUploads per service request.
        """
    async def pages(self) -> Iterator[List["MultipartUpload"]]:
        """
        A generator which yields pages of MultipartUploads.
        """
    async def __iter__(self) -> Iterator["MultipartUpload"]:
        """
        A generator which yields MultipartUploads.
        """

class VaultSucceededJobsCollection(ResourceCollection):
    async def all(self) -> "VaultSucceededJobsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """
    async def filter(  # type: ignore
        self, *, limit: str = ..., marker: str = ..., statuscode: str = ..., completed: str = ...
    ) -> "VaultSucceededJobsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """
    async def limit(self, count: int) -> "VaultSucceededJobsCollection":
        """
        Return at most this many Jobs.
        """
    async def page_size(self, count: int) -> "VaultSucceededJobsCollection":
        """
        Fetch at most this many Jobs per service request.
        """
    async def pages(self) -> Iterator[List["Job"]]:
        """
        A generator which yields pages of Jobs.
        """
    async def __iter__(self) -> Iterator["Job"]:
        """
        A generator which yields Jobs.
        """

class Job(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.Job)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#job)
    """

    job_id: str
    job_description: str
    action: ActionCodeType
    archive_id: str
    vault_arn: str
    creation_date: str
    completed: bool
    status_code: StatusCodeType
    status_message: str
    archive_size_in_bytes: int
    inventory_size_in_bytes: int
    sns_topic: str
    completion_date: str
    sha256_tree_hash: str
    archive_sha256_tree_hash: str
    retrieval_byte_range: str
    tier: str
    inventory_retrieval_parameters: InventoryRetrievalJobDescriptionResponseMetadataTypeDef
    job_output_path: str
    select_parameters: SelectParametersResponseMetadataTypeDef
    output_location: OutputLocationResponseMetadataTypeDef
    account_id: str
    vault_name: str
    id: str

    async def Vault(self) -> "_Vault":
        """
        Creates a Vault resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Job.Vault)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#jobvault-method)
        """
    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Job.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#jobget_available_subresources-method)
        """
    async def get_output(self, *, range: str = ...) -> GetJobOutputOutputTypeDef:
        """
        This operation downloads the output of the job you initiated using  InitiateJob.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Job.get_output)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#jobget_output-method)
        """
    async def load(self) -> None:
        """
        Calls :py:meth:`Glacier.Client.describe_job` to update the attributes of the Job
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Job.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#jobload-method)
        """
    async def reload(self) -> None:
        """
        Calls :py:meth:`Glacier.Client.describe_job` to update the attributes of the Job
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Job.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#jobreload-method)
        """

_Job = Job

class MultipartUpload(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.MultipartUpload)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#multipartupload)
    """

    multipart_upload_id: str
    vault_arn: str
    archive_description: str
    part_size_in_bytes: int
    creation_date: str
    account_id: str
    vault_name: str
    id: str

    async def Vault(self) -> "_Vault":
        """
        Creates a Vault resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.MultipartUpload.Vault)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#multipartuploadvault-method)
        """
    async def abort(self) -> None:
        """
        This operation aborts a multipart upload identified by the upload ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.MultipartUpload.abort)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#multipartuploadabort-method)
        """
    async def complete(
        self, *, archiveSize: str = ..., checksum: str = ...
    ) -> ArchiveCreationOutputTypeDef:
        """
        You call this operation to inform Amazon S3 Glacier (Glacier) that all the
        archive parts have been uploaded and that Glacier can now assemble the archive
        from the uploaded parts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.MultipartUpload.complete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#multipartuploadcomplete-method)
        """
    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.MultipartUpload.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#multipartuploadget_available_subresources-method)
        """
    async def parts(self, *, marker: str = ..., limit: str = ...) -> ListPartsOutputTypeDef:
        """
        This operation lists the parts of an archive that have been uploaded in a
        specific multipart upload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.MultipartUpload.parts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#multipartuploadparts-method)
        """
    async def upload_part(
        self,
        *,
        checksum: str = ...,
        range: str = ...,
        body: Union[str, bytes, IO[Any], StreamingBody] = ...
    ) -> UploadMultipartPartOutputTypeDef:
        """
        This operation uploads a part of an archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.MultipartUpload.upload_part)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#multipartuploadupload_part-method)
        """

_MultipartUpload = MultipartUpload

class Notification(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.Notification)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#notification)
    """

    sns_topic: str
    events: List[str]
    account_id: str
    vault_name: str

    async def Vault(self) -> "_Vault":
        """
        Creates a Vault resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Notification.Vault)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#notificationvault-method)
        """
    async def delete(self) -> None:
        """
        This operation deletes the notification configuration set for a vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Notification.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#notificationdelete-method)
        """
    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Notification.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#notificationget_available_subresources-method)
        """
    async def load(self) -> None:
        """
        Calls :py:meth:`Glacier.Client.get_vault_notifications` to update the attributes
        of the Notification resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Notification.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#notificationload-method)
        """
    async def reload(self) -> None:
        """
        Calls :py:meth:`Glacier.Client.get_vault_notifications` to update the attributes
        of the Notification resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Notification.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#notificationreload-method)
        """
    async def set(self, *, vaultNotificationConfig: "VaultNotificationConfigTypeDef" = ...) -> None:
        """
        This operation configures notifications that will be sent when specific events
        happen to a vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Notification.set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#notificationset-method)
        """

_Notification = Notification

class Account(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.Account)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#account)
    """

    id: str
    vaults: AccountVaultsCollection

    async def Vault(self, name: str) -> "_Vault":
        """
        Creates a Vault resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Account.Vault)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#accountvault-method)
        """
    async def create_vault(self, *, vaultName: str) -> "_Vault":
        """
        This operation creates a new vault with the specified name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Account.create_vault)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#accountcreate_vault-method)
        """
    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Account.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#accountget_available_subresources-method)
        """

_Account = Account

class Archive(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.Archive)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#archive)
    """

    account_id: str
    vault_name: str
    id: str

    async def Vault(self) -> "_Vault":
        """
        Creates a Vault resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Archive.Vault)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#archivevault-method)
        """
    async def delete(self) -> None:
        """
        This operation deletes an archive from a vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Archive.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#archivedelete-method)
        """
    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Archive.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#archiveget_available_subresources-method)
        """
    async def initiate_archive_retrieval(self) -> _Job:
        """
        This operation initiates a job of the specified type, which can be a select, an
        archival retrieval, or a vault retrieval.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Archive.initiate_archive_retrieval)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#archiveinitiate_archive_retrieval-method)
        """

_Archive = Archive

class Vault(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.Vault)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#vault)
    """

    vault_arn: str
    vault_name: str
    creation_date: str
    last_inventory_date: str
    number_of_archives: int
    size_in_bytes: int
    account_id: str
    name: str
    completed_jobs: VaultCompletedJobsCollection
    failed_jobs: VaultFailedJobsCollection
    jobs: VaultJobsCollection
    jobs_in_progress: VaultJobsInProgressCollection
    multipart_uplaods: VaultMultipartUplaodsCollection
    multipart_uploads: VaultMultipartUploadsCollection
    succeeded_jobs: VaultSucceededJobsCollection

    async def Account(self) -> _Account:
        """
        Creates a Account resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Vault.Account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#vaultaccount-method)
        """
    async def Archive(self, id: str) -> _Archive:
        """
        Creates a Archive resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Vault.Archive)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#vaultarchive-method)
        """
    async def Job(self, id: str) -> _Job:
        """
        Creates a Job resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Vault.Job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#vaultjob-method)
        """
    async def MultipartUpload(self, id: str) -> _MultipartUpload:
        """
        Creates a MultipartUpload resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Vault.MultipartUpload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#vaultmultipartupload-method)
        """
    async def Notification(self) -> _Notification:
        """
        Creates a Notification resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Vault.Notification)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#vaultnotification-method)
        """
    async def create(self) -> CreateVaultOutputTypeDef:
        """
        This operation creates a new vault with the specified name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Vault.create)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#vaultcreate-method)
        """
    async def delete(self) -> None:
        """
        This operation deletes a vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Vault.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#vaultdelete-method)
        """
    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Vault.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#vaultget_available_subresources-method)
        """
    async def initiate_inventory_retrieval(self) -> _Job:
        """
        This operation initiates a job of the specified type, which can be a select, an
        archival retrieval, or a vault retrieval.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Vault.initiate_inventory_retrieval)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#vaultinitiate_inventory_retrieval-method)
        """
    async def initiate_multipart_upload(
        self, *, archiveDescription: str = ..., partSize: str = ...
    ) -> _MultipartUpload:
        """
        This operation initiates a multipart upload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Vault.initiate_multipart_upload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#vaultinitiate_multipart_upload-method)
        """
    async def load(self) -> None:
        """
        Calls :py:meth:`Glacier.Client.describe_vault` to update the attributes of the
        Vault resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Vault.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#vaultload-method)
        """
    async def reload(self) -> None:
        """
        Calls :py:meth:`Glacier.Client.describe_vault` to update the attributes of the
        Vault resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Vault.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#vaultreload-method)
        """
    async def upload_archive(
        self,
        *,
        archiveDescription: str = ...,
        checksum: str = ...,
        body: Union[str, bytes, IO[Any], StreamingBody] = ...
    ) -> _Archive:
        """
        This operation adds an archive to a vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Vault.upload_archive)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#vaultupload_archive-method)
        """

_Vault = Vault

class GlacierResourceMeta(ResourceMeta):
    client: GlacierClient

class GlacierServiceResource(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/)
    """

    meta: "GlacierResourceMeta"
    vaults: ServiceResourceVaultsCollection

    async def Account(self, id: str) -> _Account:
        """
        Creates a Account resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.Account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#glacierserviceresourceaccount-method)
        """
    async def Archive(self, account_id: str, vault_name: str, id: str) -> _Archive:
        """
        Creates a Archive resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.Archive)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#glacierserviceresourcearchive-method)
        """
    async def Job(self, account_id: str, vault_name: str, id: str) -> _Job:
        """
        Creates a Job resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.Job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#glacierserviceresourcejob-method)
        """
    async def MultipartUpload(self, account_id: str, vault_name: str, id: str) -> _MultipartUpload:
        """
        Creates a MultipartUpload resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.MultipartUpload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#glacierserviceresourcemultipartupload-method)
        """
    async def Notification(self, account_id: str, vault_name: str) -> _Notification:
        """
        Creates a Notification resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.Notification)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#glacierserviceresourcenotification-method)
        """
    async def Vault(self, account_id: str, name: str) -> _Vault:
        """
        Creates a Vault resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.Vault)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#glacierserviceresourcevault-method)
        """
    async def create_vault(self, *, vaultName: str, accountId: str = "-") -> _Vault:
        """
        This operation creates a new vault with the specified name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.create_vault)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#glacierserviceresourcecreate_vault-method)
        """
    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.ServiceResource.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/service_resource/#glacierserviceresourceget_available_subresources-method)
        """
