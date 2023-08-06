"""
Type annotations for batch service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_batch.client import BatchClient

    session = get_session()
    async with session.create_client("batch") as client:
        client: BatchClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    CEStateType,
    CETypeType,
    JobDefinitionTypeType,
    JobStatusType,
    JQStateType,
    PlatformCapabilityType,
)
from .paginator import (
    DescribeComputeEnvironmentsPaginator,
    DescribeJobDefinitionsPaginator,
    DescribeJobQueuesPaginator,
    ListJobsPaginator,
    ListSchedulingPoliciesPaginator,
)
from .type_defs import (
    ArrayPropertiesTypeDef,
    ComputeEnvironmentOrderTypeDef,
    ComputeResourceTypeDef,
    ComputeResourceUpdateTypeDef,
    ContainerOverridesTypeDef,
    ContainerPropertiesTypeDef,
    CreateComputeEnvironmentResponseTypeDef,
    CreateJobQueueResponseTypeDef,
    CreateSchedulingPolicyResponseTypeDef,
    DescribeComputeEnvironmentsResponseTypeDef,
    DescribeJobDefinitionsResponseTypeDef,
    DescribeJobQueuesResponseTypeDef,
    DescribeJobsResponseTypeDef,
    DescribeSchedulingPoliciesResponseTypeDef,
    FairsharePolicyTypeDef,
    JobDependencyTypeDef,
    JobTimeoutTypeDef,
    KeyValuesPairTypeDef,
    ListJobsResponseTypeDef,
    ListSchedulingPoliciesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    NodeOverridesTypeDef,
    NodePropertiesTypeDef,
    RegisterJobDefinitionResponseTypeDef,
    RetryStrategyTypeDef,
    SubmitJobResponseTypeDef,
    UpdateComputeEnvironmentResponseTypeDef,
    UpdateJobQueueResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("BatchClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    ClientException: Type[BotocoreClientError]
    ServerException: Type[BotocoreClientError]

class BatchClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        BatchClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#exceptions)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#can_paginate)
        """
    async def cancel_job(self, *, jobId: str, reason: str) -> Dict[str, Any]:
        """
        Cancels a job in an Batch job queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.cancel_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#cancel_job)
        """
    async def create_compute_environment(
        self,
        *,
        computeEnvironmentName: str,
        type: CETypeType,
        state: CEStateType = ...,
        unmanagedvCpus: int = ...,
        computeResources: "ComputeResourceTypeDef" = ...,
        serviceRole: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateComputeEnvironmentResponseTypeDef:
        """
        Creates an Batch compute environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.create_compute_environment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#create_compute_environment)
        """
    async def create_job_queue(
        self,
        *,
        jobQueueName: str,
        priority: int,
        computeEnvironmentOrder: Sequence["ComputeEnvironmentOrderTypeDef"],
        state: JQStateType = ...,
        schedulingPolicyArn: str = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateJobQueueResponseTypeDef:
        """
        Creates an Batch job queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.create_job_queue)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#create_job_queue)
        """
    async def create_scheduling_policy(
        self,
        *,
        name: str,
        fairsharePolicy: "FairsharePolicyTypeDef" = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateSchedulingPolicyResponseTypeDef:
        """
        Creates an Batch scheduling policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.create_scheduling_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#create_scheduling_policy)
        """
    async def delete_compute_environment(self, *, computeEnvironment: str) -> Dict[str, Any]:
        """
        Deletes an Batch compute environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.delete_compute_environment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#delete_compute_environment)
        """
    async def delete_job_queue(self, *, jobQueue: str) -> Dict[str, Any]:
        """
        Deletes the specified job queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.delete_job_queue)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#delete_job_queue)
        """
    async def delete_scheduling_policy(self, *, arn: str) -> Dict[str, Any]:
        """
        Deletes the specified scheduling policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.delete_scheduling_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#delete_scheduling_policy)
        """
    async def deregister_job_definition(self, *, jobDefinition: str) -> Dict[str, Any]:
        """
        Deregisters an Batch job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.deregister_job_definition)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#deregister_job_definition)
        """
    async def describe_compute_environments(
        self,
        *,
        computeEnvironments: Sequence[str] = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> DescribeComputeEnvironmentsResponseTypeDef:
        """
        Describes one or more of your compute environments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.describe_compute_environments)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#describe_compute_environments)
        """
    async def describe_job_definitions(
        self,
        *,
        jobDefinitions: Sequence[str] = ...,
        maxResults: int = ...,
        jobDefinitionName: str = ...,
        status: str = ...,
        nextToken: str = ...
    ) -> DescribeJobDefinitionsResponseTypeDef:
        """
        Describes a list of job definitions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.describe_job_definitions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#describe_job_definitions)
        """
    async def describe_job_queues(
        self, *, jobQueues: Sequence[str] = ..., maxResults: int = ..., nextToken: str = ...
    ) -> DescribeJobQueuesResponseTypeDef:
        """
        Describes one or more of your job queues.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.describe_job_queues)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#describe_job_queues)
        """
    async def describe_jobs(self, *, jobs: Sequence[str]) -> DescribeJobsResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.describe_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#describe_jobs)
        """
    async def describe_scheduling_policies(
        self, *, arns: Sequence[str]
    ) -> DescribeSchedulingPoliciesResponseTypeDef:
        """
        Describes one or more of your scheduling policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.describe_scheduling_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#describe_scheduling_policies)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#generate_presigned_url)
        """
    async def list_jobs(
        self,
        *,
        jobQueue: str = ...,
        arrayJobId: str = ...,
        multiNodeJobId: str = ...,
        jobStatus: JobStatusType = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        filters: Sequence["KeyValuesPairTypeDef"] = ...
    ) -> ListJobsResponseTypeDef:
        """
        Returns a list of Batch jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.list_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#list_jobs)
        """
    async def list_scheduling_policies(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListSchedulingPoliciesResponseTypeDef:
        """
        Returns a list of Batch scheduling policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.list_scheduling_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#list_scheduling_policies)
        """
    async def list_tags_for_resource(
        self, *, resourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for an Batch resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#list_tags_for_resource)
        """
    async def register_job_definition(
        self,
        *,
        jobDefinitionName: str,
        type: JobDefinitionTypeType,
        parameters: Mapping[str, str] = ...,
        schedulingPriority: int = ...,
        containerProperties: "ContainerPropertiesTypeDef" = ...,
        nodeProperties: "NodePropertiesTypeDef" = ...,
        retryStrategy: "RetryStrategyTypeDef" = ...,
        propagateTags: bool = ...,
        timeout: "JobTimeoutTypeDef" = ...,
        tags: Mapping[str, str] = ...,
        platformCapabilities: Sequence[PlatformCapabilityType] = ...
    ) -> RegisterJobDefinitionResponseTypeDef:
        """
        Registers an Batch job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.register_job_definition)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#register_job_definition)
        """
    async def submit_job(
        self,
        *,
        jobName: str,
        jobQueue: str,
        jobDefinition: str,
        shareIdentifier: str = ...,
        schedulingPriorityOverride: int = ...,
        arrayProperties: "ArrayPropertiesTypeDef" = ...,
        dependsOn: Sequence["JobDependencyTypeDef"] = ...,
        parameters: Mapping[str, str] = ...,
        containerOverrides: "ContainerOverridesTypeDef" = ...,
        nodeOverrides: "NodeOverridesTypeDef" = ...,
        retryStrategy: "RetryStrategyTypeDef" = ...,
        propagateTags: bool = ...,
        timeout: "JobTimeoutTypeDef" = ...,
        tags: Mapping[str, str] = ...
    ) -> SubmitJobResponseTypeDef:
        """
        Submits an Batch job from a job definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.submit_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#submit_job)
        """
    async def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Associates the specified tags to a resource with the specified `resourceArn`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#tag_resource)
        """
    async def terminate_job(self, *, jobId: str, reason: str) -> Dict[str, Any]:
        """
        Terminates a job in a job queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.terminate_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#terminate_job)
        """
    async def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Deletes specified tags from an Batch resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#untag_resource)
        """
    async def update_compute_environment(
        self,
        *,
        computeEnvironment: str,
        state: CEStateType = ...,
        unmanagedvCpus: int = ...,
        computeResources: "ComputeResourceUpdateTypeDef" = ...,
        serviceRole: str = ...
    ) -> UpdateComputeEnvironmentResponseTypeDef:
        """
        Updates an Batch compute environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.update_compute_environment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#update_compute_environment)
        """
    async def update_job_queue(
        self,
        *,
        jobQueue: str,
        state: JQStateType = ...,
        schedulingPolicyArn: str = ...,
        priority: int = ...,
        computeEnvironmentOrder: Sequence["ComputeEnvironmentOrderTypeDef"] = ...
    ) -> UpdateJobQueueResponseTypeDef:
        """
        Updates a job queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.update_job_queue)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#update_job_queue)
        """
    async def update_scheduling_policy(
        self, *, arn: str, fairsharePolicy: "FairsharePolicyTypeDef" = ...
    ) -> Dict[str, Any]:
        """
        Updates a scheduling policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.update_scheduling_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#update_scheduling_policy)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["describe_compute_environments"]
    ) -> DescribeComputeEnvironmentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["describe_job_definitions"]
    ) -> DescribeJobDefinitionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["describe_job_queues"]
    ) -> DescribeJobQueuesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#get_paginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_jobs"]) -> ListJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_scheduling_policies"]
    ) -> ListSchedulingPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/#get_paginator)
        """
    async def __aenter__(self) -> "BatchClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch.html#Batch.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/client/)
        """
