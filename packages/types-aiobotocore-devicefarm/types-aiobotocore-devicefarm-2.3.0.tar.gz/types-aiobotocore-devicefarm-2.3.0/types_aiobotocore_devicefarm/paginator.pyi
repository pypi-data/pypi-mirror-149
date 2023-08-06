"""
Type annotations for devicefarm service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_devicefarm.client import DeviceFarmClient
    from types_aiobotocore_devicefarm.paginator import (
        GetOfferingStatusPaginator,
        ListArtifactsPaginator,
        ListDeviceInstancesPaginator,
        ListDevicePoolsPaginator,
        ListDevicesPaginator,
        ListInstanceProfilesPaginator,
        ListJobsPaginator,
        ListNetworkProfilesPaginator,
        ListOfferingPromotionsPaginator,
        ListOfferingTransactionsPaginator,
        ListOfferingsPaginator,
        ListProjectsPaginator,
        ListRemoteAccessSessionsPaginator,
        ListRunsPaginator,
        ListSamplesPaginator,
        ListSuitesPaginator,
        ListTestsPaginator,
        ListUniqueProblemsPaginator,
        ListUploadsPaginator,
        ListVPCEConfigurationsPaginator,
    )

    session = get_session()
    with session.create_client("devicefarm") as client:
        client: DeviceFarmClient

        get_offering_status_paginator: GetOfferingStatusPaginator = client.get_paginator("get_offering_status")
        list_artifacts_paginator: ListArtifactsPaginator = client.get_paginator("list_artifacts")
        list_device_instances_paginator: ListDeviceInstancesPaginator = client.get_paginator("list_device_instances")
        list_device_pools_paginator: ListDevicePoolsPaginator = client.get_paginator("list_device_pools")
        list_devices_paginator: ListDevicesPaginator = client.get_paginator("list_devices")
        list_instance_profiles_paginator: ListInstanceProfilesPaginator = client.get_paginator("list_instance_profiles")
        list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
        list_network_profiles_paginator: ListNetworkProfilesPaginator = client.get_paginator("list_network_profiles")
        list_offering_promotions_paginator: ListOfferingPromotionsPaginator = client.get_paginator("list_offering_promotions")
        list_offering_transactions_paginator: ListOfferingTransactionsPaginator = client.get_paginator("list_offering_transactions")
        list_offerings_paginator: ListOfferingsPaginator = client.get_paginator("list_offerings")
        list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
        list_remote_access_sessions_paginator: ListRemoteAccessSessionsPaginator = client.get_paginator("list_remote_access_sessions")
        list_runs_paginator: ListRunsPaginator = client.get_paginator("list_runs")
        list_samples_paginator: ListSamplesPaginator = client.get_paginator("list_samples")
        list_suites_paginator: ListSuitesPaginator = client.get_paginator("list_suites")
        list_tests_paginator: ListTestsPaginator = client.get_paginator("list_tests")
        list_unique_problems_paginator: ListUniqueProblemsPaginator = client.get_paginator("list_unique_problems")
        list_uploads_paginator: ListUploadsPaginator = client.get_paginator("list_uploads")
        list_vpce_configurations_paginator: ListVPCEConfigurationsPaginator = client.get_paginator("list_vpce_configurations")
    ```
"""
import sys
from typing import Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import (
    ArtifactCategoryType,
    DevicePoolTypeType,
    NetworkProfileTypeType,
    UploadTypeType,
)
from .type_defs import (
    DeviceFilterTypeDef,
    GetOfferingStatusResultTypeDef,
    ListArtifactsResultTypeDef,
    ListDeviceInstancesResultTypeDef,
    ListDevicePoolsResultTypeDef,
    ListDevicesResultTypeDef,
    ListInstanceProfilesResultTypeDef,
    ListJobsResultTypeDef,
    ListNetworkProfilesResultTypeDef,
    ListOfferingPromotionsResultTypeDef,
    ListOfferingsResultTypeDef,
    ListOfferingTransactionsResultTypeDef,
    ListProjectsResultTypeDef,
    ListRemoteAccessSessionsResultTypeDef,
    ListRunsResultTypeDef,
    ListSamplesResultTypeDef,
    ListSuitesResultTypeDef,
    ListTestsResultTypeDef,
    ListUniqueProblemsResultTypeDef,
    ListUploadsResultTypeDef,
    ListVPCEConfigurationsResultTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator

__all__ = (
    "GetOfferingStatusPaginator",
    "ListArtifactsPaginator",
    "ListDeviceInstancesPaginator",
    "ListDevicePoolsPaginator",
    "ListDevicesPaginator",
    "ListInstanceProfilesPaginator",
    "ListJobsPaginator",
    "ListNetworkProfilesPaginator",
    "ListOfferingPromotionsPaginator",
    "ListOfferingTransactionsPaginator",
    "ListOfferingsPaginator",
    "ListProjectsPaginator",
    "ListRemoteAccessSessionsPaginator",
    "ListRunsPaginator",
    "ListSamplesPaginator",
    "ListSuitesPaginator",
    "ListTestsPaginator",
    "ListUniqueProblemsPaginator",
    "ListUploadsPaginator",
    "ListVPCEConfigurationsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetOfferingStatusPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.GetOfferingStatus)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#getofferingstatuspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[GetOfferingStatusResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.GetOfferingStatus.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#getofferingstatuspaginator)
        """

class ListArtifactsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListArtifacts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listartifactspaginator)
    """

    def paginate(
        self,
        *,
        arn: str,
        type: ArtifactCategoryType,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListArtifactsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListArtifacts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listartifactspaginator)
        """

class ListDeviceInstancesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListDeviceInstances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listdeviceinstancespaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListDeviceInstancesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListDeviceInstances.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listdeviceinstancespaginator)
        """

class ListDevicePoolsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListDevicePools)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listdevicepoolspaginator)
    """

    def paginate(
        self,
        *,
        arn: str,
        type: DevicePoolTypeType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListDevicePoolsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListDevicePools.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listdevicepoolspaginator)
        """

class ListDevicesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListDevices)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listdevicespaginator)
    """

    def paginate(
        self,
        *,
        arn: str = ...,
        filters: Sequence["DeviceFilterTypeDef"] = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListDevicesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListDevices.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listdevicespaginator)
        """

class ListInstanceProfilesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListInstanceProfiles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listinstanceprofilespaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListInstanceProfilesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListInstanceProfiles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listinstanceprofilespaginator)
        """

class ListJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listjobspaginator)
    """

    def paginate(
        self, *, arn: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListJobsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listjobspaginator)
        """

class ListNetworkProfilesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListNetworkProfiles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listnetworkprofilespaginator)
    """

    def paginate(
        self,
        *,
        arn: str,
        type: NetworkProfileTypeType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListNetworkProfilesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListNetworkProfiles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listnetworkprofilespaginator)
        """

class ListOfferingPromotionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListOfferingPromotions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listofferingpromotionspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListOfferingPromotionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListOfferingPromotions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listofferingpromotionspaginator)
        """

class ListOfferingTransactionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListOfferingTransactions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listofferingtransactionspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListOfferingTransactionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListOfferingTransactions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listofferingtransactionspaginator)
        """

class ListOfferingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListOfferings)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listofferingspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListOfferingsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListOfferings.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listofferingspaginator)
        """

class ListProjectsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListProjects)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listprojectspaginator)
    """

    def paginate(
        self, *, arn: str = ..., PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListProjectsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListProjects.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listprojectspaginator)
        """

class ListRemoteAccessSessionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListRemoteAccessSessions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listremoteaccesssessionspaginator)
    """

    def paginate(
        self, *, arn: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListRemoteAccessSessionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListRemoteAccessSessions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listremoteaccesssessionspaginator)
        """

class ListRunsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListRuns)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listrunspaginator)
    """

    def paginate(
        self, *, arn: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListRunsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListRuns.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listrunspaginator)
        """

class ListSamplesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListSamples)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listsamplespaginator)
    """

    def paginate(
        self, *, arn: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListSamplesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListSamples.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listsamplespaginator)
        """

class ListSuitesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListSuites)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listsuitespaginator)
    """

    def paginate(
        self, *, arn: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListSuitesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListSuites.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listsuitespaginator)
        """

class ListTestsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListTests)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listtestspaginator)
    """

    def paginate(
        self, *, arn: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListTestsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListTests.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listtestspaginator)
        """

class ListUniqueProblemsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListUniqueProblems)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listuniqueproblemspaginator)
    """

    def paginate(
        self, *, arn: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListUniqueProblemsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListUniqueProblems.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listuniqueproblemspaginator)
        """

class ListUploadsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListUploads)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listuploadspaginator)
    """

    def paginate(
        self,
        *,
        arn: str,
        type: UploadTypeType = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListUploadsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListUploads.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listuploadspaginator)
        """

class ListVPCEConfigurationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListVPCEConfigurations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listvpceconfigurationspaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ListVPCEConfigurationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Paginator.ListVPCEConfigurations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listvpceconfigurationspaginator)
        """
