"""
Type annotations for devicefarm service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_devicefarm.client import DeviceFarmClient

    session = get_session()
    async with session.create_client("devicefarm") as client:
        client: DeviceFarmClient
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    ArtifactCategoryType,
    DevicePoolTypeType,
    InteractionModeType,
    NetworkProfileTypeType,
    TestGridSessionArtifactCategoryType,
    TestGridSessionStatusType,
    TestTypeType,
    UploadTypeType,
)
from .paginator import (
    GetOfferingStatusPaginator,
    ListArtifactsPaginator,
    ListDeviceInstancesPaginator,
    ListDevicePoolsPaginator,
    ListDevicesPaginator,
    ListInstanceProfilesPaginator,
    ListJobsPaginator,
    ListNetworkProfilesPaginator,
    ListOfferingPromotionsPaginator,
    ListOfferingsPaginator,
    ListOfferingTransactionsPaginator,
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
from .type_defs import (
    CreateDevicePoolResultTypeDef,
    CreateInstanceProfileResultTypeDef,
    CreateNetworkProfileResultTypeDef,
    CreateProjectResultTypeDef,
    CreateRemoteAccessSessionConfigurationTypeDef,
    CreateRemoteAccessSessionResultTypeDef,
    CreateTestGridProjectResultTypeDef,
    CreateTestGridUrlResultTypeDef,
    CreateUploadResultTypeDef,
    CreateVPCEConfigurationResultTypeDef,
    DeviceFilterTypeDef,
    DeviceSelectionConfigurationTypeDef,
    ExecutionConfigurationTypeDef,
    GetAccountSettingsResultTypeDef,
    GetDeviceInstanceResultTypeDef,
    GetDevicePoolCompatibilityResultTypeDef,
    GetDevicePoolResultTypeDef,
    GetDeviceResultTypeDef,
    GetInstanceProfileResultTypeDef,
    GetJobResultTypeDef,
    GetNetworkProfileResultTypeDef,
    GetOfferingStatusResultTypeDef,
    GetProjectResultTypeDef,
    GetRemoteAccessSessionResultTypeDef,
    GetRunResultTypeDef,
    GetSuiteResultTypeDef,
    GetTestGridProjectResultTypeDef,
    GetTestGridSessionResultTypeDef,
    GetTestResultTypeDef,
    GetUploadResultTypeDef,
    GetVPCEConfigurationResultTypeDef,
    InstallToRemoteAccessSessionResultTypeDef,
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
    ListTagsForResourceResponseTypeDef,
    ListTestGridProjectsResultTypeDef,
    ListTestGridSessionActionsResultTypeDef,
    ListTestGridSessionArtifactsResultTypeDef,
    ListTestGridSessionsResultTypeDef,
    ListTestsResultTypeDef,
    ListUniqueProblemsResultTypeDef,
    ListUploadsResultTypeDef,
    ListVPCEConfigurationsResultTypeDef,
    PurchaseOfferingResultTypeDef,
    RenewOfferingResultTypeDef,
    RuleTypeDef,
    ScheduleRunConfigurationTypeDef,
    ScheduleRunResultTypeDef,
    ScheduleRunTestTypeDef,
    StopJobResultTypeDef,
    StopRemoteAccessSessionResultTypeDef,
    StopRunResultTypeDef,
    TagTypeDef,
    TestGridVpcConfigTypeDef,
    UpdateDeviceInstanceResultTypeDef,
    UpdateDevicePoolResultTypeDef,
    UpdateInstanceProfileResultTypeDef,
    UpdateNetworkProfileResultTypeDef,
    UpdateProjectResultTypeDef,
    UpdateTestGridProjectResultTypeDef,
    UpdateUploadResultTypeDef,
    UpdateVPCEConfigurationResultTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("DeviceFarmClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ArgumentException: Type[BotocoreClientError]
    CannotDeleteException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    IdempotencyException: Type[BotocoreClientError]
    InternalServiceException: Type[BotocoreClientError]
    InvalidOperationException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NotEligibleException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ServiceAccountException: Type[BotocoreClientError]
    TagOperationException: Type[BotocoreClientError]
    TagPolicyException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]

class DeviceFarmClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DeviceFarmClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#exceptions)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#can_paginate)
        """
    async def create_device_pool(
        self,
        *,
        projectArn: str,
        name: str,
        rules: Sequence["RuleTypeDef"],
        description: str = ...,
        maxDevices: int = ...
    ) -> CreateDevicePoolResultTypeDef:
        """
        Creates a device pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.create_device_pool)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#create_device_pool)
        """
    async def create_instance_profile(
        self,
        *,
        name: str,
        description: str = ...,
        packageCleanup: bool = ...,
        excludeAppPackagesFromCleanup: Sequence[str] = ...,
        rebootAfterUse: bool = ...
    ) -> CreateInstanceProfileResultTypeDef:
        """
        Creates a profile that can be applied to one or more private fleet device
        instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.create_instance_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#create_instance_profile)
        """
    async def create_network_profile(
        self,
        *,
        projectArn: str,
        name: str,
        description: str = ...,
        type: NetworkProfileTypeType = ...,
        uplinkBandwidthBits: int = ...,
        downlinkBandwidthBits: int = ...,
        uplinkDelayMs: int = ...,
        downlinkDelayMs: int = ...,
        uplinkJitterMs: int = ...,
        downlinkJitterMs: int = ...,
        uplinkLossPercent: int = ...,
        downlinkLossPercent: int = ...
    ) -> CreateNetworkProfileResultTypeDef:
        """
        Creates a network profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.create_network_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#create_network_profile)
        """
    async def create_project(
        self, *, name: str, defaultJobTimeoutMinutes: int = ...
    ) -> CreateProjectResultTypeDef:
        """
        Creates a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.create_project)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#create_project)
        """
    async def create_remote_access_session(
        self,
        *,
        projectArn: str,
        deviceArn: str,
        instanceArn: str = ...,
        sshPublicKey: str = ...,
        remoteDebugEnabled: bool = ...,
        remoteRecordEnabled: bool = ...,
        remoteRecordAppArn: str = ...,
        name: str = ...,
        clientId: str = ...,
        configuration: "CreateRemoteAccessSessionConfigurationTypeDef" = ...,
        interactionMode: InteractionModeType = ...,
        skipAppResign: bool = ...
    ) -> CreateRemoteAccessSessionResultTypeDef:
        """
        Specifies and starts a remote access session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.create_remote_access_session)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#create_remote_access_session)
        """
    async def create_test_grid_project(
        self, *, name: str, description: str = ..., vpcConfig: "TestGridVpcConfigTypeDef" = ...
    ) -> CreateTestGridProjectResultTypeDef:
        """
        Creates a Selenium testing project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.create_test_grid_project)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#create_test_grid_project)
        """
    async def create_test_grid_url(
        self, *, projectArn: str, expiresInSeconds: int
    ) -> CreateTestGridUrlResultTypeDef:
        """
        Creates a signed, short-term URL that can be passed to a Selenium
        `RemoteWebDriver` constructor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.create_test_grid_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#create_test_grid_url)
        """
    async def create_upload(
        self, *, projectArn: str, name: str, type: UploadTypeType, contentType: str = ...
    ) -> CreateUploadResultTypeDef:
        """
        Uploads an app or test scripts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.create_upload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#create_upload)
        """
    async def create_vpce_configuration(
        self,
        *,
        vpceConfigurationName: str,
        vpceServiceName: str,
        serviceDnsName: str,
        vpceConfigurationDescription: str = ...
    ) -> CreateVPCEConfigurationResultTypeDef:
        """
        Creates a configuration record in Device Farm for your Amazon Virtual Private
        Cloud (VPC) endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.create_vpce_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#create_vpce_configuration)
        """
    async def delete_device_pool(self, *, arn: str) -> Dict[str, Any]:
        """
        Deletes a device pool given the pool ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.delete_device_pool)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#delete_device_pool)
        """
    async def delete_instance_profile(self, *, arn: str) -> Dict[str, Any]:
        """
        Deletes a profile that can be applied to one or more private device instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.delete_instance_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#delete_instance_profile)
        """
    async def delete_network_profile(self, *, arn: str) -> Dict[str, Any]:
        """
        Deletes a network profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.delete_network_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#delete_network_profile)
        """
    async def delete_project(self, *, arn: str) -> Dict[str, Any]:
        """
        Deletes an AWS Device Farm project, given the project ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.delete_project)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#delete_project)
        """
    async def delete_remote_access_session(self, *, arn: str) -> Dict[str, Any]:
        """
        Deletes a completed remote access session and its results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.delete_remote_access_session)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#delete_remote_access_session)
        """
    async def delete_run(self, *, arn: str) -> Dict[str, Any]:
        """
        Deletes the run, given the run ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.delete_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#delete_run)
        """
    async def delete_test_grid_project(self, *, projectArn: str) -> Dict[str, Any]:
        """
        Deletes a Selenium testing project and all content generated under it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.delete_test_grid_project)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#delete_test_grid_project)
        """
    async def delete_upload(self, *, arn: str) -> Dict[str, Any]:
        """
        Deletes an upload given the upload ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.delete_upload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#delete_upload)
        """
    async def delete_vpce_configuration(self, *, arn: str) -> Dict[str, Any]:
        """
        Deletes a configuration for your Amazon Virtual Private Cloud (VPC) endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.delete_vpce_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#delete_vpce_configuration)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#generate_presigned_url)
        """
    async def get_account_settings(self) -> GetAccountSettingsResultTypeDef:
        """
        Returns the number of unmetered iOS or unmetered Android devices that have been
        purchased by the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_account_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_account_settings)
        """
    async def get_device(self, *, arn: str) -> GetDeviceResultTypeDef:
        """
        Gets information about a unique device type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_device)
        """
    async def get_device_instance(self, *, arn: str) -> GetDeviceInstanceResultTypeDef:
        """
        Returns information about a device instance that belongs to a private device
        fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_device_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_device_instance)
        """
    async def get_device_pool(self, *, arn: str) -> GetDevicePoolResultTypeDef:
        """
        Gets information about a device pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_device_pool)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_device_pool)
        """
    async def get_device_pool_compatibility(
        self,
        *,
        devicePoolArn: str,
        appArn: str = ...,
        testType: TestTypeType = ...,
        test: "ScheduleRunTestTypeDef" = ...,
        configuration: "ScheduleRunConfigurationTypeDef" = ...
    ) -> GetDevicePoolCompatibilityResultTypeDef:
        """
        Gets information about compatibility with a device pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_device_pool_compatibility)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_device_pool_compatibility)
        """
    async def get_instance_profile(self, *, arn: str) -> GetInstanceProfileResultTypeDef:
        """
        Returns information about the specified instance profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_instance_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_instance_profile)
        """
    async def get_job(self, *, arn: str) -> GetJobResultTypeDef:
        """
        Gets information about a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_job)
        """
    async def get_network_profile(self, *, arn: str) -> GetNetworkProfileResultTypeDef:
        """
        Returns information about a network profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_network_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_network_profile)
        """
    async def get_offering_status(self, *, nextToken: str = ...) -> GetOfferingStatusResultTypeDef:
        """
        Gets the current status and future status of all offerings purchased by an AWS
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_offering_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_offering_status)
        """
    async def get_project(self, *, arn: str) -> GetProjectResultTypeDef:
        """
        Gets information about a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_project)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_project)
        """
    async def get_remote_access_session(self, *, arn: str) -> GetRemoteAccessSessionResultTypeDef:
        """
        Returns a link to a currently running remote access session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_remote_access_session)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_remote_access_session)
        """
    async def get_run(self, *, arn: str) -> GetRunResultTypeDef:
        """
        Gets information about a run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_run)
        """
    async def get_suite(self, *, arn: str) -> GetSuiteResultTypeDef:
        """
        Gets information about a suite.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_suite)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_suite)
        """
    async def get_test(self, *, arn: str) -> GetTestResultTypeDef:
        """
        Gets information about a test.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_test)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_test)
        """
    async def get_test_grid_project(self, *, projectArn: str) -> GetTestGridProjectResultTypeDef:
        """
        Retrieves information about a Selenium testing project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_test_grid_project)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_test_grid_project)
        """
    async def get_test_grid_session(
        self, *, projectArn: str = ..., sessionId: str = ..., sessionArn: str = ...
    ) -> GetTestGridSessionResultTypeDef:
        """
        A session is an instance of a browser created through a `RemoteWebDriver` with
        the URL from  CreateTestGridUrlResult$url.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_test_grid_session)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_test_grid_session)
        """
    async def get_upload(self, *, arn: str) -> GetUploadResultTypeDef:
        """
        Gets information about an upload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_upload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_upload)
        """
    async def get_vpce_configuration(self, *, arn: str) -> GetVPCEConfigurationResultTypeDef:
        """
        Returns information about the configuration settings for your Amazon Virtual
        Private Cloud (VPC) endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_vpce_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_vpce_configuration)
        """
    async def install_to_remote_access_session(
        self, *, remoteAccessSessionArn: str, appArn: str
    ) -> InstallToRemoteAccessSessionResultTypeDef:
        """
        Installs an application to the device in a remote access session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.install_to_remote_access_session)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#install_to_remote_access_session)
        """
    async def list_artifacts(
        self, *, arn: str, type: ArtifactCategoryType, nextToken: str = ...
    ) -> ListArtifactsResultTypeDef:
        """
        Gets information about artifacts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.list_artifacts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_artifacts)
        """
    async def list_device_instances(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListDeviceInstancesResultTypeDef:
        """
        Returns information about the private device instances associated with one or
        more AWS accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.list_device_instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_device_instances)
        """
    async def list_device_pools(
        self, *, arn: str, type: DevicePoolTypeType = ..., nextToken: str = ...
    ) -> ListDevicePoolsResultTypeDef:
        """
        Gets information about device pools.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.list_device_pools)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_device_pools)
        """
    async def list_devices(
        self,
        *,
        arn: str = ...,
        nextToken: str = ...,
        filters: Sequence["DeviceFilterTypeDef"] = ...
    ) -> ListDevicesResultTypeDef:
        """
        Gets information about unique device types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.list_devices)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_devices)
        """
    async def list_instance_profiles(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListInstanceProfilesResultTypeDef:
        """
        Returns information about all the instance profiles in an AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.list_instance_profiles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_instance_profiles)
        """
    async def list_jobs(self, *, arn: str, nextToken: str = ...) -> ListJobsResultTypeDef:
        """
        Gets information about jobs for a given test run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.list_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_jobs)
        """
    async def list_network_profiles(
        self, *, arn: str, type: NetworkProfileTypeType = ..., nextToken: str = ...
    ) -> ListNetworkProfilesResultTypeDef:
        """
        Returns the list of available network profiles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.list_network_profiles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_network_profiles)
        """
    async def list_offering_promotions(
        self, *, nextToken: str = ...
    ) -> ListOfferingPromotionsResultTypeDef:
        """
        Returns a list of offering promotions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.list_offering_promotions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_offering_promotions)
        """
    async def list_offering_transactions(
        self, *, nextToken: str = ...
    ) -> ListOfferingTransactionsResultTypeDef:
        """
        Returns a list of all historical purchases, renewals, and system renewal
        transactions for an AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.list_offering_transactions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_offering_transactions)
        """
    async def list_offerings(self, *, nextToken: str = ...) -> ListOfferingsResultTypeDef:
        """
        Returns a list of products or offerings that the user can manage through the
        API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.list_offerings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_offerings)
        """
    async def list_projects(
        self, *, arn: str = ..., nextToken: str = ...
    ) -> ListProjectsResultTypeDef:
        """
        Gets information about projects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.list_projects)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_projects)
        """
    async def list_remote_access_sessions(
        self, *, arn: str, nextToken: str = ...
    ) -> ListRemoteAccessSessionsResultTypeDef:
        """
        Returns a list of all currently running remote access sessions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.list_remote_access_sessions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_remote_access_sessions)
        """
    async def list_runs(self, *, arn: str, nextToken: str = ...) -> ListRunsResultTypeDef:
        """
        Gets information about runs, given an AWS Device Farm project ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.list_runs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_runs)
        """
    async def list_samples(self, *, arn: str, nextToken: str = ...) -> ListSamplesResultTypeDef:
        """
        Gets information about samples, given an AWS Device Farm job ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.list_samples)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_samples)
        """
    async def list_suites(self, *, arn: str, nextToken: str = ...) -> ListSuitesResultTypeDef:
        """
        Gets information about test suites for a given job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.list_suites)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_suites)
        """
    async def list_tags_for_resource(
        self, *, ResourceARN: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List the tags for an AWS Device Farm resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_tags_for_resource)
        """
    async def list_test_grid_projects(
        self, *, maxResult: int = ..., nextToken: str = ...
    ) -> ListTestGridProjectsResultTypeDef:
        """
        Gets a list of all Selenium testing projects in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.list_test_grid_projects)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_test_grid_projects)
        """
    async def list_test_grid_session_actions(
        self, *, sessionArn: str, maxResult: int = ..., nextToken: str = ...
    ) -> ListTestGridSessionActionsResultTypeDef:
        """
        Returns a list of the actions taken in a  TestGridSession .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.list_test_grid_session_actions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_test_grid_session_actions)
        """
    async def list_test_grid_session_artifacts(
        self,
        *,
        sessionArn: str,
        type: TestGridSessionArtifactCategoryType = ...,
        maxResult: int = ...,
        nextToken: str = ...
    ) -> ListTestGridSessionArtifactsResultTypeDef:
        """
        Retrieves a list of artifacts created during the session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.list_test_grid_session_artifacts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_test_grid_session_artifacts)
        """
    async def list_test_grid_sessions(
        self,
        *,
        projectArn: str,
        status: TestGridSessionStatusType = ...,
        creationTimeAfter: Union[datetime, str] = ...,
        creationTimeBefore: Union[datetime, str] = ...,
        endTimeAfter: Union[datetime, str] = ...,
        endTimeBefore: Union[datetime, str] = ...,
        maxResult: int = ...,
        nextToken: str = ...
    ) -> ListTestGridSessionsResultTypeDef:
        """
        Retrieves a list of sessions for a  TestGridProject .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.list_test_grid_sessions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_test_grid_sessions)
        """
    async def list_tests(self, *, arn: str, nextToken: str = ...) -> ListTestsResultTypeDef:
        """
        Gets information about tests in a given test suite.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.list_tests)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_tests)
        """
    async def list_unique_problems(
        self, *, arn: str, nextToken: str = ...
    ) -> ListUniqueProblemsResultTypeDef:
        """
        Gets information about unique problems, such as exceptions or crashes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.list_unique_problems)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_unique_problems)
        """
    async def list_uploads(
        self, *, arn: str, type: UploadTypeType = ..., nextToken: str = ...
    ) -> ListUploadsResultTypeDef:
        """
        Gets information about uploads, given an AWS Device Farm project ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.list_uploads)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_uploads)
        """
    async def list_vpce_configurations(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListVPCEConfigurationsResultTypeDef:
        """
        Returns information about all Amazon Virtual Private Cloud (VPC) endpoint
        configurations in the AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.list_vpce_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#list_vpce_configurations)
        """
    async def purchase_offering(
        self, *, offeringId: str, quantity: int, offeringPromotionId: str = ...
    ) -> PurchaseOfferingResultTypeDef:
        """
        Immediately purchases offerings for an AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.purchase_offering)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#purchase_offering)
        """
    async def renew_offering(self, *, offeringId: str, quantity: int) -> RenewOfferingResultTypeDef:
        """
        Explicitly sets the quantity of devices to renew for an offering, starting from
        the `effectiveDate` of the next period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.renew_offering)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#renew_offering)
        """
    async def schedule_run(
        self,
        *,
        projectArn: str,
        test: "ScheduleRunTestTypeDef",
        appArn: str = ...,
        devicePoolArn: str = ...,
        deviceSelectionConfiguration: "DeviceSelectionConfigurationTypeDef" = ...,
        name: str = ...,
        configuration: "ScheduleRunConfigurationTypeDef" = ...,
        executionConfiguration: "ExecutionConfigurationTypeDef" = ...
    ) -> ScheduleRunResultTypeDef:
        """
        Schedules a run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.schedule_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#schedule_run)
        """
    async def stop_job(self, *, arn: str) -> StopJobResultTypeDef:
        """
        Initiates a stop request for the current job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.stop_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#stop_job)
        """
    async def stop_remote_access_session(self, *, arn: str) -> StopRemoteAccessSessionResultTypeDef:
        """
        Ends a specified remote access session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.stop_remote_access_session)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#stop_remote_access_session)
        """
    async def stop_run(self, *, arn: str) -> StopRunResultTypeDef:
        """
        Initiates a stop request for the current test run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.stop_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#stop_run)
        """
    async def tag_resource(
        self, *, ResourceARN: str, Tags: Sequence["TagTypeDef"]
    ) -> Dict[str, Any]:
        """
        Associates the specified tags to a resource with the specified `resourceArn`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#tag_resource)
        """
    async def untag_resource(self, *, ResourceARN: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Deletes the specified tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#untag_resource)
        """
    async def update_device_instance(
        self, *, arn: str, profileArn: str = ..., labels: Sequence[str] = ...
    ) -> UpdateDeviceInstanceResultTypeDef:
        """
        Updates information about a private device instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.update_device_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#update_device_instance)
        """
    async def update_device_pool(
        self,
        *,
        arn: str,
        name: str = ...,
        description: str = ...,
        rules: Sequence["RuleTypeDef"] = ...,
        maxDevices: int = ...,
        clearMaxDevices: bool = ...
    ) -> UpdateDevicePoolResultTypeDef:
        """
        Modifies the name, description, and rules in a device pool given the attributes
        and the pool ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.update_device_pool)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#update_device_pool)
        """
    async def update_instance_profile(
        self,
        *,
        arn: str,
        name: str = ...,
        description: str = ...,
        packageCleanup: bool = ...,
        excludeAppPackagesFromCleanup: Sequence[str] = ...,
        rebootAfterUse: bool = ...
    ) -> UpdateInstanceProfileResultTypeDef:
        """
        Updates information about an existing private device instance profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.update_instance_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#update_instance_profile)
        """
    async def update_network_profile(
        self,
        *,
        arn: str,
        name: str = ...,
        description: str = ...,
        type: NetworkProfileTypeType = ...,
        uplinkBandwidthBits: int = ...,
        downlinkBandwidthBits: int = ...,
        uplinkDelayMs: int = ...,
        downlinkDelayMs: int = ...,
        uplinkJitterMs: int = ...,
        downlinkJitterMs: int = ...,
        uplinkLossPercent: int = ...,
        downlinkLossPercent: int = ...
    ) -> UpdateNetworkProfileResultTypeDef:
        """
        Updates the network profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.update_network_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#update_network_profile)
        """
    async def update_project(
        self, *, arn: str, name: str = ..., defaultJobTimeoutMinutes: int = ...
    ) -> UpdateProjectResultTypeDef:
        """
        Modifies the specified project name, given the project ARN and a new name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.update_project)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#update_project)
        """
    async def update_test_grid_project(
        self,
        *,
        projectArn: str,
        name: str = ...,
        description: str = ...,
        vpcConfig: "TestGridVpcConfigTypeDef" = ...
    ) -> UpdateTestGridProjectResultTypeDef:
        """
        Change details of a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.update_test_grid_project)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#update_test_grid_project)
        """
    async def update_upload(
        self, *, arn: str, name: str = ..., contentType: str = ..., editContent: bool = ...
    ) -> UpdateUploadResultTypeDef:
        """
        Updates an uploaded test spec.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.update_upload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#update_upload)
        """
    async def update_vpce_configuration(
        self,
        *,
        arn: str,
        vpceConfigurationName: str = ...,
        vpceServiceName: str = ...,
        serviceDnsName: str = ...,
        vpceConfigurationDescription: str = ...
    ) -> UpdateVPCEConfigurationResultTypeDef:
        """
        Updates information about an Amazon Virtual Private Cloud (VPC) endpoint
        configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.update_vpce_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#update_vpce_configuration)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["get_offering_status"]
    ) -> GetOfferingStatusPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_artifacts"]) -> ListArtifactsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_device_instances"]
    ) -> ListDeviceInstancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_device_pools"]
    ) -> ListDevicePoolsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_devices"]) -> ListDevicesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_instance_profiles"]
    ) -> ListInstanceProfilesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_jobs"]) -> ListJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_network_profiles"]
    ) -> ListNetworkProfilesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_offering_promotions"]
    ) -> ListOfferingPromotionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_offering_transactions"]
    ) -> ListOfferingTransactionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_offerings"]) -> ListOfferingsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_projects"]) -> ListProjectsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_remote_access_sessions"]
    ) -> ListRemoteAccessSessionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_runs"]) -> ListRunsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_samples"]) -> ListSamplesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_suites"]) -> ListSuitesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_tests"]) -> ListTestsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_unique_problems"]
    ) -> ListUniqueProblemsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_uploads"]) -> ListUploadsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_vpce_configurations"]
    ) -> ListVPCEConfigurationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/#get_paginator)
        """
    async def __aenter__(self) -> "DeviceFarmClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm.html#DeviceFarm.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/client/)
        """
