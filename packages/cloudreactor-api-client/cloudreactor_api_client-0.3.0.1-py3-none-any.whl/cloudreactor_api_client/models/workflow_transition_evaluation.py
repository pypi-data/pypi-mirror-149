import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.name_and_uuid import NameAndUuid
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowTransitionEvaluation")


@attr.s(auto_attribs=True)
class WorkflowTransitionEvaluation:
    """A WorkflowTransitionEvaluation is a saved evaluation of the conditions
    in a WorkflowTransition during a WorkflowExecution.

        Attributes:
            uuid (Union[Unset, str]):
            result (Union[Unset, bool]):
            workflow_transition (Union[Unset, NameAndUuid]): Identifies an entity in three ways: 1. UUID; 2. Name; and 3.
                URL.
                When used to indentify an entity in a request method body, only one of
                uuid and name needs to be specified. If both are present, they must
                refer to the same entity or else the response will be a 400 error.
            workflow_execution (Union[Unset, NameAndUuid]): Identifies an entity in three ways: 1. UUID; 2. Name; and 3.
                URL.
                When used to indentify an entity in a request method body, only one of
                uuid and name needs to be specified. If both are present, they must
                refer to the same entity or else the response will be a 400 error.
            from_workflow_task_instance_execution (Union[Unset, None, str]):
            evaluated_at (Union[Unset, datetime.datetime]):
    """

    uuid: Union[Unset, str] = UNSET
    result: Union[Unset, bool] = UNSET
    workflow_transition: Union[Unset, NameAndUuid] = UNSET
    workflow_execution: Union[Unset, NameAndUuid] = UNSET
    from_workflow_task_instance_execution: Union[Unset, None, str] = UNSET
    evaluated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        uuid = self.uuid
        result = self.result
        workflow_transition: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.workflow_transition, Unset):
            workflow_transition = self.workflow_transition.to_dict()

        workflow_execution: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.workflow_execution, Unset):
            workflow_execution = self.workflow_execution.to_dict()

        from_workflow_task_instance_execution = self.from_workflow_task_instance_execution
        evaluated_at: Union[Unset, str] = UNSET
        if not isinstance(self.evaluated_at, Unset):
            evaluated_at = self.evaluated_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if result is not UNSET:
            field_dict["result"] = result
        if workflow_transition is not UNSET:
            field_dict["workflow_transition"] = workflow_transition
        if workflow_execution is not UNSET:
            field_dict["workflow_execution"] = workflow_execution
        if from_workflow_task_instance_execution is not UNSET:
            field_dict["from_workflow_task_instance_execution"] = from_workflow_task_instance_execution
        if evaluated_at is not UNSET:
            field_dict["evaluated_at"] = evaluated_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        uuid = d.pop("uuid", UNSET)

        result = d.pop("result", UNSET)

        _workflow_transition = d.pop("workflow_transition", UNSET)
        workflow_transition: Union[Unset, NameAndUuid]
        if isinstance(_workflow_transition, Unset):
            workflow_transition = UNSET
        else:
            workflow_transition = NameAndUuid.from_dict(_workflow_transition)

        _workflow_execution = d.pop("workflow_execution", UNSET)
        workflow_execution: Union[Unset, NameAndUuid]
        if isinstance(_workflow_execution, Unset):
            workflow_execution = UNSET
        else:
            workflow_execution = NameAndUuid.from_dict(_workflow_execution)

        from_workflow_task_instance_execution = d.pop("from_workflow_task_instance_execution", UNSET)

        _evaluated_at = d.pop("evaluated_at", UNSET)
        evaluated_at: Union[Unset, datetime.datetime]
        if isinstance(_evaluated_at, Unset):
            evaluated_at = UNSET
        else:
            evaluated_at = isoparse(_evaluated_at)

        workflow_transition_evaluation = cls(
            uuid=uuid,
            result=result,
            workflow_transition=workflow_transition,
            workflow_execution=workflow_execution,
            from_workflow_task_instance_execution=from_workflow_task_instance_execution,
            evaluated_at=evaluated_at,
        )

        workflow_transition_evaluation.additional_properties = d
        return workflow_transition_evaluation

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
