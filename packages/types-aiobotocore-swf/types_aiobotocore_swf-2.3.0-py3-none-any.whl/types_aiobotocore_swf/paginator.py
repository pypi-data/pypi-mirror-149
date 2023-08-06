"""
Type annotations for swf service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_swf.client import SWFClient
    from types_aiobotocore_swf.paginator import (
        GetWorkflowExecutionHistoryPaginator,
        ListActivityTypesPaginator,
        ListClosedWorkflowExecutionsPaginator,
        ListDomainsPaginator,
        ListOpenWorkflowExecutionsPaginator,
        ListWorkflowTypesPaginator,
        PollForDecisionTaskPaginator,
    )

    session = get_session()
    with session.create_client("swf") as client:
        client: SWFClient

        get_workflow_execution_history_paginator: GetWorkflowExecutionHistoryPaginator = client.get_paginator("get_workflow_execution_history")
        list_activity_types_paginator: ListActivityTypesPaginator = client.get_paginator("list_activity_types")
        list_closed_workflow_executions_paginator: ListClosedWorkflowExecutionsPaginator = client.get_paginator("list_closed_workflow_executions")
        list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
        list_open_workflow_executions_paginator: ListOpenWorkflowExecutionsPaginator = client.get_paginator("list_open_workflow_executions")
        list_workflow_types_paginator: ListWorkflowTypesPaginator = client.get_paginator("list_workflow_types")
        poll_for_decision_task_paginator: PollForDecisionTaskPaginator = client.get_paginator("poll_for_decision_task")
    ```
"""
import sys
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import RegistrationStatusType
from .type_defs import (
    ActivityTypeInfosTypeDef,
    CloseStatusFilterTypeDef,
    DecisionTaskTypeDef,
    DomainInfosTypeDef,
    ExecutionTimeFilterTypeDef,
    HistoryTypeDef,
    PaginatorConfigTypeDef,
    TagFilterTypeDef,
    TaskListTypeDef,
    WorkflowExecutionFilterTypeDef,
    WorkflowExecutionInfosTypeDef,
    WorkflowExecutionTypeDef,
    WorkflowTypeFilterTypeDef,
    WorkflowTypeInfosTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator


__all__ = (
    "GetWorkflowExecutionHistoryPaginator",
    "ListActivityTypesPaginator",
    "ListClosedWorkflowExecutionsPaginator",
    "ListDomainsPaginator",
    "ListOpenWorkflowExecutionsPaginator",
    "ListWorkflowTypesPaginator",
    "PollForDecisionTaskPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetWorkflowExecutionHistoryPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Paginator.GetWorkflowExecutionHistory)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#getworkflowexecutionhistorypaginator)
    """

    def paginate(
        self,
        *,
        domain: str,
        execution: "WorkflowExecutionTypeDef",
        reverseOrder: bool = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[HistoryTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Paginator.GetWorkflowExecutionHistory.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#getworkflowexecutionhistorypaginator)
        """


class ListActivityTypesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Paginator.ListActivityTypes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#listactivitytypespaginator)
    """

    def paginate(
        self,
        *,
        domain: str,
        registrationStatus: RegistrationStatusType,
        name: str = ...,
        reverseOrder: bool = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[ActivityTypeInfosTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Paginator.ListActivityTypes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#listactivitytypespaginator)
        """


class ListClosedWorkflowExecutionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Paginator.ListClosedWorkflowExecutions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#listclosedworkflowexecutionspaginator)
    """

    def paginate(
        self,
        *,
        domain: str,
        startTimeFilter: "ExecutionTimeFilterTypeDef" = ...,
        closeTimeFilter: "ExecutionTimeFilterTypeDef" = ...,
        executionFilter: "WorkflowExecutionFilterTypeDef" = ...,
        closeStatusFilter: "CloseStatusFilterTypeDef" = ...,
        typeFilter: "WorkflowTypeFilterTypeDef" = ...,
        tagFilter: "TagFilterTypeDef" = ...,
        reverseOrder: bool = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[WorkflowExecutionInfosTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Paginator.ListClosedWorkflowExecutions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#listclosedworkflowexecutionspaginator)
        """


class ListDomainsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Paginator.ListDomains)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#listdomainspaginator)
    """

    def paginate(
        self,
        *,
        registrationStatus: RegistrationStatusType,
        reverseOrder: bool = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DomainInfosTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Paginator.ListDomains.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#listdomainspaginator)
        """


class ListOpenWorkflowExecutionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Paginator.ListOpenWorkflowExecutions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#listopenworkflowexecutionspaginator)
    """

    def paginate(
        self,
        *,
        domain: str,
        startTimeFilter: "ExecutionTimeFilterTypeDef",
        typeFilter: "WorkflowTypeFilterTypeDef" = ...,
        tagFilter: "TagFilterTypeDef" = ...,
        reverseOrder: bool = ...,
        executionFilter: "WorkflowExecutionFilterTypeDef" = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[WorkflowExecutionInfosTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Paginator.ListOpenWorkflowExecutions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#listopenworkflowexecutionspaginator)
        """


class ListWorkflowTypesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Paginator.ListWorkflowTypes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#listworkflowtypespaginator)
    """

    def paginate(
        self,
        *,
        domain: str,
        registrationStatus: RegistrationStatusType,
        name: str = ...,
        reverseOrder: bool = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[WorkflowTypeInfosTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Paginator.ListWorkflowTypes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#listworkflowtypespaginator)
        """


class PollForDecisionTaskPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Paginator.PollForDecisionTask)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#pollfordecisiontaskpaginator)
    """

    def paginate(
        self,
        *,
        domain: str,
        taskList: "TaskListTypeDef",
        identity: str = ...,
        reverseOrder: bool = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> AsyncIterator[DecisionTaskTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Paginator.PollForDecisionTask.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#pollfordecisiontaskpaginator)
        """
