import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.failure_behavior_enum import FailureBehaviorEnum
from ..models.name_and_uuid import NameAndUuid
from ..models.patched_workflow_task_instance_environment_variables_overrides import (
    PatchedWorkflowTaskInstanceEnvironmentVariablesOverrides,
)
from ..models.start_transition_condition_enum import StartTransitionConditionEnum
from ..models.timeout_behavior_enum import TimeoutBehaviorEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedWorkflowTaskInstance")


@attr.s(auto_attribs=True)
class PatchedWorkflowTaskInstance:
    """A WorkflowTaskInstance contains a Task that is configured to run in
    a Workflow.

        Attributes:
            url (Union[Unset, str]):
            uuid (Union[Unset, str]):
            name (Union[Unset, str]):
            description (Union[Unset, str]):
            workflow (Union[Unset, NameAndUuid]): Identifies an entity in three ways: 1. UUID; 2. Name; and 3. URL.
                When used to indentify an entity in a request method body, only one of
                uuid and name needs to be specified. If both are present, they must
                refer to the same entity or else the response will be a 400 error.
            task (Union[Unset, NameAndUuid]): Identifies an entity in three ways: 1. UUID; 2. Name; and 3. URL.
                When used to indentify an entity in a request method body, only one of
                uuid and name needs to be specified. If both are present, they must
                refer to the same entity or else the response will be a 400 error.
            start_transition_condition (Union[Unset, StartTransitionConditionEnum]):
            max_complete_executions (Union[Unset, None, int]):
            should_eval_transitions_after_first_execution (Union[Unset, bool]):
            condition_count_threshold (Union[Unset, None, int]):
            condition_ratio_threshold (Union[Unset, None, float]):
            max_age_seconds (Union[Unset, None, int]):
            default_max_retries (Union[Unset, int]):
            failure_behavior (Union[Unset, FailureBehaviorEnum]):
            allow_workflow_execution_after_failure (Union[Unset, bool]):
            timeout_behavior (Union[Unset, TimeoutBehaviorEnum]):
            allow_workflow_execution_after_timeout (Union[Unset, bool]):
            environment_variables_overrides (Union[Unset, None, PatchedWorkflowTaskInstanceEnvironmentVariablesOverrides]):
            allocated_cpu_units (Union[Unset, None, int]):
            allocated_memory_mb (Union[Unset, None, int]):
            use_task_alert_methods (Union[Unset, bool]):
            ui_color (Union[Unset, str]):
            ui_icon_type (Union[Unset, str]):
            ui_scale (Union[Unset, None, float]):
            ui_center_margin_top (Union[Unset, None, float]):
            ui_center_margin_left (Union[Unset, None, float]):
            created_at (Union[Unset, datetime.datetime]):
            updated_at (Union[Unset, datetime.datetime]):
    """

    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    workflow: Union[Unset, NameAndUuid] = UNSET
    task: Union[Unset, NameAndUuid] = UNSET
    start_transition_condition: Union[Unset, StartTransitionConditionEnum] = UNSET
    max_complete_executions: Union[Unset, None, int] = UNSET
    should_eval_transitions_after_first_execution: Union[Unset, bool] = UNSET
    condition_count_threshold: Union[Unset, None, int] = UNSET
    condition_ratio_threshold: Union[Unset, None, float] = UNSET
    max_age_seconds: Union[Unset, None, int] = UNSET
    default_max_retries: Union[Unset, int] = UNSET
    failure_behavior: Union[Unset, FailureBehaviorEnum] = UNSET
    allow_workflow_execution_after_failure: Union[Unset, bool] = UNSET
    timeout_behavior: Union[Unset, TimeoutBehaviorEnum] = UNSET
    allow_workflow_execution_after_timeout: Union[Unset, bool] = UNSET
    environment_variables_overrides: Union[
        Unset, None, PatchedWorkflowTaskInstanceEnvironmentVariablesOverrides
    ] = UNSET
    allocated_cpu_units: Union[Unset, None, int] = UNSET
    allocated_memory_mb: Union[Unset, None, int] = UNSET
    use_task_alert_methods: Union[Unset, bool] = UNSET
    ui_color: Union[Unset, str] = UNSET
    ui_icon_type: Union[Unset, str] = UNSET
    ui_scale: Union[Unset, None, float] = UNSET
    ui_center_margin_top: Union[Unset, None, float] = UNSET
    ui_center_margin_left: Union[Unset, None, float] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        url = self.url
        uuid = self.uuid
        name = self.name
        description = self.description
        workflow: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.workflow, Unset):
            workflow = self.workflow.to_dict()

        task: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.task, Unset):
            task = self.task.to_dict()

        start_transition_condition: Union[Unset, str] = UNSET
        if not isinstance(self.start_transition_condition, Unset):
            start_transition_condition = self.start_transition_condition.value

        max_complete_executions = self.max_complete_executions
        should_eval_transitions_after_first_execution = self.should_eval_transitions_after_first_execution
        condition_count_threshold = self.condition_count_threshold
        condition_ratio_threshold = self.condition_ratio_threshold
        max_age_seconds = self.max_age_seconds
        default_max_retries = self.default_max_retries
        failure_behavior: Union[Unset, str] = UNSET
        if not isinstance(self.failure_behavior, Unset):
            failure_behavior = self.failure_behavior.value

        allow_workflow_execution_after_failure = self.allow_workflow_execution_after_failure
        timeout_behavior: Union[Unset, str] = UNSET
        if not isinstance(self.timeout_behavior, Unset):
            timeout_behavior = self.timeout_behavior.value

        allow_workflow_execution_after_timeout = self.allow_workflow_execution_after_timeout
        environment_variables_overrides: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.environment_variables_overrides, Unset):
            environment_variables_overrides = (
                self.environment_variables_overrides.to_dict() if self.environment_variables_overrides else None
            )

        allocated_cpu_units = self.allocated_cpu_units
        allocated_memory_mb = self.allocated_memory_mb
        use_task_alert_methods = self.use_task_alert_methods
        ui_color = self.ui_color
        ui_icon_type = self.ui_icon_type
        ui_scale = self.ui_scale
        ui_center_margin_top = self.ui_center_margin_top
        ui_center_margin_left = self.ui_center_margin_left
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if workflow is not UNSET:
            field_dict["workflow"] = workflow
        if task is not UNSET:
            field_dict["task"] = task
        if start_transition_condition is not UNSET:
            field_dict["start_transition_condition"] = start_transition_condition
        if max_complete_executions is not UNSET:
            field_dict["max_complete_executions"] = max_complete_executions
        if should_eval_transitions_after_first_execution is not UNSET:
            field_dict["should_eval_transitions_after_first_execution"] = should_eval_transitions_after_first_execution
        if condition_count_threshold is not UNSET:
            field_dict["condition_count_threshold"] = condition_count_threshold
        if condition_ratio_threshold is not UNSET:
            field_dict["condition_ratio_threshold"] = condition_ratio_threshold
        if max_age_seconds is not UNSET:
            field_dict["max_age_seconds"] = max_age_seconds
        if default_max_retries is not UNSET:
            field_dict["default_max_retries"] = default_max_retries
        if failure_behavior is not UNSET:
            field_dict["failure_behavior"] = failure_behavior
        if allow_workflow_execution_after_failure is not UNSET:
            field_dict["allow_workflow_execution_after_failure"] = allow_workflow_execution_after_failure
        if timeout_behavior is not UNSET:
            field_dict["timeout_behavior"] = timeout_behavior
        if allow_workflow_execution_after_timeout is not UNSET:
            field_dict["allow_workflow_execution_after_timeout"] = allow_workflow_execution_after_timeout
        if environment_variables_overrides is not UNSET:
            field_dict["environment_variables_overrides"] = environment_variables_overrides
        if allocated_cpu_units is not UNSET:
            field_dict["allocated_cpu_units"] = allocated_cpu_units
        if allocated_memory_mb is not UNSET:
            field_dict["allocated_memory_mb"] = allocated_memory_mb
        if use_task_alert_methods is not UNSET:
            field_dict["use_task_alert_methods"] = use_task_alert_methods
        if ui_color is not UNSET:
            field_dict["ui_color"] = ui_color
        if ui_icon_type is not UNSET:
            field_dict["ui_icon_type"] = ui_icon_type
        if ui_scale is not UNSET:
            field_dict["ui_scale"] = ui_scale
        if ui_center_margin_top is not UNSET:
            field_dict["ui_center_margin_top"] = ui_center_margin_top
        if ui_center_margin_left is not UNSET:
            field_dict["ui_center_margin_left"] = ui_center_margin_left
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        url = d.pop("url", UNSET)

        uuid = d.pop("uuid", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        _workflow = d.pop("workflow", UNSET)
        workflow: Union[Unset, NameAndUuid]
        if isinstance(_workflow, Unset):
            workflow = UNSET
        else:
            workflow = NameAndUuid.from_dict(_workflow)

        _task = d.pop("task", UNSET)
        task: Union[Unset, NameAndUuid]
        if isinstance(_task, Unset):
            task = UNSET
        else:
            task = NameAndUuid.from_dict(_task)

        _start_transition_condition = d.pop("start_transition_condition", UNSET)
        start_transition_condition: Union[Unset, StartTransitionConditionEnum]
        if isinstance(_start_transition_condition, Unset):
            start_transition_condition = UNSET
        else:
            start_transition_condition = StartTransitionConditionEnum(_start_transition_condition)

        max_complete_executions = d.pop("max_complete_executions", UNSET)

        should_eval_transitions_after_first_execution = d.pop("should_eval_transitions_after_first_execution", UNSET)

        condition_count_threshold = d.pop("condition_count_threshold", UNSET)

        condition_ratio_threshold = d.pop("condition_ratio_threshold", UNSET)

        max_age_seconds = d.pop("max_age_seconds", UNSET)

        default_max_retries = d.pop("default_max_retries", UNSET)

        _failure_behavior = d.pop("failure_behavior", UNSET)
        failure_behavior: Union[Unset, FailureBehaviorEnum]
        if isinstance(_failure_behavior, Unset):
            failure_behavior = UNSET
        else:
            failure_behavior = FailureBehaviorEnum(_failure_behavior)

        allow_workflow_execution_after_failure = d.pop("allow_workflow_execution_after_failure", UNSET)

        _timeout_behavior = d.pop("timeout_behavior", UNSET)
        timeout_behavior: Union[Unset, TimeoutBehaviorEnum]
        if isinstance(_timeout_behavior, Unset):
            timeout_behavior = UNSET
        else:
            timeout_behavior = TimeoutBehaviorEnum(_timeout_behavior)

        allow_workflow_execution_after_timeout = d.pop("allow_workflow_execution_after_timeout", UNSET)

        _environment_variables_overrides = d.pop("environment_variables_overrides", UNSET)
        environment_variables_overrides: Union[Unset, None, PatchedWorkflowTaskInstanceEnvironmentVariablesOverrides]
        if _environment_variables_overrides is None:
            environment_variables_overrides = None
        elif isinstance(_environment_variables_overrides, Unset):
            environment_variables_overrides = UNSET
        else:
            environment_variables_overrides = PatchedWorkflowTaskInstanceEnvironmentVariablesOverrides.from_dict(
                _environment_variables_overrides
            )

        allocated_cpu_units = d.pop("allocated_cpu_units", UNSET)

        allocated_memory_mb = d.pop("allocated_memory_mb", UNSET)

        use_task_alert_methods = d.pop("use_task_alert_methods", UNSET)

        ui_color = d.pop("ui_color", UNSET)

        ui_icon_type = d.pop("ui_icon_type", UNSET)

        ui_scale = d.pop("ui_scale", UNSET)

        ui_center_margin_top = d.pop("ui_center_margin_top", UNSET)

        ui_center_margin_left = d.pop("ui_center_margin_left", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _updated_at = d.pop("updated_at", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        patched_workflow_task_instance = cls(
            url=url,
            uuid=uuid,
            name=name,
            description=description,
            workflow=workflow,
            task=task,
            start_transition_condition=start_transition_condition,
            max_complete_executions=max_complete_executions,
            should_eval_transitions_after_first_execution=should_eval_transitions_after_first_execution,
            condition_count_threshold=condition_count_threshold,
            condition_ratio_threshold=condition_ratio_threshold,
            max_age_seconds=max_age_seconds,
            default_max_retries=default_max_retries,
            failure_behavior=failure_behavior,
            allow_workflow_execution_after_failure=allow_workflow_execution_after_failure,
            timeout_behavior=timeout_behavior,
            allow_workflow_execution_after_timeout=allow_workflow_execution_after_timeout,
            environment_variables_overrides=environment_variables_overrides,
            allocated_cpu_units=allocated_cpu_units,
            allocated_memory_mb=allocated_memory_mb,
            use_task_alert_methods=use_task_alert_methods,
            ui_color=ui_color,
            ui_icon_type=ui_icon_type,
            ui_scale=ui_scale,
            ui_center_margin_top=ui_center_margin_top,
            ui_center_margin_left=ui_center_margin_left,
            created_at=created_at,
            updated_at=updated_at,
        )

        patched_workflow_task_instance.additional_properties = d
        return patched_workflow_task_instance

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
