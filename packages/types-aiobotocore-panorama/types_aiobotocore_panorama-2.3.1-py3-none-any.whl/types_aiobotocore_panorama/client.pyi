"""
Type annotations for panorama service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_panorama.client import PanoramaClient

    session = get_session()
    async with session.create_client("panorama") as client:
        client: PanoramaClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import NodeCategoryType, PackageImportJobTypeType, StatusFilterType
from .type_defs import (
    CreateApplicationInstanceResponseTypeDef,
    CreateJobForDevicesResponseTypeDef,
    CreateNodeFromTemplateJobResponseTypeDef,
    CreatePackageImportJobResponseTypeDef,
    CreatePackageResponseTypeDef,
    DeleteDeviceResponseTypeDef,
    DescribeApplicationInstanceDetailsResponseTypeDef,
    DescribeApplicationInstanceResponseTypeDef,
    DescribeDeviceJobResponseTypeDef,
    DescribeDeviceResponseTypeDef,
    DescribeNodeFromTemplateJobResponseTypeDef,
    DescribeNodeResponseTypeDef,
    DescribePackageImportJobResponseTypeDef,
    DescribePackageResponseTypeDef,
    DescribePackageVersionResponseTypeDef,
    DeviceJobConfigTypeDef,
    JobResourceTagsTypeDef,
    ListApplicationInstanceDependenciesResponseTypeDef,
    ListApplicationInstanceNodeInstancesResponseTypeDef,
    ListApplicationInstancesResponseTypeDef,
    ListDevicesJobsResponseTypeDef,
    ListDevicesResponseTypeDef,
    ListNodeFromTemplateJobsResponseTypeDef,
    ListNodesResponseTypeDef,
    ListPackageImportJobsResponseTypeDef,
    ListPackagesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ManifestOverridesPayloadTypeDef,
    ManifestPayloadTypeDef,
    NetworkPayloadTypeDef,
    PackageImportJobInputConfigTypeDef,
    PackageImportJobOutputConfigTypeDef,
    ProvisionDeviceResponseTypeDef,
    UpdateDeviceMetadataResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("PanoramaClient",)

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
    ValidationException: Type[BotocoreClientError]

class PanoramaClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        PanoramaClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#exceptions)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#can_paginate)
        """
    async def create_application_instance(
        self,
        *,
        DefaultRuntimeContextDevice: str,
        ManifestPayload: "ManifestPayloadTypeDef",
        ApplicationInstanceIdToReplace: str = ...,
        Description: str = ...,
        ManifestOverridesPayload: "ManifestOverridesPayloadTypeDef" = ...,
        Name: str = ...,
        RuntimeRoleArn: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> CreateApplicationInstanceResponseTypeDef:
        """
        Creates an application instance and deploys it to a device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.create_application_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#create_application_instance)
        """
    async def create_job_for_devices(
        self,
        *,
        DeviceIds: Sequence[str],
        DeviceJobConfig: "DeviceJobConfigTypeDef",
        JobType: Literal["OTA"]
    ) -> CreateJobForDevicesResponseTypeDef:
        """
        Creates a job to run on one or more devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.create_job_for_devices)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#create_job_for_devices)
        """
    async def create_node_from_template_job(
        self,
        *,
        NodeName: str,
        OutputPackageName: str,
        OutputPackageVersion: str,
        TemplateParameters: Mapping[str, str],
        TemplateType: Literal["RTSP_CAMERA_STREAM"],
        JobTags: Sequence["JobResourceTagsTypeDef"] = ...,
        NodeDescription: str = ...
    ) -> CreateNodeFromTemplateJobResponseTypeDef:
        """
        Creates a camera stream node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.create_node_from_template_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#create_node_from_template_job)
        """
    async def create_package(
        self, *, PackageName: str, Tags: Mapping[str, str] = ...
    ) -> CreatePackageResponseTypeDef:
        """
        Creates a package and storage location in an Amazon S3 access point.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.create_package)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#create_package)
        """
    async def create_package_import_job(
        self,
        *,
        ClientToken: str,
        InputConfig: "PackageImportJobInputConfigTypeDef",
        JobType: PackageImportJobTypeType,
        OutputConfig: "PackageImportJobOutputConfigTypeDef",
        JobTags: Sequence["JobResourceTagsTypeDef"] = ...
    ) -> CreatePackageImportJobResponseTypeDef:
        """
        Imports a node package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.create_package_import_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#create_package_import_job)
        """
    async def delete_device(self, *, DeviceId: str) -> DeleteDeviceResponseTypeDef:
        """
        Deletes a device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.delete_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#delete_device)
        """
    async def delete_package(self, *, PackageId: str, ForceDelete: bool = ...) -> Dict[str, Any]:
        """
        Deletes a package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.delete_package)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#delete_package)
        """
    async def deregister_package_version(
        self,
        *,
        PackageId: str,
        PackageVersion: str,
        PatchVersion: str,
        OwnerAccount: str = ...,
        UpdatedLatestPatchVersion: str = ...
    ) -> Dict[str, Any]:
        """
        Deregisters a package version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.deregister_package_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#deregister_package_version)
        """
    async def describe_application_instance(
        self, *, ApplicationInstanceId: str
    ) -> DescribeApplicationInstanceResponseTypeDef:
        """
        Returns information about an application instance on a device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.describe_application_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#describe_application_instance)
        """
    async def describe_application_instance_details(
        self, *, ApplicationInstanceId: str
    ) -> DescribeApplicationInstanceDetailsResponseTypeDef:
        """
        Returns information about an application instance's configuration manifest.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.describe_application_instance_details)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#describe_application_instance_details)
        """
    async def describe_device(self, *, DeviceId: str) -> DescribeDeviceResponseTypeDef:
        """
        Returns information about a device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.describe_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#describe_device)
        """
    async def describe_device_job(self, *, JobId: str) -> DescribeDeviceJobResponseTypeDef:
        """
        Returns information about a device job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.describe_device_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#describe_device_job)
        """
    async def describe_node(
        self, *, NodeId: str, OwnerAccount: str = ...
    ) -> DescribeNodeResponseTypeDef:
        """
        Returns information about a node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.describe_node)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#describe_node)
        """
    async def describe_node_from_template_job(
        self, *, JobId: str
    ) -> DescribeNodeFromTemplateJobResponseTypeDef:
        """
        Returns information about a job to create a camera stream node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.describe_node_from_template_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#describe_node_from_template_job)
        """
    async def describe_package(self, *, PackageId: str) -> DescribePackageResponseTypeDef:
        """
        Returns information about a package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.describe_package)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#describe_package)
        """
    async def describe_package_import_job(
        self, *, JobId: str
    ) -> DescribePackageImportJobResponseTypeDef:
        """
        Returns information about a package import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.describe_package_import_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#describe_package_import_job)
        """
    async def describe_package_version(
        self,
        *,
        PackageId: str,
        PackageVersion: str,
        OwnerAccount: str = ...,
        PatchVersion: str = ...
    ) -> DescribePackageVersionResponseTypeDef:
        """
        Returns information about a package version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.describe_package_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#describe_package_version)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#generate_presigned_url)
        """
    async def list_application_instance_dependencies(
        self, *, ApplicationInstanceId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListApplicationInstanceDependenciesResponseTypeDef:
        """
        Returns a list of application instance dependencies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.list_application_instance_dependencies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#list_application_instance_dependencies)
        """
    async def list_application_instance_node_instances(
        self, *, ApplicationInstanceId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListApplicationInstanceNodeInstancesResponseTypeDef:
        """
        Returns a list of application node instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.list_application_instance_node_instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#list_application_instance_node_instances)
        """
    async def list_application_instances(
        self,
        *,
        DeviceId: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        StatusFilter: StatusFilterType = ...
    ) -> ListApplicationInstancesResponseTypeDef:
        """
        Returns a list of application instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.list_application_instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#list_application_instances)
        """
    async def list_devices(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListDevicesResponseTypeDef:
        """
        Returns a list of devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.list_devices)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#list_devices)
        """
    async def list_devices_jobs(
        self, *, DeviceId: str = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> ListDevicesJobsResponseTypeDef:
        """
        Returns a list of jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.list_devices_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#list_devices_jobs)
        """
    async def list_node_from_template_jobs(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListNodeFromTemplateJobsResponseTypeDef:
        """
        Returns a list of camera stream node jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.list_node_from_template_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#list_node_from_template_jobs)
        """
    async def list_nodes(
        self,
        *,
        Category: NodeCategoryType = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        OwnerAccount: str = ...,
        PackageName: str = ...,
        PackageVersion: str = ...,
        PatchVersion: str = ...
    ) -> ListNodesResponseTypeDef:
        """
        Returns a list of nodes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.list_nodes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#list_nodes)
        """
    async def list_package_import_jobs(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListPackageImportJobsResponseTypeDef:
        """
        Returns a list of package import jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.list_package_import_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#list_package_import_jobs)
        """
    async def list_packages(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListPackagesResponseTypeDef:
        """
        Returns a list of packages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.list_packages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#list_packages)
        """
    async def list_tags_for_resource(
        self, *, ResourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#list_tags_for_resource)
        """
    async def provision_device(
        self,
        *,
        Name: str,
        Description: str = ...,
        NetworkingConfiguration: "NetworkPayloadTypeDef" = ...,
        Tags: Mapping[str, str] = ...
    ) -> ProvisionDeviceResponseTypeDef:
        """
        Creates a device and returns a configuration archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.provision_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#provision_device)
        """
    async def register_package_version(
        self,
        *,
        PackageId: str,
        PackageVersion: str,
        PatchVersion: str,
        MarkLatest: bool = ...,
        OwnerAccount: str = ...
    ) -> Dict[str, Any]:
        """
        Registers a package version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.register_package_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#register_package_version)
        """
    async def remove_application_instance(self, *, ApplicationInstanceId: str) -> Dict[str, Any]:
        """
        Removes an application instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.remove_application_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#remove_application_instance)
        """
    async def tag_resource(self, *, ResourceArn: str, Tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Tags a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#tag_resource)
        """
    async def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#untag_resource)
        """
    async def update_device_metadata(
        self, *, DeviceId: str, Description: str = ...
    ) -> UpdateDeviceMetadataResponseTypeDef:
        """
        Updates a device's metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client.update_device_metadata)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/#update_device_metadata)
        """
    async def __aenter__(self) -> "PanoramaClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/panorama.html#Panorama.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_panorama/client/)
        """
