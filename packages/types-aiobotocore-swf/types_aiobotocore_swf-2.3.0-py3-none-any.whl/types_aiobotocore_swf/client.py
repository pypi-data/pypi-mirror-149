"""
Type annotations for swf service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_swf.client import SWFClient

    session = get_session()
    async with session.create_client("swf") as client:
        client: SWFClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import ChildPolicyType, RegistrationStatusType
from .paginator import (
    GetWorkflowExecutionHistoryPaginator,
    ListActivityTypesPaginator,
    ListClosedWorkflowExecutionsPaginator,
    ListDomainsPaginator,
    ListOpenWorkflowExecutionsPaginator,
    ListWorkflowTypesPaginator,
    PollForDecisionTaskPaginator,
)
from .type_defs import (
    ActivityTaskStatusTypeDef,
    ActivityTaskTypeDef,
    ActivityTypeDetailTypeDef,
    ActivityTypeInfosTypeDef,
    ActivityTypeTypeDef,
    CloseStatusFilterTypeDef,
    DecisionTaskTypeDef,
    DecisionTypeDef,
    DomainDetailTypeDef,
    DomainInfosTypeDef,
    ExecutionTimeFilterTypeDef,
    HistoryTypeDef,
    ListTagsForResourceOutputTypeDef,
    PendingTaskCountTypeDef,
    ResourceTagTypeDef,
    RunTypeDef,
    TagFilterTypeDef,
    TaskListTypeDef,
    WorkflowExecutionCountTypeDef,
    WorkflowExecutionDetailTypeDef,
    WorkflowExecutionFilterTypeDef,
    WorkflowExecutionInfosTypeDef,
    WorkflowExecutionTypeDef,
    WorkflowTypeDetailTypeDef,
    WorkflowTypeFilterTypeDef,
    WorkflowTypeInfosTypeDef,
    WorkflowTypeTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("SWFClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    DefaultUndefinedFault: Type[BotocoreClientError]
    DomainAlreadyExistsFault: Type[BotocoreClientError]
    DomainDeprecatedFault: Type[BotocoreClientError]
    LimitExceededFault: Type[BotocoreClientError]
    OperationNotPermittedFault: Type[BotocoreClientError]
    TooManyTagsFault: Type[BotocoreClientError]
    TypeAlreadyExistsFault: Type[BotocoreClientError]
    TypeDeprecatedFault: Type[BotocoreClientError]
    UnknownResourceFault: Type[BotocoreClientError]
    WorkflowExecutionAlreadyStartedFault: Type[BotocoreClientError]


class SWFClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SWFClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#can_paginate)
        """

    async def count_closed_workflow_executions(
        self,
        *,
        domain: str,
        startTimeFilter: "ExecutionTimeFilterTypeDef" = ...,
        closeTimeFilter: "ExecutionTimeFilterTypeDef" = ...,
        executionFilter: "WorkflowExecutionFilterTypeDef" = ...,
        typeFilter: "WorkflowTypeFilterTypeDef" = ...,
        tagFilter: "TagFilterTypeDef" = ...,
        closeStatusFilter: "CloseStatusFilterTypeDef" = ...
    ) -> WorkflowExecutionCountTypeDef:
        """
        Returns the number of closed workflow executions within the given domain that
        meet the specified filtering criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.count_closed_workflow_executions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#count_closed_workflow_executions)
        """

    async def count_open_workflow_executions(
        self,
        *,
        domain: str,
        startTimeFilter: "ExecutionTimeFilterTypeDef",
        typeFilter: "WorkflowTypeFilterTypeDef" = ...,
        tagFilter: "TagFilterTypeDef" = ...,
        executionFilter: "WorkflowExecutionFilterTypeDef" = ...
    ) -> WorkflowExecutionCountTypeDef:
        """
        Returns the number of open workflow executions within the given domain that meet
        the specified filtering criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.count_open_workflow_executions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#count_open_workflow_executions)
        """

    async def count_pending_activity_tasks(
        self, *, domain: str, taskList: "TaskListTypeDef"
    ) -> PendingTaskCountTypeDef:
        """
        Returns the estimated number of activity tasks in the specified task list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.count_pending_activity_tasks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#count_pending_activity_tasks)
        """

    async def count_pending_decision_tasks(
        self, *, domain: str, taskList: "TaskListTypeDef"
    ) -> PendingTaskCountTypeDef:
        """
        Returns the estimated number of decision tasks in the specified task list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.count_pending_decision_tasks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#count_pending_decision_tasks)
        """

    async def deprecate_activity_type(
        self, *, domain: str, activityType: "ActivityTypeTypeDef"
    ) -> None:
        """
        Deprecates the specified *activity type*.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.deprecate_activity_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#deprecate_activity_type)
        """

    async def deprecate_domain(self, *, name: str) -> None:
        """
        Deprecates the specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.deprecate_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#deprecate_domain)
        """

    async def deprecate_workflow_type(
        self, *, domain: str, workflowType: "WorkflowTypeTypeDef"
    ) -> None:
        """
        Deprecates the specified *workflow type*.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.deprecate_workflow_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#deprecate_workflow_type)
        """

    async def describe_activity_type(
        self, *, domain: str, activityType: "ActivityTypeTypeDef"
    ) -> ActivityTypeDetailTypeDef:
        """
        Returns information about the specified activity type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.describe_activity_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#describe_activity_type)
        """

    async def describe_domain(self, *, name: str) -> DomainDetailTypeDef:
        """
        Returns information about the specified domain, including description and
        status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.describe_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#describe_domain)
        """

    async def describe_workflow_execution(
        self, *, domain: str, execution: "WorkflowExecutionTypeDef"
    ) -> WorkflowExecutionDetailTypeDef:
        """
        Returns information about the specified workflow execution including its type
        and some statistics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.describe_workflow_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#describe_workflow_execution)
        """

    async def describe_workflow_type(
        self, *, domain: str, workflowType: "WorkflowTypeTypeDef"
    ) -> WorkflowTypeDetailTypeDef:
        """
        Returns information about the specified *workflow type*.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.describe_workflow_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#describe_workflow_type)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#generate_presigned_url)
        """

    async def get_workflow_execution_history(
        self,
        *,
        domain: str,
        execution: "WorkflowExecutionTypeDef",
        nextPageToken: str = ...,
        maximumPageSize: int = ...,
        reverseOrder: bool = ...
    ) -> HistoryTypeDef:
        """
        Returns the history of the specified workflow execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.get_workflow_execution_history)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#get_workflow_execution_history)
        """

    async def list_activity_types(
        self,
        *,
        domain: str,
        registrationStatus: RegistrationStatusType,
        name: str = ...,
        nextPageToken: str = ...,
        maximumPageSize: int = ...,
        reverseOrder: bool = ...
    ) -> ActivityTypeInfosTypeDef:
        """
        Returns information about all activities registered in the specified domain that
        match the specified name and registration status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.list_activity_types)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#list_activity_types)
        """

    async def list_closed_workflow_executions(
        self,
        *,
        domain: str,
        startTimeFilter: "ExecutionTimeFilterTypeDef" = ...,
        closeTimeFilter: "ExecutionTimeFilterTypeDef" = ...,
        executionFilter: "WorkflowExecutionFilterTypeDef" = ...,
        closeStatusFilter: "CloseStatusFilterTypeDef" = ...,
        typeFilter: "WorkflowTypeFilterTypeDef" = ...,
        tagFilter: "TagFilterTypeDef" = ...,
        nextPageToken: str = ...,
        maximumPageSize: int = ...,
        reverseOrder: bool = ...
    ) -> WorkflowExecutionInfosTypeDef:
        """
        Returns a list of closed workflow executions in the specified domain that meet
        the filtering criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.list_closed_workflow_executions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#list_closed_workflow_executions)
        """

    async def list_domains(
        self,
        *,
        registrationStatus: RegistrationStatusType,
        nextPageToken: str = ...,
        maximumPageSize: int = ...,
        reverseOrder: bool = ...
    ) -> DomainInfosTypeDef:
        """
        Returns the list of domains registered in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.list_domains)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#list_domains)
        """

    async def list_open_workflow_executions(
        self,
        *,
        domain: str,
        startTimeFilter: "ExecutionTimeFilterTypeDef",
        typeFilter: "WorkflowTypeFilterTypeDef" = ...,
        tagFilter: "TagFilterTypeDef" = ...,
        nextPageToken: str = ...,
        maximumPageSize: int = ...,
        reverseOrder: bool = ...,
        executionFilter: "WorkflowExecutionFilterTypeDef" = ...
    ) -> WorkflowExecutionInfosTypeDef:
        """
        Returns a list of open workflow executions in the specified domain that meet the
        filtering criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.list_open_workflow_executions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#list_open_workflow_executions)
        """

    async def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceOutputTypeDef:
        """
        List tags for a given domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#list_tags_for_resource)
        """

    async def list_workflow_types(
        self,
        *,
        domain: str,
        registrationStatus: RegistrationStatusType,
        name: str = ...,
        nextPageToken: str = ...,
        maximumPageSize: int = ...,
        reverseOrder: bool = ...
    ) -> WorkflowTypeInfosTypeDef:
        """
        Returns information about workflow types in the specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.list_workflow_types)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#list_workflow_types)
        """

    async def poll_for_activity_task(
        self, *, domain: str, taskList: "TaskListTypeDef", identity: str = ...
    ) -> ActivityTaskTypeDef:
        """
        Used by workers to get an  ActivityTask from the specified activity `taskList`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.poll_for_activity_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#poll_for_activity_task)
        """

    async def poll_for_decision_task(
        self,
        *,
        domain: str,
        taskList: "TaskListTypeDef",
        identity: str = ...,
        nextPageToken: str = ...,
        maximumPageSize: int = ...,
        reverseOrder: bool = ...
    ) -> DecisionTaskTypeDef:
        """
        Used by deciders to get a  DecisionTask from the specified decision `taskList`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.poll_for_decision_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#poll_for_decision_task)
        """

    async def record_activity_task_heartbeat(
        self, *, taskToken: str, details: str = ...
    ) -> ActivityTaskStatusTypeDef:
        """
        Used by activity workers to report to the service that the  ActivityTask
        represented by the specified `taskToken` is still making progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.record_activity_task_heartbeat)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#record_activity_task_heartbeat)
        """

    async def register_activity_type(
        self,
        *,
        domain: str,
        name: str,
        version: str,
        description: str = ...,
        defaultTaskStartToCloseTimeout: str = ...,
        defaultTaskHeartbeatTimeout: str = ...,
        defaultTaskList: "TaskListTypeDef" = ...,
        defaultTaskPriority: str = ...,
        defaultTaskScheduleToStartTimeout: str = ...,
        defaultTaskScheduleToCloseTimeout: str = ...
    ) -> None:
        """
        Registers a new *activity type* along with its configuration settings in the
        specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.register_activity_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#register_activity_type)
        """

    async def register_domain(
        self,
        *,
        name: str,
        workflowExecutionRetentionPeriodInDays: str,
        description: str = ...,
        tags: Sequence["ResourceTagTypeDef"] = ...
    ) -> None:
        """
        Registers a new domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.register_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#register_domain)
        """

    async def register_workflow_type(
        self,
        *,
        domain: str,
        name: str,
        version: str,
        description: str = ...,
        defaultTaskStartToCloseTimeout: str = ...,
        defaultExecutionStartToCloseTimeout: str = ...,
        defaultTaskList: "TaskListTypeDef" = ...,
        defaultTaskPriority: str = ...,
        defaultChildPolicy: ChildPolicyType = ...,
        defaultLambdaRole: str = ...
    ) -> None:
        """
        Registers a new *workflow type* and its configuration settings in the specified
        domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.register_workflow_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#register_workflow_type)
        """

    async def request_cancel_workflow_execution(
        self, *, domain: str, workflowId: str, runId: str = ...
    ) -> None:
        """
        Records a `WorkflowExecutionCancelRequested` event in the currently running
        workflow execution identified by the given domain, workflowId, and runId.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.request_cancel_workflow_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#request_cancel_workflow_execution)
        """

    async def respond_activity_task_canceled(self, *, taskToken: str, details: str = ...) -> None:
        """
        Used by workers to tell the service that the  ActivityTask identified by the
        `taskToken` was successfully canceled.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.respond_activity_task_canceled)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#respond_activity_task_canceled)
        """

    async def respond_activity_task_completed(self, *, taskToken: str, result: str = ...) -> None:
        """
        Used by workers to tell the service that the  ActivityTask identified by the
        `taskToken` completed successfully with a `result` (if provided).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.respond_activity_task_completed)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#respond_activity_task_completed)
        """

    async def respond_activity_task_failed(
        self, *, taskToken: str, reason: str = ..., details: str = ...
    ) -> None:
        """
        Used by workers to tell the service that the  ActivityTask identified by the
        `taskToken` has failed with `reason` (if specified).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.respond_activity_task_failed)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#respond_activity_task_failed)
        """

    async def respond_decision_task_completed(
        self,
        *,
        taskToken: str,
        decisions: Sequence["DecisionTypeDef"] = ...,
        executionContext: str = ...
    ) -> None:
        """
        Used by deciders to tell the service that the  DecisionTask identified by the
        `taskToken` has successfully completed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.respond_decision_task_completed)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#respond_decision_task_completed)
        """

    async def signal_workflow_execution(
        self, *, domain: str, workflowId: str, signalName: str, runId: str = ..., input: str = ...
    ) -> None:
        """
        Records a `WorkflowExecutionSignaled` event in the workflow execution history
        and creates a decision task for the workflow execution identified by the given
        domain, workflowId and runId.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.signal_workflow_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#signal_workflow_execution)
        """

    async def start_workflow_execution(
        self,
        *,
        domain: str,
        workflowId: str,
        workflowType: "WorkflowTypeTypeDef",
        taskList: "TaskListTypeDef" = ...,
        taskPriority: str = ...,
        input: str = ...,
        executionStartToCloseTimeout: str = ...,
        tagList: Sequence[str] = ...,
        taskStartToCloseTimeout: str = ...,
        childPolicy: ChildPolicyType = ...,
        lambdaRole: str = ...
    ) -> RunTypeDef:
        """
        Starts an execution of the workflow type in the specified domain using the
        provided `workflowId` and input data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.start_workflow_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#start_workflow_execution)
        """

    async def tag_resource(self, *, resourceArn: str, tags: Sequence["ResourceTagTypeDef"]) -> None:
        """
        Add a tag to a Amazon SWF domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#tag_resource)
        """

    async def terminate_workflow_execution(
        self,
        *,
        domain: str,
        workflowId: str,
        runId: str = ...,
        reason: str = ...,
        details: str = ...,
        childPolicy: ChildPolicyType = ...
    ) -> None:
        """
        Records a `WorkflowExecutionTerminated` event and forces closure of the workflow
        execution identified by the given domain, runId, and workflowId.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.terminate_workflow_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#terminate_workflow_execution)
        """

    async def undeprecate_activity_type(
        self, *, domain: str, activityType: "ActivityTypeTypeDef"
    ) -> None:
        """
        Undeprecates a previously deprecated *activity type*.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.undeprecate_activity_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#undeprecate_activity_type)
        """

    async def undeprecate_domain(self, *, name: str) -> None:
        """
        Undeprecates a previously deprecated domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.undeprecate_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#undeprecate_domain)
        """

    async def undeprecate_workflow_type(
        self, *, domain: str, workflowType: "WorkflowTypeTypeDef"
    ) -> None:
        """
        Undeprecates a previously deprecated *workflow type*.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.undeprecate_workflow_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#undeprecate_workflow_type)
        """

    async def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> None:
        """
        Remove a tag from a Amazon SWF domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#untag_resource)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_workflow_execution_history"]
    ) -> GetWorkflowExecutionHistoryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_activity_types"]
    ) -> ListActivityTypesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_closed_workflow_executions"]
    ) -> ListClosedWorkflowExecutionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_domains"]) -> ListDomainsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_open_workflow_executions"]
    ) -> ListOpenWorkflowExecutionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_workflow_types"]
    ) -> ListWorkflowTypesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["poll_for_decision_task"]
    ) -> PollForDecisionTaskPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#get_paginator)
        """

    async def __aenter__(self) -> "SWFClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/)
        """
