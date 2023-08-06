"""
Type annotations for ecs service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ecs.client import ECSClient

    session = get_session()
    async with session.create_client("ecs") as client:
        client: ECSClient
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    ClusterFieldType,
    CompatibilityType,
    ContainerInstanceFieldType,
    ContainerInstanceStatusType,
    DesiredStatusType,
    IpcModeType,
    LaunchTypeType,
    NetworkModeType,
    PidModeType,
    PropagateTagsType,
    SchedulingStrategyType,
    SettingNameType,
    SortOrderType,
    TaskDefinitionFamilyStatusType,
    TaskDefinitionStatusType,
)
from .paginator import (
    ListAccountSettingsPaginator,
    ListAttributesPaginator,
    ListClustersPaginator,
    ListContainerInstancesPaginator,
    ListServicesPaginator,
    ListTaskDefinitionFamiliesPaginator,
    ListTaskDefinitionsPaginator,
    ListTasksPaginator,
)
from .type_defs import (
    AttachmentStateChangeTypeDef,
    AttributeTypeDef,
    AutoScalingGroupProviderTypeDef,
    AutoScalingGroupProviderUpdateTypeDef,
    CapacityProviderStrategyItemTypeDef,
    ClusterConfigurationTypeDef,
    ClusterSettingTypeDef,
    ContainerDefinitionTypeDef,
    ContainerStateChangeTypeDef,
    CreateCapacityProviderResponseTypeDef,
    CreateClusterResponseTypeDef,
    CreateServiceResponseTypeDef,
    CreateTaskSetResponseTypeDef,
    DeleteAccountSettingResponseTypeDef,
    DeleteAttributesResponseTypeDef,
    DeleteCapacityProviderResponseTypeDef,
    DeleteClusterResponseTypeDef,
    DeleteServiceResponseTypeDef,
    DeleteTaskSetResponseTypeDef,
    DeploymentConfigurationTypeDef,
    DeploymentControllerTypeDef,
    DeregisterContainerInstanceResponseTypeDef,
    DeregisterTaskDefinitionResponseTypeDef,
    DescribeCapacityProvidersResponseTypeDef,
    DescribeClustersResponseTypeDef,
    DescribeContainerInstancesResponseTypeDef,
    DescribeServicesResponseTypeDef,
    DescribeTaskDefinitionResponseTypeDef,
    DescribeTaskSetsResponseTypeDef,
    DescribeTasksResponseTypeDef,
    DiscoverPollEndpointResponseTypeDef,
    EphemeralStorageTypeDef,
    ExecuteCommandResponseTypeDef,
    InferenceAcceleratorTypeDef,
    ListAccountSettingsResponseTypeDef,
    ListAttributesResponseTypeDef,
    ListClustersResponseTypeDef,
    ListContainerInstancesResponseTypeDef,
    ListServicesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTaskDefinitionFamiliesResponseTypeDef,
    ListTaskDefinitionsResponseTypeDef,
    ListTasksResponseTypeDef,
    LoadBalancerTypeDef,
    ManagedAgentStateChangeTypeDef,
    NetworkBindingTypeDef,
    NetworkConfigurationTypeDef,
    PlacementConstraintTypeDef,
    PlacementStrategyTypeDef,
    PlatformDeviceTypeDef,
    ProxyConfigurationTypeDef,
    PutAccountSettingDefaultResponseTypeDef,
    PutAccountSettingResponseTypeDef,
    PutAttributesResponseTypeDef,
    PutClusterCapacityProvidersResponseTypeDef,
    RegisterContainerInstanceResponseTypeDef,
    RegisterTaskDefinitionResponseTypeDef,
    ResourceTypeDef,
    RunTaskResponseTypeDef,
    RuntimePlatformTypeDef,
    ScaleTypeDef,
    ServiceRegistryTypeDef,
    StartTaskResponseTypeDef,
    StopTaskResponseTypeDef,
    SubmitAttachmentStateChangesResponseTypeDef,
    SubmitContainerStateChangeResponseTypeDef,
    SubmitTaskStateChangeResponseTypeDef,
    TagTypeDef,
    TaskDefinitionPlacementConstraintTypeDef,
    TaskOverrideTypeDef,
    UpdateCapacityProviderResponseTypeDef,
    UpdateClusterResponseTypeDef,
    UpdateClusterSettingsResponseTypeDef,
    UpdateContainerAgentResponseTypeDef,
    UpdateContainerInstancesStateResponseTypeDef,
    UpdateServicePrimaryTaskSetResponseTypeDef,
    UpdateServiceResponseTypeDef,
    UpdateTaskSetResponseTypeDef,
    VersionInfoTypeDef,
    VolumeTypeDef,
)
from .waiter import (
    ServicesInactiveWaiter,
    ServicesStableWaiter,
    TasksRunningWaiter,
    TasksStoppedWaiter,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ECSClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    AttributeLimitExceededException: Type[BotocoreClientError]
    BlockedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ClientException: Type[BotocoreClientError]
    ClusterContainsContainerInstancesException: Type[BotocoreClientError]
    ClusterContainsServicesException: Type[BotocoreClientError]
    ClusterContainsTasksException: Type[BotocoreClientError]
    ClusterNotFoundException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MissingVersionException: Type[BotocoreClientError]
    NoUpdateAvailableException: Type[BotocoreClientError]
    PlatformTaskDefinitionIncompatibilityException: Type[BotocoreClientError]
    PlatformUnknownException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServerException: Type[BotocoreClientError]
    ServiceNotActiveException: Type[BotocoreClientError]
    ServiceNotFoundException: Type[BotocoreClientError]
    TargetNotConnectedException: Type[BotocoreClientError]
    TargetNotFoundException: Type[BotocoreClientError]
    TaskSetNotFoundException: Type[BotocoreClientError]
    UnsupportedFeatureException: Type[BotocoreClientError]
    UpdateInProgressException: Type[BotocoreClientError]


class ECSClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ECSClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#can_paginate)
        """

    async def create_capacity_provider(
        self,
        *,
        name: str,
        autoScalingGroupProvider: "AutoScalingGroupProviderTypeDef",
        tags: Sequence["TagTypeDef"] = ...
    ) -> CreateCapacityProviderResponseTypeDef:
        """
        Creates a new capacity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.create_capacity_provider)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#create_capacity_provider)
        """

    async def create_cluster(
        self,
        *,
        clusterName: str = ...,
        tags: Sequence["TagTypeDef"] = ...,
        settings: Sequence["ClusterSettingTypeDef"] = ...,
        configuration: "ClusterConfigurationTypeDef" = ...,
        capacityProviders: Sequence[str] = ...,
        defaultCapacityProviderStrategy: Sequence["CapacityProviderStrategyItemTypeDef"] = ...
    ) -> CreateClusterResponseTypeDef:
        """
        Creates a new Amazon ECS cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.create_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#create_cluster)
        """

    async def create_service(
        self,
        *,
        serviceName: str,
        cluster: str = ...,
        taskDefinition: str = ...,
        loadBalancers: Sequence["LoadBalancerTypeDef"] = ...,
        serviceRegistries: Sequence["ServiceRegistryTypeDef"] = ...,
        desiredCount: int = ...,
        clientToken: str = ...,
        launchType: LaunchTypeType = ...,
        capacityProviderStrategy: Sequence["CapacityProviderStrategyItemTypeDef"] = ...,
        platformVersion: str = ...,
        role: str = ...,
        deploymentConfiguration: "DeploymentConfigurationTypeDef" = ...,
        placementConstraints: Sequence["PlacementConstraintTypeDef"] = ...,
        placementStrategy: Sequence["PlacementStrategyTypeDef"] = ...,
        networkConfiguration: "NetworkConfigurationTypeDef" = ...,
        healthCheckGracePeriodSeconds: int = ...,
        schedulingStrategy: SchedulingStrategyType = ...,
        deploymentController: "DeploymentControllerTypeDef" = ...,
        tags: Sequence["TagTypeDef"] = ...,
        enableECSManagedTags: bool = ...,
        propagateTags: PropagateTagsType = ...,
        enableExecuteCommand: bool = ...
    ) -> CreateServiceResponseTypeDef:
        """
        Runs and maintains your desired number of tasks from a specified task
        definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.create_service)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#create_service)
        """

    async def create_task_set(
        self,
        *,
        service: str,
        cluster: str,
        taskDefinition: str,
        externalId: str = ...,
        networkConfiguration: "NetworkConfigurationTypeDef" = ...,
        loadBalancers: Sequence["LoadBalancerTypeDef"] = ...,
        serviceRegistries: Sequence["ServiceRegistryTypeDef"] = ...,
        launchType: LaunchTypeType = ...,
        capacityProviderStrategy: Sequence["CapacityProviderStrategyItemTypeDef"] = ...,
        platformVersion: str = ...,
        scale: "ScaleTypeDef" = ...,
        clientToken: str = ...,
        tags: Sequence["TagTypeDef"] = ...
    ) -> CreateTaskSetResponseTypeDef:
        """
        Create a task set in the specified cluster and service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.create_task_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#create_task_set)
        """

    async def delete_account_setting(
        self, *, name: SettingNameType, principalArn: str = ...
    ) -> DeleteAccountSettingResponseTypeDef:
        """
        Disables an account setting for a specified IAM user, IAM role, or the root user
        for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.delete_account_setting)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#delete_account_setting)
        """

    async def delete_attributes(
        self, *, attributes: Sequence["AttributeTypeDef"], cluster: str = ...
    ) -> DeleteAttributesResponseTypeDef:
        """
        Deletes one or more custom attributes from an Amazon ECS resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.delete_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#delete_attributes)
        """

    async def delete_capacity_provider(
        self, *, capacityProvider: str
    ) -> DeleteCapacityProviderResponseTypeDef:
        """
        Deletes the specified capacity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.delete_capacity_provider)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#delete_capacity_provider)
        """

    async def delete_cluster(self, *, cluster: str) -> DeleteClusterResponseTypeDef:
        """
        Deletes the specified cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.delete_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#delete_cluster)
        """

    async def delete_service(
        self, *, service: str, cluster: str = ..., force: bool = ...
    ) -> DeleteServiceResponseTypeDef:
        """
        Deletes a specified service within a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.delete_service)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#delete_service)
        """

    async def delete_task_set(
        self, *, cluster: str, service: str, taskSet: str, force: bool = ...
    ) -> DeleteTaskSetResponseTypeDef:
        """
        Deletes a specified task set within a service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.delete_task_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#delete_task_set)
        """

    async def deregister_container_instance(
        self, *, containerInstance: str, cluster: str = ..., force: bool = ...
    ) -> DeregisterContainerInstanceResponseTypeDef:
        """
        Deregisters an Amazon ECS container instance from the specified cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.deregister_container_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#deregister_container_instance)
        """

    async def deregister_task_definition(
        self, *, taskDefinition: str
    ) -> DeregisterTaskDefinitionResponseTypeDef:
        """
        Deregisters the specified task definition by family and revision.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.deregister_task_definition)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#deregister_task_definition)
        """

    async def describe_capacity_providers(
        self,
        *,
        capacityProviders: Sequence[str] = ...,
        include: Sequence[Literal["TAGS"]] = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> DescribeCapacityProvidersResponseTypeDef:
        """
        Describes one or more of your capacity providers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.describe_capacity_providers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#describe_capacity_providers)
        """

    async def describe_clusters(
        self, *, clusters: Sequence[str] = ..., include: Sequence[ClusterFieldType] = ...
    ) -> DescribeClustersResponseTypeDef:
        """
        Describes one or more of your clusters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.describe_clusters)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#describe_clusters)
        """

    async def describe_container_instances(
        self,
        *,
        containerInstances: Sequence[str],
        cluster: str = ...,
        include: Sequence[ContainerInstanceFieldType] = ...
    ) -> DescribeContainerInstancesResponseTypeDef:
        """
        Describes one or more container instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.describe_container_instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#describe_container_instances)
        """

    async def describe_services(
        self,
        *,
        services: Sequence[str],
        cluster: str = ...,
        include: Sequence[Literal["TAGS"]] = ...
    ) -> DescribeServicesResponseTypeDef:
        """
        Describes the specified services running in your cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.describe_services)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#describe_services)
        """

    async def describe_task_definition(
        self, *, taskDefinition: str, include: Sequence[Literal["TAGS"]] = ...
    ) -> DescribeTaskDefinitionResponseTypeDef:
        """
        Describes a task definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.describe_task_definition)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#describe_task_definition)
        """

    async def describe_task_sets(
        self,
        *,
        cluster: str,
        service: str,
        taskSets: Sequence[str] = ...,
        include: Sequence[Literal["TAGS"]] = ...
    ) -> DescribeTaskSetsResponseTypeDef:
        """
        Describes the task sets in the specified cluster and service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.describe_task_sets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#describe_task_sets)
        """

    async def describe_tasks(
        self, *, tasks: Sequence[str], cluster: str = ..., include: Sequence[Literal["TAGS"]] = ...
    ) -> DescribeTasksResponseTypeDef:
        """
        Describes a specified task or tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.describe_tasks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#describe_tasks)
        """

    async def discover_poll_endpoint(
        self, *, containerInstance: str = ..., cluster: str = ...
    ) -> DiscoverPollEndpointResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.discover_poll_endpoint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#discover_poll_endpoint)
        """

    async def execute_command(
        self,
        *,
        command: str,
        interactive: bool,
        task: str,
        cluster: str = ...,
        container: str = ...
    ) -> ExecuteCommandResponseTypeDef:
        """
        Runs a command remotely on a container within a task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.execute_command)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#execute_command)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#generate_presigned_url)
        """

    async def list_account_settings(
        self,
        *,
        name: SettingNameType = ...,
        value: str = ...,
        principalArn: str = ...,
        effectiveSettings: bool = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListAccountSettingsResponseTypeDef:
        """
        Lists the account settings for a specified principal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.list_account_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#list_account_settings)
        """

    async def list_attributes(
        self,
        *,
        targetType: Literal["container-instance"],
        cluster: str = ...,
        attributeName: str = ...,
        attributeValue: str = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListAttributesResponseTypeDef:
        """
        Lists the attributes for Amazon ECS resources within a specified target type and
        cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.list_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#list_attributes)
        """

    async def list_clusters(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListClustersResponseTypeDef:
        """
        Returns a list of existing clusters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.list_clusters)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#list_clusters)
        """

    async def list_container_instances(
        self,
        *,
        cluster: str = ...,
        filter: str = ...,
        nextToken: str = ...,
        maxResults: int = ...,
        status: ContainerInstanceStatusType = ...
    ) -> ListContainerInstancesResponseTypeDef:
        """
        Returns a list of container instances in a specified cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.list_container_instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#list_container_instances)
        """

    async def list_services(
        self,
        *,
        cluster: str = ...,
        nextToken: str = ...,
        maxResults: int = ...,
        launchType: LaunchTypeType = ...,
        schedulingStrategy: SchedulingStrategyType = ...
    ) -> ListServicesResponseTypeDef:
        """
        Returns a list of services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.list_services)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#list_services)
        """

    async def list_tags_for_resource(
        self, *, resourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List the tags for an Amazon ECS resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#list_tags_for_resource)
        """

    async def list_task_definition_families(
        self,
        *,
        familyPrefix: str = ...,
        status: TaskDefinitionFamilyStatusType = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListTaskDefinitionFamiliesResponseTypeDef:
        """
        Returns a list of task definition families that are registered to your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.list_task_definition_families)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#list_task_definition_families)
        """

    async def list_task_definitions(
        self,
        *,
        familyPrefix: str = ...,
        status: TaskDefinitionStatusType = ...,
        sort: SortOrderType = ...,
        nextToken: str = ...,
        maxResults: int = ...
    ) -> ListTaskDefinitionsResponseTypeDef:
        """
        Returns a list of task definitions that are registered to your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.list_task_definitions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#list_task_definitions)
        """

    async def list_tasks(
        self,
        *,
        cluster: str = ...,
        containerInstance: str = ...,
        family: str = ...,
        nextToken: str = ...,
        maxResults: int = ...,
        startedBy: str = ...,
        serviceName: str = ...,
        desiredStatus: DesiredStatusType = ...,
        launchType: LaunchTypeType = ...
    ) -> ListTasksResponseTypeDef:
        """
        Returns a list of tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.list_tasks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#list_tasks)
        """

    async def put_account_setting(
        self, *, name: SettingNameType, value: str, principalArn: str = ...
    ) -> PutAccountSettingResponseTypeDef:
        """
        Modifies an account setting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.put_account_setting)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#put_account_setting)
        """

    async def put_account_setting_default(
        self, *, name: SettingNameType, value: str
    ) -> PutAccountSettingDefaultResponseTypeDef:
        """
        Modifies an account setting for all IAM users on an account for whom no
        individual account setting has been specified.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.put_account_setting_default)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#put_account_setting_default)
        """

    async def put_attributes(
        self, *, attributes: Sequence["AttributeTypeDef"], cluster: str = ...
    ) -> PutAttributesResponseTypeDef:
        """
        Create or update an attribute on an Amazon ECS resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.put_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#put_attributes)
        """

    async def put_cluster_capacity_providers(
        self,
        *,
        cluster: str,
        capacityProviders: Sequence[str],
        defaultCapacityProviderStrategy: Sequence["CapacityProviderStrategyItemTypeDef"]
    ) -> PutClusterCapacityProvidersResponseTypeDef:
        """
        Modifies the available capacity providers and the default capacity provider
        strategy for a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.put_cluster_capacity_providers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#put_cluster_capacity_providers)
        """

    async def register_container_instance(
        self,
        *,
        cluster: str = ...,
        instanceIdentityDocument: str = ...,
        instanceIdentityDocumentSignature: str = ...,
        totalResources: Sequence["ResourceTypeDef"] = ...,
        versionInfo: "VersionInfoTypeDef" = ...,
        containerInstanceArn: str = ...,
        attributes: Sequence["AttributeTypeDef"] = ...,
        platformDevices: Sequence["PlatformDeviceTypeDef"] = ...,
        tags: Sequence["TagTypeDef"] = ...
    ) -> RegisterContainerInstanceResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.register_container_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#register_container_instance)
        """

    async def register_task_definition(
        self,
        *,
        family: str,
        containerDefinitions: Sequence["ContainerDefinitionTypeDef"],
        taskRoleArn: str = ...,
        executionRoleArn: str = ...,
        networkMode: NetworkModeType = ...,
        volumes: Sequence["VolumeTypeDef"] = ...,
        placementConstraints: Sequence["TaskDefinitionPlacementConstraintTypeDef"] = ...,
        requiresCompatibilities: Sequence[CompatibilityType] = ...,
        cpu: str = ...,
        memory: str = ...,
        tags: Sequence["TagTypeDef"] = ...,
        pidMode: PidModeType = ...,
        ipcMode: IpcModeType = ...,
        proxyConfiguration: "ProxyConfigurationTypeDef" = ...,
        inferenceAccelerators: Sequence["InferenceAcceleratorTypeDef"] = ...,
        ephemeralStorage: "EphemeralStorageTypeDef" = ...,
        runtimePlatform: "RuntimePlatformTypeDef" = ...
    ) -> RegisterTaskDefinitionResponseTypeDef:
        """
        Registers a new task definition from the supplied `family` and
        `containerDefinitions`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.register_task_definition)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#register_task_definition)
        """

    async def run_task(
        self,
        *,
        taskDefinition: str,
        capacityProviderStrategy: Sequence["CapacityProviderStrategyItemTypeDef"] = ...,
        cluster: str = ...,
        count: int = ...,
        enableECSManagedTags: bool = ...,
        enableExecuteCommand: bool = ...,
        group: str = ...,
        launchType: LaunchTypeType = ...,
        networkConfiguration: "NetworkConfigurationTypeDef" = ...,
        overrides: "TaskOverrideTypeDef" = ...,
        placementConstraints: Sequence["PlacementConstraintTypeDef"] = ...,
        placementStrategy: Sequence["PlacementStrategyTypeDef"] = ...,
        platformVersion: str = ...,
        propagateTags: PropagateTagsType = ...,
        referenceId: str = ...,
        startedBy: str = ...,
        tags: Sequence["TagTypeDef"] = ...
    ) -> RunTaskResponseTypeDef:
        """
        Starts a new task using the specified task definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.run_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#run_task)
        """

    async def start_task(
        self,
        *,
        containerInstances: Sequence[str],
        taskDefinition: str,
        cluster: str = ...,
        enableECSManagedTags: bool = ...,
        enableExecuteCommand: bool = ...,
        group: str = ...,
        networkConfiguration: "NetworkConfigurationTypeDef" = ...,
        overrides: "TaskOverrideTypeDef" = ...,
        propagateTags: PropagateTagsType = ...,
        referenceId: str = ...,
        startedBy: str = ...,
        tags: Sequence["TagTypeDef"] = ...
    ) -> StartTaskResponseTypeDef:
        """
        Starts a new task from the specified task definition on the specified container
        instance or instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.start_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#start_task)
        """

    async def stop_task(
        self, *, task: str, cluster: str = ..., reason: str = ...
    ) -> StopTaskResponseTypeDef:
        """
        Stops a running task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.stop_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#stop_task)
        """

    async def submit_attachment_state_changes(
        self, *, attachments: Sequence["AttachmentStateChangeTypeDef"], cluster: str = ...
    ) -> SubmitAttachmentStateChangesResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.submit_attachment_state_changes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#submit_attachment_state_changes)
        """

    async def submit_container_state_change(
        self,
        *,
        cluster: str = ...,
        task: str = ...,
        containerName: str = ...,
        runtimeId: str = ...,
        status: str = ...,
        exitCode: int = ...,
        reason: str = ...,
        networkBindings: Sequence["NetworkBindingTypeDef"] = ...
    ) -> SubmitContainerStateChangeResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.submit_container_state_change)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#submit_container_state_change)
        """

    async def submit_task_state_change(
        self,
        *,
        cluster: str = ...,
        task: str = ...,
        status: str = ...,
        reason: str = ...,
        containers: Sequence["ContainerStateChangeTypeDef"] = ...,
        attachments: Sequence["AttachmentStateChangeTypeDef"] = ...,
        managedAgents: Sequence["ManagedAgentStateChangeTypeDef"] = ...,
        pullStartedAt: Union[datetime, str] = ...,
        pullStoppedAt: Union[datetime, str] = ...,
        executionStoppedAt: Union[datetime, str] = ...
    ) -> SubmitTaskStateChangeResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.submit_task_state_change)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#submit_task_state_change)
        """

    async def tag_resource(
        self, *, resourceArn: str, tags: Sequence["TagTypeDef"]
    ) -> Dict[str, Any]:
        """
        Associates the specified tags to a resource with the specified `resourceArn`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#tag_resource)
        """

    async def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Deletes specified tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#untag_resource)
        """

    async def update_capacity_provider(
        self, *, name: str, autoScalingGroupProvider: "AutoScalingGroupProviderUpdateTypeDef"
    ) -> UpdateCapacityProviderResponseTypeDef:
        """
        Modifies the parameters for a capacity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.update_capacity_provider)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#update_capacity_provider)
        """

    async def update_cluster(
        self,
        *,
        cluster: str,
        settings: Sequence["ClusterSettingTypeDef"] = ...,
        configuration: "ClusterConfigurationTypeDef" = ...
    ) -> UpdateClusterResponseTypeDef:
        """
        Updates the cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.update_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#update_cluster)
        """

    async def update_cluster_settings(
        self, *, cluster: str, settings: Sequence["ClusterSettingTypeDef"]
    ) -> UpdateClusterSettingsResponseTypeDef:
        """
        Modifies the settings to use for a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.update_cluster_settings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#update_cluster_settings)
        """

    async def update_container_agent(
        self, *, containerInstance: str, cluster: str = ...
    ) -> UpdateContainerAgentResponseTypeDef:
        """
        Updates the Amazon ECS container agent on a specified container instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.update_container_agent)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#update_container_agent)
        """

    async def update_container_instances_state(
        self,
        *,
        containerInstances: Sequence[str],
        status: ContainerInstanceStatusType,
        cluster: str = ...
    ) -> UpdateContainerInstancesStateResponseTypeDef:
        """
        Modifies the status of an Amazon ECS container instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.update_container_instances_state)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#update_container_instances_state)
        """

    async def update_service(
        self,
        *,
        service: str,
        cluster: str = ...,
        desiredCount: int = ...,
        taskDefinition: str = ...,
        capacityProviderStrategy: Sequence["CapacityProviderStrategyItemTypeDef"] = ...,
        deploymentConfiguration: "DeploymentConfigurationTypeDef" = ...,
        networkConfiguration: "NetworkConfigurationTypeDef" = ...,
        placementConstraints: Sequence["PlacementConstraintTypeDef"] = ...,
        placementStrategy: Sequence["PlacementStrategyTypeDef"] = ...,
        platformVersion: str = ...,
        forceNewDeployment: bool = ...,
        healthCheckGracePeriodSeconds: int = ...,
        enableExecuteCommand: bool = ...,
        enableECSManagedTags: bool = ...,
        loadBalancers: Sequence["LoadBalancerTypeDef"] = ...,
        propagateTags: PropagateTagsType = ...,
        serviceRegistries: Sequence["ServiceRegistryTypeDef"] = ...
    ) -> UpdateServiceResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.update_service)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#update_service)
        """

    async def update_service_primary_task_set(
        self, *, cluster: str, service: str, primaryTaskSet: str
    ) -> UpdateServicePrimaryTaskSetResponseTypeDef:
        """
        Modifies which task set in a service is the primary task set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.update_service_primary_task_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#update_service_primary_task_set)
        """

    async def update_task_set(
        self, *, cluster: str, service: str, taskSet: str, scale: "ScaleTypeDef"
    ) -> UpdateTaskSetResponseTypeDef:
        """
        Modifies a task set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.update_task_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#update_task_set)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_account_settings"]
    ) -> ListAccountSettingsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_attributes"]) -> ListAttributesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_clusters"]) -> ListClustersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_container_instances"]
    ) -> ListContainerInstancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_services"]) -> ListServicesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_task_definition_families"]
    ) -> ListTaskDefinitionFamiliesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_task_definitions"]
    ) -> ListTaskDefinitionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_tasks"]) -> ListTasksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["services_inactive"]) -> ServicesInactiveWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["services_stable"]) -> ServicesStableWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["tasks_running"]) -> TasksRunningWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["tasks_stopped"]) -> TasksStoppedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/#get_waiter)
        """

    async def __aenter__(self) -> "ECSClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/client/)
        """
