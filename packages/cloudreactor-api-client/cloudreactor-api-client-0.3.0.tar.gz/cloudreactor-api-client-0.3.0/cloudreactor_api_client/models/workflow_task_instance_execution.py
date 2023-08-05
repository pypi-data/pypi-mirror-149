import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.name_and_uuid import NameAndUuid
from ..models.task_execution import TaskExecution
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowTaskInstanceExecution")


@attr.s(auto_attribs=True)
class WorkflowTaskInstanceExecution:
    """WorkflowTaskInstanceExecutions hold the execution information
    for a WorkflowTaskInstance (which holds a Task) for a specific
    WorkflowExection (run of a Workflow).

        Attributes:
            uuid (Union[Unset, str]):
            workflow_execution (Union[Unset, NameAndUuid]): Identifies an entity in three ways: 1. UUID; 2. Name; and 3.
                URL.
                When used to indentify an entity in a request method body, only one of
                uuid and name needs to be specified. If both are present, they must
                refer to the same entity or else the response will be a 400 error.
            workflow_task_instance (Union[Unset, NameAndUuid]): Identifies an entity in three ways: 1. UUID; 2. Name; and 3.
                URL.
                When used to indentify an entity in a request method body, only one of
                uuid and name needs to be specified. If both are present, they must
                refer to the same entity or else the response will be a 400 error.
            task_execution (Union[Unset, TaskExecution]): A Task Execution is an execution / run instance of a Task.
            is_latest (Union[Unset, bool]):
            created_at (Union[Unset, datetime.datetime]):
    """

    uuid: Union[Unset, str] = UNSET
    workflow_execution: Union[Unset, NameAndUuid] = UNSET
    workflow_task_instance: Union[Unset, NameAndUuid] = UNSET
    task_execution: Union[Unset, TaskExecution] = UNSET
    is_latest: Union[Unset, bool] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        uuid = self.uuid
        workflow_execution: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.workflow_execution, Unset):
            workflow_execution = self.workflow_execution.to_dict()

        workflow_task_instance: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.workflow_task_instance, Unset):
            workflow_task_instance = self.workflow_task_instance.to_dict()

        task_execution: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.task_execution, Unset):
            task_execution = self.task_execution.to_dict()

        is_latest = self.is_latest
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if workflow_execution is not UNSET:
            field_dict["workflow_execution"] = workflow_execution
        if workflow_task_instance is not UNSET:
            field_dict["workflow_task_instance"] = workflow_task_instance
        if task_execution is not UNSET:
            field_dict["task_execution"] = task_execution
        if is_latest is not UNSET:
            field_dict["is_latest"] = is_latest
        if created_at is not UNSET:
            field_dict["created_at"] = created_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        uuid = d.pop("uuid", UNSET)

        _workflow_execution = d.pop("workflow_execution", UNSET)
        workflow_execution: Union[Unset, NameAndUuid]
        if isinstance(_workflow_execution, Unset):
            workflow_execution = UNSET
        else:
            workflow_execution = NameAndUuid.from_dict(_workflow_execution)

        _workflow_task_instance = d.pop("workflow_task_instance", UNSET)
        workflow_task_instance: Union[Unset, NameAndUuid]
        if isinstance(_workflow_task_instance, Unset):
            workflow_task_instance = UNSET
        else:
            workflow_task_instance = NameAndUuid.from_dict(_workflow_task_instance)

        _task_execution = d.pop("task_execution", UNSET)
        task_execution: Union[Unset, TaskExecution]
        if isinstance(_task_execution, Unset):
            task_execution = UNSET
        else:
            task_execution = TaskExecution.from_dict(_task_execution)

        is_latest = d.pop("is_latest", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        workflow_task_instance_execution = cls(
            uuid=uuid,
            workflow_execution=workflow_execution,
            workflow_task_instance=workflow_task_instance,
            task_execution=task_execution,
            is_latest=is_latest,
            created_at=created_at,
        )

        workflow_task_instance_execution.additional_properties = d
        return workflow_task_instance_execution

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
