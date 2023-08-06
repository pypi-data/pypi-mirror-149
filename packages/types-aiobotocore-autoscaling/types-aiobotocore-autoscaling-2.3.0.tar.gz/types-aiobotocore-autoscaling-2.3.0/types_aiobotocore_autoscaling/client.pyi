"""
Type annotations for autoscaling service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_autoscaling.client import AutoScalingClient

    session = get_session()
    async with session.create_client("autoscaling") as client:
        client: AutoScalingClient
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import WarmPoolStateType
from .paginator import (
    DescribeAutoScalingGroupsPaginator,
    DescribeAutoScalingInstancesPaginator,
    DescribeLaunchConfigurationsPaginator,
    DescribeLoadBalancersPaginator,
    DescribeLoadBalancerTargetGroupsPaginator,
    DescribeNotificationConfigurationsPaginator,
    DescribePoliciesPaginator,
    DescribeScalingActivitiesPaginator,
    DescribeScheduledActionsPaginator,
    DescribeTagsPaginator,
)
from .type_defs import (
    ActivitiesTypeTypeDef,
    ActivityTypeTypeDef,
    AutoScalingGroupsTypeTypeDef,
    AutoScalingInstancesTypeTypeDef,
    BatchDeleteScheduledActionAnswerTypeDef,
    BatchPutScheduledUpdateGroupActionAnswerTypeDef,
    BlockDeviceMappingTypeDef,
    CancelInstanceRefreshAnswerTypeDef,
    DescribeAccountLimitsAnswerTypeDef,
    DescribeAdjustmentTypesAnswerTypeDef,
    DescribeAutoScalingNotificationTypesAnswerTypeDef,
    DescribeInstanceRefreshesAnswerTypeDef,
    DescribeLifecycleHooksAnswerTypeDef,
    DescribeLifecycleHookTypesAnswerTypeDef,
    DescribeLoadBalancersResponseTypeDef,
    DescribeLoadBalancerTargetGroupsResponseTypeDef,
    DescribeMetricCollectionTypesAnswerTypeDef,
    DescribeNotificationConfigurationsAnswerTypeDef,
    DescribeTerminationPolicyTypesAnswerTypeDef,
    DescribeWarmPoolAnswerTypeDef,
    DesiredConfigurationTypeDef,
    DetachInstancesAnswerTypeDef,
    EnterStandbyAnswerTypeDef,
    ExitStandbyAnswerTypeDef,
    FilterTypeDef,
    GetPredictiveScalingForecastAnswerTypeDef,
    InstanceMetadataOptionsTypeDef,
    InstanceMonitoringTypeDef,
    InstanceReusePolicyTypeDef,
    LaunchConfigurationsTypeTypeDef,
    LaunchTemplateSpecificationTypeDef,
    LifecycleHookSpecificationTypeDef,
    MixedInstancesPolicyTypeDef,
    PoliciesTypeTypeDef,
    PolicyARNTypeTypeDef,
    PredictiveScalingConfigurationTypeDef,
    ProcessesTypeTypeDef,
    RefreshPreferencesTypeDef,
    ScheduledActionsTypeTypeDef,
    ScheduledUpdateGroupActionRequestTypeDef,
    StartInstanceRefreshAnswerTypeDef,
    StepAdjustmentTypeDef,
    TagsTypeTypeDef,
    TagTypeDef,
    TargetTrackingConfigurationTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("AutoScalingClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ActiveInstanceRefreshNotFoundFault: Type[BotocoreClientError]
    AlreadyExistsFault: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InstanceRefreshInProgressFault: Type[BotocoreClientError]
    InvalidNextToken: Type[BotocoreClientError]
    LimitExceededFault: Type[BotocoreClientError]
    ResourceContentionFault: Type[BotocoreClientError]
    ResourceInUseFault: Type[BotocoreClientError]
    ScalingActivityInProgressFault: Type[BotocoreClientError]
    ServiceLinkedRoleFailure: Type[BotocoreClientError]

class AutoScalingClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AutoScalingClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#exceptions)
        """
    async def attach_instances(
        self, *, AutoScalingGroupName: str, InstanceIds: Sequence[str] = ...
    ) -> None:
        """
        Attaches one or more EC2 instances to the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.attach_instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#attach_instances)
        """
    async def attach_load_balancer_target_groups(
        self, *, AutoScalingGroupName: str, TargetGroupARNs: Sequence[str]
    ) -> Dict[str, Any]:
        """
        Attaches one or more target groups to the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.attach_load_balancer_target_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#attach_load_balancer_target_groups)
        """
    async def attach_load_balancers(
        self, *, AutoScalingGroupName: str, LoadBalancerNames: Sequence[str]
    ) -> Dict[str, Any]:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.attach_load_balancers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#attach_load_balancers)
        """
    async def batch_delete_scheduled_action(
        self, *, AutoScalingGroupName: str, ScheduledActionNames: Sequence[str]
    ) -> BatchDeleteScheduledActionAnswerTypeDef:
        """
        Deletes one or more scheduled actions for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.batch_delete_scheduled_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#batch_delete_scheduled_action)
        """
    async def batch_put_scheduled_update_group_action(
        self,
        *,
        AutoScalingGroupName: str,
        ScheduledUpdateGroupActions: Sequence["ScheduledUpdateGroupActionRequestTypeDef"]
    ) -> BatchPutScheduledUpdateGroupActionAnswerTypeDef:
        """
        Creates or updates one or more scheduled scaling actions for an Auto Scaling
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.batch_put_scheduled_update_group_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#batch_put_scheduled_update_group_action)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#can_paginate)
        """
    async def cancel_instance_refresh(
        self, *, AutoScalingGroupName: str
    ) -> CancelInstanceRefreshAnswerTypeDef:
        """
        Cancels an instance refresh operation in progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.cancel_instance_refresh)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#cancel_instance_refresh)
        """
    async def complete_lifecycle_action(
        self,
        *,
        LifecycleHookName: str,
        AutoScalingGroupName: str,
        LifecycleActionResult: str,
        LifecycleActionToken: str = ...,
        InstanceId: str = ...
    ) -> Dict[str, Any]:
        """
        Completes the lifecycle action for the specified token or instance with the
        specified result.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.complete_lifecycle_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#complete_lifecycle_action)
        """
    async def create_auto_scaling_group(
        self,
        *,
        AutoScalingGroupName: str,
        MinSize: int,
        MaxSize: int,
        LaunchConfigurationName: str = ...,
        LaunchTemplate: "LaunchTemplateSpecificationTypeDef" = ...,
        MixedInstancesPolicy: "MixedInstancesPolicyTypeDef" = ...,
        InstanceId: str = ...,
        DesiredCapacity: int = ...,
        DefaultCooldown: int = ...,
        AvailabilityZones: Sequence[str] = ...,
        LoadBalancerNames: Sequence[str] = ...,
        TargetGroupARNs: Sequence[str] = ...,
        HealthCheckType: str = ...,
        HealthCheckGracePeriod: int = ...,
        PlacementGroup: str = ...,
        VPCZoneIdentifier: str = ...,
        TerminationPolicies: Sequence[str] = ...,
        NewInstancesProtectedFromScaleIn: bool = ...,
        CapacityRebalance: bool = ...,
        LifecycleHookSpecificationList: Sequence["LifecycleHookSpecificationTypeDef"] = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        ServiceLinkedRoleARN: str = ...,
        MaxInstanceLifetime: int = ...,
        Context: str = ...,
        DesiredCapacityType: str = ...
    ) -> None:
        """
        **We strongly recommend using a launch template when calling this operation to
        ensure full functionality for Amazon EC2 Auto Scaling and Amazon EC2.** Creates
        an Auto Scaling group with the specified name and attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.create_auto_scaling_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#create_auto_scaling_group)
        """
    async def create_launch_configuration(
        self,
        *,
        LaunchConfigurationName: str,
        ImageId: str = ...,
        KeyName: str = ...,
        SecurityGroups: Sequence[str] = ...,
        ClassicLinkVPCId: str = ...,
        ClassicLinkVPCSecurityGroups: Sequence[str] = ...,
        UserData: str = ...,
        InstanceId: str = ...,
        InstanceType: str = ...,
        KernelId: str = ...,
        RamdiskId: str = ...,
        BlockDeviceMappings: Sequence["BlockDeviceMappingTypeDef"] = ...,
        InstanceMonitoring: "InstanceMonitoringTypeDef" = ...,
        SpotPrice: str = ...,
        IamInstanceProfile: str = ...,
        EbsOptimized: bool = ...,
        AssociatePublicIpAddress: bool = ...,
        PlacementTenancy: str = ...,
        MetadataOptions: "InstanceMetadataOptionsTypeDef" = ...
    ) -> None:
        """
        Creates a launch configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.create_launch_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#create_launch_configuration)
        """
    async def create_or_update_tags(self, *, Tags: Sequence["TagTypeDef"]) -> None:
        """
        Creates or updates tags for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.create_or_update_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#create_or_update_tags)
        """
    async def delete_auto_scaling_group(
        self, *, AutoScalingGroupName: str, ForceDelete: bool = ...
    ) -> None:
        """
        Deletes the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.delete_auto_scaling_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#delete_auto_scaling_group)
        """
    async def delete_launch_configuration(self, *, LaunchConfigurationName: str) -> None:
        """
        Deletes the specified launch configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.delete_launch_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#delete_launch_configuration)
        """
    async def delete_lifecycle_hook(
        self, *, LifecycleHookName: str, AutoScalingGroupName: str
    ) -> Dict[str, Any]:
        """
        Deletes the specified lifecycle hook.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.delete_lifecycle_hook)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#delete_lifecycle_hook)
        """
    async def delete_notification_configuration(
        self, *, AutoScalingGroupName: str, TopicARN: str
    ) -> None:
        """
        Deletes the specified notification.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.delete_notification_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#delete_notification_configuration)
        """
    async def delete_policy(self, *, PolicyName: str, AutoScalingGroupName: str = ...) -> None:
        """
        Deletes the specified scaling policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.delete_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#delete_policy)
        """
    async def delete_scheduled_action(
        self, *, AutoScalingGroupName: str, ScheduledActionName: str
    ) -> None:
        """
        Deletes the specified scheduled action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.delete_scheduled_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#delete_scheduled_action)
        """
    async def delete_tags(self, *, Tags: Sequence["TagTypeDef"]) -> None:
        """
        Deletes the specified tags.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.delete_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#delete_tags)
        """
    async def delete_warm_pool(
        self, *, AutoScalingGroupName: str, ForceDelete: bool = ...
    ) -> Dict[str, Any]:
        """
        Deletes the warm pool for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.delete_warm_pool)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#delete_warm_pool)
        """
    async def describe_account_limits(self) -> DescribeAccountLimitsAnswerTypeDef:
        """
        Describes the current Amazon EC2 Auto Scaling resource quotas for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_account_limits)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_account_limits)
        """
    async def describe_adjustment_types(self) -> DescribeAdjustmentTypesAnswerTypeDef:
        """
        Describes the available adjustment types for step scaling and simple scaling
        policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_adjustment_types)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_adjustment_types)
        """
    async def describe_auto_scaling_groups(
        self,
        *,
        AutoScalingGroupNames: Sequence[str] = ...,
        NextToken: str = ...,
        MaxRecords: int = ...,
        Filters: Sequence["FilterTypeDef"] = ...
    ) -> AutoScalingGroupsTypeTypeDef:
        """
        Gets information about the Auto Scaling groups in the account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_auto_scaling_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_auto_scaling_groups)
        """
    async def describe_auto_scaling_instances(
        self, *, InstanceIds: Sequence[str] = ..., MaxRecords: int = ..., NextToken: str = ...
    ) -> AutoScalingInstancesTypeTypeDef:
        """
        Gets information about the Auto Scaling instances in the account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_auto_scaling_instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_auto_scaling_instances)
        """
    async def describe_auto_scaling_notification_types(
        self,
    ) -> DescribeAutoScalingNotificationTypesAnswerTypeDef:
        """
        Describes the notification types that are supported by Amazon EC2 Auto Scaling.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_auto_scaling_notification_types)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_auto_scaling_notification_types)
        """
    async def describe_instance_refreshes(
        self,
        *,
        AutoScalingGroupName: str,
        InstanceRefreshIds: Sequence[str] = ...,
        NextToken: str = ...,
        MaxRecords: int = ...
    ) -> DescribeInstanceRefreshesAnswerTypeDef:
        """
        Gets information about the instance refreshes for the specified Auto Scaling
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_instance_refreshes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_instance_refreshes)
        """
    async def describe_launch_configurations(
        self,
        *,
        LaunchConfigurationNames: Sequence[str] = ...,
        NextToken: str = ...,
        MaxRecords: int = ...
    ) -> LaunchConfigurationsTypeTypeDef:
        """
        Gets information about the launch configurations in the account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_launch_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_launch_configurations)
        """
    async def describe_lifecycle_hook_types(self) -> DescribeLifecycleHookTypesAnswerTypeDef:
        """
        Describes the available types of lifecycle hooks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_lifecycle_hook_types)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_lifecycle_hook_types)
        """
    async def describe_lifecycle_hooks(
        self, *, AutoScalingGroupName: str, LifecycleHookNames: Sequence[str] = ...
    ) -> DescribeLifecycleHooksAnswerTypeDef:
        """
        Gets information about the lifecycle hooks for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_lifecycle_hooks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_lifecycle_hooks)
        """
    async def describe_load_balancer_target_groups(
        self, *, AutoScalingGroupName: str, NextToken: str = ..., MaxRecords: int = ...
    ) -> DescribeLoadBalancerTargetGroupsResponseTypeDef:
        """
        Gets information about the load balancer target groups for the specified Auto
        Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_load_balancer_target_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_load_balancer_target_groups)
        """
    async def describe_load_balancers(
        self, *, AutoScalingGroupName: str, NextToken: str = ..., MaxRecords: int = ...
    ) -> DescribeLoadBalancersResponseTypeDef:
        """
        Gets information about the load balancers for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_load_balancers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_load_balancers)
        """
    async def describe_metric_collection_types(self) -> DescribeMetricCollectionTypesAnswerTypeDef:
        """
        Describes the available CloudWatch metrics for Amazon EC2 Auto Scaling.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_metric_collection_types)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_metric_collection_types)
        """
    async def describe_notification_configurations(
        self,
        *,
        AutoScalingGroupNames: Sequence[str] = ...,
        NextToken: str = ...,
        MaxRecords: int = ...
    ) -> DescribeNotificationConfigurationsAnswerTypeDef:
        """
        Gets information about the Amazon SNS notifications that are configured for one
        or more Auto Scaling groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_notification_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_notification_configurations)
        """
    async def describe_policies(
        self,
        *,
        AutoScalingGroupName: str = ...,
        PolicyNames: Sequence[str] = ...,
        PolicyTypes: Sequence[str] = ...,
        NextToken: str = ...,
        MaxRecords: int = ...
    ) -> PoliciesTypeTypeDef:
        """
        Gets information about the scaling policies in the account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_policies)
        """
    async def describe_scaling_activities(
        self,
        *,
        ActivityIds: Sequence[str] = ...,
        AutoScalingGroupName: str = ...,
        IncludeDeletedGroups: bool = ...,
        MaxRecords: int = ...,
        NextToken: str = ...
    ) -> ActivitiesTypeTypeDef:
        """
        Gets information about the scaling activities in the account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_scaling_activities)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_scaling_activities)
        """
    async def describe_scaling_process_types(self) -> ProcessesTypeTypeDef:
        """
        Describes the scaling process types for use with the  ResumeProcesses and
        SuspendProcesses APIs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_scaling_process_types)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_scaling_process_types)
        """
    async def describe_scheduled_actions(
        self,
        *,
        AutoScalingGroupName: str = ...,
        ScheduledActionNames: Sequence[str] = ...,
        StartTime: Union[datetime, str] = ...,
        EndTime: Union[datetime, str] = ...,
        NextToken: str = ...,
        MaxRecords: int = ...
    ) -> ScheduledActionsTypeTypeDef:
        """
        Gets information about the scheduled actions that haven't run or that have not
        reached their end time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_scheduled_actions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_scheduled_actions)
        """
    async def describe_tags(
        self,
        *,
        Filters: Sequence["FilterTypeDef"] = ...,
        NextToken: str = ...,
        MaxRecords: int = ...
    ) -> TagsTypeTypeDef:
        """
        Describes the specified tags.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_tags)
        """
    async def describe_termination_policy_types(
        self,
    ) -> DescribeTerminationPolicyTypesAnswerTypeDef:
        """
        Describes the termination policies supported by Amazon EC2 Auto Scaling.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_termination_policy_types)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_termination_policy_types)
        """
    async def describe_warm_pool(
        self, *, AutoScalingGroupName: str, MaxRecords: int = ..., NextToken: str = ...
    ) -> DescribeWarmPoolAnswerTypeDef:
        """
        Gets information about a warm pool and its instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_warm_pool)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#describe_warm_pool)
        """
    async def detach_instances(
        self,
        *,
        AutoScalingGroupName: str,
        ShouldDecrementDesiredCapacity: bool,
        InstanceIds: Sequence[str] = ...
    ) -> DetachInstancesAnswerTypeDef:
        """
        Removes one or more instances from the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.detach_instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#detach_instances)
        """
    async def detach_load_balancer_target_groups(
        self, *, AutoScalingGroupName: str, TargetGroupARNs: Sequence[str]
    ) -> Dict[str, Any]:
        """
        Detaches one or more target groups from the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.detach_load_balancer_target_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#detach_load_balancer_target_groups)
        """
    async def detach_load_balancers(
        self, *, AutoScalingGroupName: str, LoadBalancerNames: Sequence[str]
    ) -> Dict[str, Any]:
        """
        Detaches one or more Classic Load Balancers from the specified Auto Scaling
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.detach_load_balancers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#detach_load_balancers)
        """
    async def disable_metrics_collection(
        self, *, AutoScalingGroupName: str, Metrics: Sequence[str] = ...
    ) -> None:
        """
        Disables group metrics for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.disable_metrics_collection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#disable_metrics_collection)
        """
    async def enable_metrics_collection(
        self, *, AutoScalingGroupName: str, Granularity: str, Metrics: Sequence[str] = ...
    ) -> None:
        """
        Enables group metrics for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.enable_metrics_collection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#enable_metrics_collection)
        """
    async def enter_standby(
        self,
        *,
        AutoScalingGroupName: str,
        ShouldDecrementDesiredCapacity: bool,
        InstanceIds: Sequence[str] = ...
    ) -> EnterStandbyAnswerTypeDef:
        """
        Moves the specified instances into the standby state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.enter_standby)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#enter_standby)
        """
    async def execute_policy(
        self,
        *,
        PolicyName: str,
        AutoScalingGroupName: str = ...,
        HonorCooldown: bool = ...,
        MetricValue: float = ...,
        BreachThreshold: float = ...
    ) -> None:
        """
        Executes the specified policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.execute_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#execute_policy)
        """
    async def exit_standby(
        self, *, AutoScalingGroupName: str, InstanceIds: Sequence[str] = ...
    ) -> ExitStandbyAnswerTypeDef:
        """
        Moves the specified instances out of the standby state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.exit_standby)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#exit_standby)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#generate_presigned_url)
        """
    async def get_predictive_scaling_forecast(
        self,
        *,
        AutoScalingGroupName: str,
        PolicyName: str,
        StartTime: Union[datetime, str],
        EndTime: Union[datetime, str]
    ) -> GetPredictiveScalingForecastAnswerTypeDef:
        """
        Retrieves the forecast data for a predictive scaling policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_predictive_scaling_forecast)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#get_predictive_scaling_forecast)
        """
    async def put_lifecycle_hook(
        self,
        *,
        LifecycleHookName: str,
        AutoScalingGroupName: str,
        LifecycleTransition: str = ...,
        RoleARN: str = ...,
        NotificationTargetARN: str = ...,
        NotificationMetadata: str = ...,
        HeartbeatTimeout: int = ...,
        DefaultResult: str = ...
    ) -> Dict[str, Any]:
        """
        Creates or updates a lifecycle hook for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.put_lifecycle_hook)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#put_lifecycle_hook)
        """
    async def put_notification_configuration(
        self, *, AutoScalingGroupName: str, TopicARN: str, NotificationTypes: Sequence[str]
    ) -> None:
        """
        Configures an Auto Scaling group to send notifications when specified events
        take place.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.put_notification_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#put_notification_configuration)
        """
    async def put_scaling_policy(
        self,
        *,
        AutoScalingGroupName: str,
        PolicyName: str,
        PolicyType: str = ...,
        AdjustmentType: str = ...,
        MinAdjustmentStep: int = ...,
        MinAdjustmentMagnitude: int = ...,
        ScalingAdjustment: int = ...,
        Cooldown: int = ...,
        MetricAggregationType: str = ...,
        StepAdjustments: Sequence["StepAdjustmentTypeDef"] = ...,
        EstimatedInstanceWarmup: int = ...,
        TargetTrackingConfiguration: "TargetTrackingConfigurationTypeDef" = ...,
        Enabled: bool = ...,
        PredictiveScalingConfiguration: "PredictiveScalingConfigurationTypeDef" = ...
    ) -> PolicyARNTypeTypeDef:
        """
        Creates or updates a scaling policy for an Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.put_scaling_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#put_scaling_policy)
        """
    async def put_scheduled_update_group_action(
        self,
        *,
        AutoScalingGroupName: str,
        ScheduledActionName: str,
        Time: Union[datetime, str] = ...,
        StartTime: Union[datetime, str] = ...,
        EndTime: Union[datetime, str] = ...,
        Recurrence: str = ...,
        MinSize: int = ...,
        MaxSize: int = ...,
        DesiredCapacity: int = ...,
        TimeZone: str = ...
    ) -> None:
        """
        Creates or updates a scheduled scaling action for an Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.put_scheduled_update_group_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#put_scheduled_update_group_action)
        """
    async def put_warm_pool(
        self,
        *,
        AutoScalingGroupName: str,
        MaxGroupPreparedCapacity: int = ...,
        MinSize: int = ...,
        PoolState: WarmPoolStateType = ...,
        InstanceReusePolicy: "InstanceReusePolicyTypeDef" = ...
    ) -> Dict[str, Any]:
        """
        Creates or updates a warm pool for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.put_warm_pool)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#put_warm_pool)
        """
    async def record_lifecycle_action_heartbeat(
        self,
        *,
        LifecycleHookName: str,
        AutoScalingGroupName: str,
        LifecycleActionToken: str = ...,
        InstanceId: str = ...
    ) -> Dict[str, Any]:
        """
        Records a heartbeat for the lifecycle action associated with the specified token
        or instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.record_lifecycle_action_heartbeat)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#record_lifecycle_action_heartbeat)
        """
    async def resume_processes(
        self, *, AutoScalingGroupName: str, ScalingProcesses: Sequence[str] = ...
    ) -> None:
        """
        Resumes the specified suspended auto scaling processes, or all suspended
        process, for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.resume_processes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#resume_processes)
        """
    async def set_desired_capacity(
        self, *, AutoScalingGroupName: str, DesiredCapacity: int, HonorCooldown: bool = ...
    ) -> None:
        """
        Sets the size of the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.set_desired_capacity)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#set_desired_capacity)
        """
    async def set_instance_health(
        self, *, InstanceId: str, HealthStatus: str, ShouldRespectGracePeriod: bool = ...
    ) -> None:
        """
        Sets the health status of the specified instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.set_instance_health)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#set_instance_health)
        """
    async def set_instance_protection(
        self, *, InstanceIds: Sequence[str], AutoScalingGroupName: str, ProtectedFromScaleIn: bool
    ) -> Dict[str, Any]:
        """
        Updates the instance protection settings of the specified instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.set_instance_protection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#set_instance_protection)
        """
    async def start_instance_refresh(
        self,
        *,
        AutoScalingGroupName: str,
        Strategy: Literal["Rolling"] = ...,
        DesiredConfiguration: "DesiredConfigurationTypeDef" = ...,
        Preferences: "RefreshPreferencesTypeDef" = ...
    ) -> StartInstanceRefreshAnswerTypeDef:
        """
        Starts a new instance refresh operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.start_instance_refresh)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#start_instance_refresh)
        """
    async def suspend_processes(
        self, *, AutoScalingGroupName: str, ScalingProcesses: Sequence[str] = ...
    ) -> None:
        """
        Suspends the specified auto scaling processes, or all processes, for the
        specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.suspend_processes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#suspend_processes)
        """
    async def terminate_instance_in_auto_scaling_group(
        self, *, InstanceId: str, ShouldDecrementDesiredCapacity: bool
    ) -> ActivityTypeTypeDef:
        """
        Terminates the specified instance and optionally adjusts the desired group size.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.terminate_instance_in_auto_scaling_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#terminate_instance_in_auto_scaling_group)
        """
    async def update_auto_scaling_group(
        self,
        *,
        AutoScalingGroupName: str,
        LaunchConfigurationName: str = ...,
        LaunchTemplate: "LaunchTemplateSpecificationTypeDef" = ...,
        MixedInstancesPolicy: "MixedInstancesPolicyTypeDef" = ...,
        MinSize: int = ...,
        MaxSize: int = ...,
        DesiredCapacity: int = ...,
        DefaultCooldown: int = ...,
        AvailabilityZones: Sequence[str] = ...,
        HealthCheckType: str = ...,
        HealthCheckGracePeriod: int = ...,
        PlacementGroup: str = ...,
        VPCZoneIdentifier: str = ...,
        TerminationPolicies: Sequence[str] = ...,
        NewInstancesProtectedFromScaleIn: bool = ...,
        ServiceLinkedRoleARN: str = ...,
        MaxInstanceLifetime: int = ...,
        CapacityRebalance: bool = ...,
        Context: str = ...,
        DesiredCapacityType: str = ...
    ) -> None:
        """
        **We strongly recommend that all Auto Scaling groups use launch templates to
        ensure full functionality for Amazon EC2 Auto Scaling and Amazon EC2.** Updates
        the configuration for the specified Auto Scaling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.update_auto_scaling_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#update_auto_scaling_group)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["describe_auto_scaling_groups"]
    ) -> DescribeAutoScalingGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["describe_auto_scaling_instances"]
    ) -> DescribeAutoScalingInstancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["describe_launch_configurations"]
    ) -> DescribeLaunchConfigurationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["describe_load_balancer_target_groups"]
    ) -> DescribeLoadBalancerTargetGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["describe_load_balancers"]
    ) -> DescribeLoadBalancersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["describe_notification_configurations"]
    ) -> DescribeNotificationConfigurationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["describe_policies"]
    ) -> DescribePoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["describe_scaling_activities"]
    ) -> DescribeScalingActivitiesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["describe_scheduled_actions"]
    ) -> DescribeScheduledActionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["describe_tags"]) -> DescribeTagsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/#get_paginator)
        """
    async def __aenter__(self) -> "AutoScalingClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling/client/)
        """
