"""
Type annotations for stepfunctions service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_stepfunctions.client import SFNClient

    session = get_session()
    async with session.create_client("stepfunctions") as client:
        client: SFNClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import ExecutionStatusType, StateMachineTypeType
from .paginator import (
    GetExecutionHistoryPaginator,
    ListActivitiesPaginator,
    ListExecutionsPaginator,
    ListStateMachinesPaginator,
)
from .type_defs import (
    CreateActivityOutputTypeDef,
    CreateStateMachineOutputTypeDef,
    DescribeActivityOutputTypeDef,
    DescribeExecutionOutputTypeDef,
    DescribeStateMachineForExecutionOutputTypeDef,
    DescribeStateMachineOutputTypeDef,
    GetActivityTaskOutputTypeDef,
    GetExecutionHistoryOutputTypeDef,
    ListActivitiesOutputTypeDef,
    ListExecutionsOutputTypeDef,
    ListStateMachinesOutputTypeDef,
    ListTagsForResourceOutputTypeDef,
    LoggingConfigurationTypeDef,
    StartExecutionOutputTypeDef,
    StartSyncExecutionOutputTypeDef,
    StopExecutionOutputTypeDef,
    TagTypeDef,
    TracingConfigurationTypeDef,
    UpdateStateMachineOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("SFNClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ActivityDoesNotExist: Type[BotocoreClientError]
    ActivityLimitExceeded: Type[BotocoreClientError]
    ActivityWorkerLimitExceeded: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ExecutionAlreadyExists: Type[BotocoreClientError]
    ExecutionDoesNotExist: Type[BotocoreClientError]
    ExecutionLimitExceeded: Type[BotocoreClientError]
    InvalidArn: Type[BotocoreClientError]
    InvalidDefinition: Type[BotocoreClientError]
    InvalidExecutionInput: Type[BotocoreClientError]
    InvalidLoggingConfiguration: Type[BotocoreClientError]
    InvalidName: Type[BotocoreClientError]
    InvalidOutput: Type[BotocoreClientError]
    InvalidToken: Type[BotocoreClientError]
    InvalidTracingConfiguration: Type[BotocoreClientError]
    MissingRequiredParameter: Type[BotocoreClientError]
    ResourceNotFound: Type[BotocoreClientError]
    StateMachineAlreadyExists: Type[BotocoreClientError]
    StateMachineDeleting: Type[BotocoreClientError]
    StateMachineDoesNotExist: Type[BotocoreClientError]
    StateMachineLimitExceeded: Type[BotocoreClientError]
    StateMachineTypeNotSupported: Type[BotocoreClientError]
    TaskDoesNotExist: Type[BotocoreClientError]
    TaskTimedOut: Type[BotocoreClientError]
    TooManyTags: Type[BotocoreClientError]


class SFNClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SFNClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/#can_paginate)
        """

    async def create_activity(
        self, *, name: str, tags: Sequence["TagTypeDef"] = ...
    ) -> CreateActivityOutputTypeDef:
        """
        Creates an activity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.create_activity)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/#create_activity)
        """

    async def create_state_machine(
        self,
        *,
        name: str,
        definition: str,
        roleArn: str,
        type: StateMachineTypeType = ...,
        loggingConfiguration: "LoggingConfigurationTypeDef" = ...,
        tags: Sequence["TagTypeDef"] = ...,
        tracingConfiguration: "TracingConfigurationTypeDef" = ...
    ) -> CreateStateMachineOutputTypeDef:
        """
        Creates a state machine.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.create_state_machine)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/#create_state_machine)
        """

    async def delete_activity(self, *, activityArn: str) -> Dict[str, Any]:
        """
        Deletes an activity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.delete_activity)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/#delete_activity)
        """

    async def delete_state_machine(self, *, stateMachineArn: str) -> Dict[str, Any]:
        """
        Deletes a state machine.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.delete_state_machine)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/#delete_state_machine)
        """

    async def describe_activity(self, *, activityArn: str) -> DescribeActivityOutputTypeDef:
        """
        Describes an activity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.describe_activity)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/#describe_activity)
        """

    async def describe_execution(self, *, executionArn: str) -> DescribeExecutionOutputTypeDef:
        """
        Describes an execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.describe_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/#describe_execution)
        """

    async def describe_state_machine(
        self, *, stateMachineArn: str
    ) -> DescribeStateMachineOutputTypeDef:
        """
        Describes a state machine.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.describe_state_machine)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/#describe_state_machine)
        """

    async def describe_state_machine_for_execution(
        self, *, executionArn: str
    ) -> DescribeStateMachineForExecutionOutputTypeDef:
        """
        Describes the state machine associated with a specific execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.describe_state_machine_for_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/#describe_state_machine_for_execution)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/#generate_presigned_url)
        """

    async def get_activity_task(
        self, *, activityArn: str, workerName: str = ...
    ) -> GetActivityTaskOutputTypeDef:
        """
        Used by workers to retrieve a task (with the specified activity ARN) which has
        been scheduled for execution by a running state machine.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.get_activity_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/#get_activity_task)
        """

    async def get_execution_history(
        self,
        *,
        executionArn: str,
        maxResults: int = ...,
        reverseOrder: bool = ...,
        nextToken: str = ...,
        includeExecutionData: bool = ...
    ) -> GetExecutionHistoryOutputTypeDef:
        """
        Returns the history of the specified execution as a list of events.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.get_execution_history)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/#get_execution_history)
        """

    async def list_activities(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListActivitiesOutputTypeDef:
        """
        Lists the existing activities.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.list_activities)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/#list_activities)
        """

    async def list_executions(
        self,
        *,
        stateMachineArn: str,
        statusFilter: ExecutionStatusType = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListExecutionsOutputTypeDef:
        """
        Lists the executions of a state machine that meet the filtering criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.list_executions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/#list_executions)
        """

    async def list_state_machines(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListStateMachinesOutputTypeDef:
        """
        Lists the existing state machines.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.list_state_machines)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/#list_state_machines)
        """

    async def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceOutputTypeDef:
        """
        List tags for a given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/#list_tags_for_resource)
        """

    async def send_task_failure(
        self, *, taskToken: str, error: str = ..., cause: str = ...
    ) -> Dict[str, Any]:
        """
        Used by activity workers and task states using the
        [callback](https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-
        resource.html#connect-wait-token)_ pattern to report that the task identified by
        the `taskToken` failed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.send_task_failure)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/#send_task_failure)
        """

    async def send_task_heartbeat(self, *, taskToken: str) -> Dict[str, Any]:
        """
        Used by activity workers and task states using the
        [callback](https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-
        resource.html#connect-wait-token)_ pattern to report to Step Functions that the
        task represented by the specified `taskToken` is still making progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.send_task_heartbeat)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/#send_task_heartbeat)
        """

    async def send_task_success(self, *, taskToken: str, output: str) -> Dict[str, Any]:
        """
        Used by activity workers and task states using the
        [callback](https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-
        resource.html#connect-wait-token)_ pattern to report that the task identified by
        the `taskToken` completed successfully.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.send_task_success)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/#send_task_success)
        """

    async def start_execution(
        self, *, stateMachineArn: str, name: str = ..., input: str = ..., traceHeader: str = ...
    ) -> StartExecutionOutputTypeDef:
        """
        Starts a state machine execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.start_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/#start_execution)
        """

    async def start_sync_execution(
        self, *, stateMachineArn: str, name: str = ..., input: str = ..., traceHeader: str = ...
    ) -> StartSyncExecutionOutputTypeDef:
        """
        Starts a Synchronous Express state machine execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.start_sync_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/#start_sync_execution)
        """

    async def stop_execution(
        self, *, executionArn: str, error: str = ..., cause: str = ...
    ) -> StopExecutionOutputTypeDef:
        """
        Stops an execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.stop_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/#stop_execution)
        """

    async def tag_resource(
        self, *, resourceArn: str, tags: Sequence["TagTypeDef"]
    ) -> Dict[str, Any]:
        """
        Add a tag to a Step Functions resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/#tag_resource)
        """

    async def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Remove a tag from a Step Functions resource See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/states-2016-11-23/UntagResource).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/#untag_resource)
        """

    async def update_state_machine(
        self,
        *,
        stateMachineArn: str,
        definition: str = ...,
        roleArn: str = ...,
        loggingConfiguration: "LoggingConfigurationTypeDef" = ...,
        tracingConfiguration: "TracingConfigurationTypeDef" = ...
    ) -> UpdateStateMachineOutputTypeDef:
        """
        Updates an existing state machine by modifying its `definition` , `roleArn` , or
        `loggingConfiguration`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.update_state_machine)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/#update_state_machine)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_execution_history"]
    ) -> GetExecutionHistoryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_activities"]) -> ListActivitiesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_executions"]) -> ListExecutionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_state_machines"]
    ) -> ListStateMachinesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/#get_paginator)
        """

    async def __aenter__(self) -> "SFNClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/client/)
        """
